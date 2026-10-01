"""Neutral answer-format and public question-policy validation."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .authentication import (
    PUBLIC_PACKAGES,
    PUBLIC_QUESTIONS,
    authenticate_answer_candidate,
    authenticate_answer_schema,
    authenticate_public_file,
)
from .integrity import sha256_bytes
from .json_validation import load_json, validate_instance


@dataclass(frozen=True, order=True)
class ProtocolError:
    category: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


FORBIDDEN_REASON_PATTERNS = (
    re.compile(r"\bP0[1-4]\b", re.IGNORECASE),
    re.compile(r"(?:^|[/\\])(?:packages|runner)(?:[/\\])", re.IGNORECASE),
    re.compile(r"\binput\.json\b", re.IGNORECASE),
    re.compile(
        r"\b(?:representation_id|ordering_source|boundary_rule|event_order|project_groups|fact_ids|"
        r"markers|source_record_id|supporting_fact_ids|from_record_id|to_record_id|"
        r"relation_dictionary|relations)\b",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*(?:state|scope|code)\s*[.!]?\s*$", re.IGNORECASE),
    re.compile(r"\b(?:state|scope|code)\s+(?:field|key|value)\b", re.IGNORECASE),
    re.compile(r"\bP0[1-4]B[12][A-Z0-9]+\b", re.IGNORECASE),
    re.compile(r"\bR0[1-6]\b"),
    re.compile(r"\b(?:C[1-7]|M[1-6])\b"),
    re.compile(r"\b(?:rank(?:ing|ed)?|target preference|preferred structure)\b", re.IGNORECASE),
    re.compile(r"\bS0[\s-]*(?:ready|complete|validated|approved)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:I0|implementation|system)(?:[\s-]+(?:is|has[\s-]+been))?[\s-]+"
        r"(?:ready|complete|completed|frozen|validated|operational)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:implemented|operational implementation|validated system|central system works)\b", re.IGNORECASE),
)


def _add(errors: list[ProtocolError], category: str, path: str, message: str) -> None:
    errors.append(ProtocolError(category, path, message))


def _validate_answer_data(
    answer: dict[str, Any],
    answer_schema: dict[str, Any],
    question_projection: dict[str, Any],
    input_package: dict[str, Any],
    input_bytes: bytes,
    *,
    answer_bytes: bytes | None = None,
) -> list[ProtocolError]:
    """Validate format and public policies without oracle or scoring input."""

    schema_errors = validate_instance(answer, answer_schema)
    if schema_errors:
        return sorted(
            ProtocolError("schema", error.instance_path, error.message)
            for error in schema_errors
        )

    errors: list[ProtocolError] = []
    if answer_bytes is not None and len(answer_bytes) > 8192:
        _add(errors, "answer-size", "$", "answer exceeds 8192 UTF-8 bytes")
    if answer["block_id"] != question_projection["block_id"] or answer["block_id"] != input_package["block_id"]:
        _add(errors, "block-id", "$.block_id", "block_id does not match public inputs")
    if answer["input_hash"] != sha256_bytes(input_bytes):
        _add(errors, "input-hash", "$.input_hash", "input_hash does not match supplied package bytes")

    expected_questions = question_projection["questions"]
    expected_ids = [item["question_id"] for item in expected_questions]
    actual_ids = [item["question_id"] for item in answer["answers"]]
    if actual_ids != sorted(actual_ids):
        _add(errors, "question-order", "$.answers", "answers must be sorted by question_id")
    duplicate_ids = sorted({item for item in actual_ids if actual_ids.count(item) > 1})
    if duplicate_ids:
        _add(errors, "question-duplicate", "$.answers", f"duplicate question IDs: {duplicate_ids}")
    missing = sorted(set(expected_ids) - set(actual_ids))
    extra = sorted(set(actual_ids) - set(expected_ids))
    if missing:
        _add(errors, "question-missing", "$.answers", f"missing question IDs: {missing}")
    if extra:
        _add(errors, "question-extra", "$.answers", f"extra question IDs: {extra}")

    questions = {item["question_id"]: item for item in expected_questions}
    allowed_records = {fact["record_id"] for fact in input_package["facts"]}
    for index, item in enumerate(answer["answers"]):
        path = f"$.answers[{index}]"
        question = questions.get(item["question_id"])
        if question is None:
            continue
        options = {option["option_id"] for option in question["options"]}
        if item["decision_option_id"] not in options:
            _add(errors, "decision-option", path + ".decision_option_id", "decision option is not allowed for this question")

        cited = item["cited_record_ids"]
        affected = item["affected_record_ids"]
        if cited != sorted(cited) or len(cited) != len(set(cited)):
            _add(errors, "citation-order", path + ".cited_record_ids", "cited IDs must be unique and sorted")
        if affected != sorted(affected) or len(affected) != len(set(affected)):
            _add(errors, "affected-order", path + ".affected_record_ids", "affected IDs must be unique and sorted")
        if question["citation_policy"] == "required" and not cited:
            _add(errors, "citation-required", path + ".cited_record_ids", "at least one citation is required")
        invalid_cited = sorted(set(cited) - allowed_records)
        invalid_affected = sorted(set(affected) - allowed_records)
        if invalid_cited:
            _add(errors, "citation-id", path + ".cited_record_ids", f"unknown record IDs: {invalid_cited}")
        if invalid_affected:
            _add(errors, "affected-id", path + ".affected_record_ids", f"unknown record IDs: {invalid_affected}")

        policy = question["affected_ids_policy"]
        if policy == "must-be-empty" and affected:
            _add(errors, "affected-forbidden", path + ".affected_record_ids", "affected IDs must be empty")
        if policy == "required-nonempty" and not affected:
            _add(errors, "affected-required", path + ".affected_record_ids", "affected IDs must be non-empty")

        reason = item["short_reason"]
        if "\n" in reason or "\r" in reason:
            _add(errors, "reason-line", path + ".short_reason", "short_reason must be one line")
        if any(pattern.search(reason) for pattern in FORBIDDEN_REASON_PATTERNS):
            _add(errors, "forbidden-disclosure", path + ".short_reason", "short_reason contains forbidden structural disclosure")

    return sorted(errors)


def validate_answer_candidate_bytes(
    workspace_root: Path,
    answer_bytes: bytes,
    *,
    answer_schema: str | Path,
    questions: str | Path,
    input_package: str | Path,
) -> list[ProtocolError]:
    """Validate untrusted answer bytes against authenticated frozen dependencies."""

    try:
        answer = json.loads(answer_bytes.decode("utf-8"))
    except UnicodeDecodeError:
        return [ProtocolError("utf8", "$", "answer is not valid UTF-8")]
    except json.JSONDecodeError as exc:
        return [
            ProtocolError(
                "json-parse",
                "$",
                f"invalid JSON at line {exc.lineno}, column {exc.colno}",
            )
        ]

    schema_path = authenticate_answer_schema(workspace_root, answer_schema)
    question_path = authenticate_public_file(workspace_root, questions, PUBLIC_QUESTIONS)
    input_path = authenticate_public_file(workspace_root, input_package, PUBLIC_PACKAGES)
    schema, _ = load_json(schema_path)
    question_projection, _ = load_json(question_path)
    package, input_bytes = load_json(input_path)
    return _validate_answer_data(
        answer,
        schema,
        question_projection,
        package,
        input_bytes,
        answer_bytes=answer_bytes,
    )


def validate_public_answer_file(
    workspace_root: Path,
    answer: str | Path,
    *,
    answer_schema: str | Path,
    questions: str | Path,
    input_package: str | Path,
) -> list[ProtocolError]:
    """Validate an approved public answer or an untrusted candidate below I0."""

    answer_path = authenticate_answer_candidate(workspace_root, answer)
    return validate_answer_candidate_bytes(
        workspace_root,
        answer_path.read_bytes(),
        answer_schema=answer_schema,
        questions=questions,
        input_package=input_package,
    )
