"""Deterministic P01-P04 adapters for the public practice canonical format.

The adapters consume only one in-memory canonical object and one opaque profile
ID.  They do not import I/O or communication libraries.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Callable
from typing import Any


class TransformationError(ValueError):
    """The canonical input cannot be transformed without inference."""


PROFILES = frozenset({"P01", "P02", "P03", "P04"})


def _one(facts: list[dict[str, Any]], predicate: Callable[[dict[str, Any]], bool], role: str) -> dict[str, Any]:
    matches = [fact for fact in facts if predicate(fact)]
    if len(matches) != 1:
        raise TransformationError(f"canonical input must contain exactly one explicit {role} fact")
    return matches[0]


def _roles(canonical: dict[str, Any]) -> dict[str, Any]:
    facts = canonical["facts"]
    private = _one(
        facts,
        lambda f: "project-private" in f["text"] and "owns the raw" in f["text"],
        "private-boundary",
    )
    derived = _one(facts, lambda f: "directly from" in f["text"], "direct-derivation")
    correlated = [fact for fact in facts if "correlated with" in fact["text"]]
    if len(correlated) != 2:
        raise TransformationError("canonical input must contain exactly two explicit correlated facts")
    correlated.sort(key=lambda fact: fact["fact_id"])
    counter = _one(
        facts,
        lambda f: "counterexample" in f["text"]
        and ("explicitly states" in f["text"] or "explicitly identifies" in f["text"]),
        "counterexample",
    )
    withdrawal = _one(facts, lambda f: "withdrew" in f["text"], "withdrawal")
    data = _one(
        facts,
        lambda f: ("untrusted test data" in f["text"] or "hostile sample data" in f["text"])
        and "not" in f["text"]
        and "instruction" in f["text"],
        "untrusted-data",
    )
    responsibility = _one(
        facts,
        lambda f: "central workspace" in f["text"] and "Project Brain owner" in f["text"],
        "responsibility-boundary",
    )
    candidate = _one(facts, lambda f: "asset candidate" in f["text"], "candidate")
    no_change = _one(
        facts,
        lambda f: "state change" in f["text"] and "human review" in f["text"],
        "no-change",
    )
    data_permission = _one(
        facts,
        lambda f: f["project_id"] == data["project_id"]
        and data["record_id"] in f["text"]
        and ("execut" in f["text"] or "authority" in f["text"]),
        "untrusted-data permission",
    )
    state_match = re.search(r"\b(pending|paused)\b", candidate["text"])
    if not state_match:
        raise TransformationError("candidate fact lacks an explicit supported state")
    return {
        "private": private,
        "derived": derived,
        "correlated": correlated,
        "counter": counter,
        "withdrawal": withdrawal,
        "data": data,
        "data_permission": data_permission,
        "responsibility": responsibility,
        "candidate": candidate,
        "no_change": no_change,
        "candidate_state": state_match.group(1),
    }


def _validate_canonical(canonical: dict[str, Any]) -> None:
    required = {"practice_version", "block_id", "practice_only", "projects", "target_task_id", "facts"}
    if set(canonical) != required or canonical.get("practice_only") is not True:
        raise TransformationError("canonical input is not the frozen public practice shape")
    facts = canonical.get("facts")
    if not isinstance(facts, list) or not facts:
        raise TransformationError("canonical facts must be a non-empty array")
    required_fact = {"fact_id", "record_id", "project_id", "observed_at", "text"}
    if any(set(fact) != required_fact for fact in facts):
        raise TransformationError("each fact must contain only the five frozen public fields")
    for key in ("fact_id", "record_id"):
        values = [fact[key] for fact in facts]
        if len(values) != len(set(values)):
            raise TransformationError(f"duplicate {key}")


def _build_view(canonical: dict[str, Any], profile: str) -> dict[str, Any]:
    facts = canonical["facts"]
    if profile == "P01":
        ordered = sorted(facts, key=lambda fact: (fact["observed_at"], fact["fact_id"]))
        return {
            "label": "P01",
            "ordering_source": "observed_at",
            "boundary_rule": "retain record_id and project_id",
            "event_order": [fact["fact_id"] for fact in ordered],
            "rule": "Read the supplied events in observed_at order while retaining each project_id boundary.",
        }
    if profile == "P02":
        boundaries = [*canonical["projects"], canonical["target_task_id"]]
        groups = [
            {
                "project_id": project_id,
                "fact_ids": [fact["fact_id"] for fact in facts if fact["project_id"] == project_id],
            }
            for project_id in boundaries
        ]
        if any(not group["fact_ids"] for group in groups):
            raise TransformationError("every supplied project boundary must own at least one fact")
        if {fact["project_id"] for fact in facts} != set(boundaries):
            raise TransformationError("fact project boundary is not declared by canonical input")
        return {
            "label": "P02",
            "project_groups": groups,
            "rule": "Read records inside their supplied project_id boundary and retain local source and state text.",
        }

    roles = _roles(canonical)
    if profile == "P03":
        private = roles["private"]
        derived = roles["derived"]
        corr1, corr2 = roles["correlated"]
        withdrawal = roles["withdrawal"]
        data = roles["data"]
        permission = roles["data_permission"]
        candidate = roles["candidate"]
        no_change = roles["no_change"]
        return {
            "label": "P03",
            "markers": [
                {"fact_id": private["fact_id"], "state": "private", "scope": private["project_id"], "source_record_id": private["record_id"], "supporting_fact_ids": [private["fact_id"]]},
                {"fact_id": derived["fact_id"], "state": "withdrawn", "scope": "evaluation", "source_record_id": derived["record_id"], "supporting_fact_ids": [derived["fact_id"], withdrawal["fact_id"]]},
                {"fact_id": corr1["fact_id"], "state": "suspended", "scope": "evaluation", "source_record_id": corr1["record_id"], "supporting_fact_ids": [corr1["fact_id"], withdrawal["fact_id"]]},
                {"fact_id": corr2["fact_id"], "state": "suspended", "scope": "evaluation", "source_record_id": corr2["record_id"], "supporting_fact_ids": [corr2["fact_id"], withdrawal["fact_id"]]},
                {"fact_id": data["fact_id"], "state": "data-only", "scope": data["project_id"], "source_record_id": data["record_id"], "supporting_fact_ids": [data["fact_id"], permission["fact_id"]]},
                {"fact_id": candidate["fact_id"], "state": roles["candidate_state"], "scope": candidate["project_id"], "source_record_id": candidate["record_id"], "supporting_fact_ids": [withdrawal["fact_id"], candidate["fact_id"], no_change["fact_id"]]},
            ],
        }

    derived = roles["derived"]
    private = roles["private"]
    corr1, corr2 = roles["correlated"]
    counter = roles["counter"]
    withdrawal = roles["withdrawal"]
    responsibility = roles["responsibility"]
    candidate = roles["candidate"]
    no_change = roles["no_change"]
    return {
        "label": "P04",
        "relation_dictionary": {
            "R01": "is directly derived from",
            "R02": "is explicitly correlated with",
            "R03": "is suspended by",
            "R04": "is an explicit counterexample to",
            "R05": "requires a decision by",
            "R06": "is candidate for",
        },
        "relations": [
            {"code": "R01", "from_record_id": derived["record_id"], "to_record_id": private["record_id"], "supporting_fact_ids": [derived["fact_id"]]},
            {"code": "R02", "from_record_id": corr1["record_id"], "to_record_id": derived["record_id"], "supporting_fact_ids": [corr1["fact_id"]]},
            {"code": "R02", "from_record_id": corr2["record_id"], "to_record_id": derived["record_id"], "supporting_fact_ids": [corr2["fact_id"]]},
            {"code": "R04", "from_record_id": counter["record_id"], "to_record_id": candidate["record_id"], "supporting_fact_ids": [counter["fact_id"], candidate["fact_id"]]},
            {"code": "R03", "from_record_id": candidate["record_id"], "to_record_id": withdrawal["record_id"], "supporting_fact_ids": [withdrawal["fact_id"], candidate["fact_id"]]},
            {"code": "R05", "from_record_id": no_change["record_id"], "to_record_id": responsibility["record_id"], "supporting_fact_ids": [responsibility["fact_id"], no_change["fact_id"]]},
            {"code": "R06", "from_record_id": derived["record_id"], "to_record_id": candidate["record_id"], "supporting_fact_ids": [candidate["fact_id"]]},
        ],
    }


def _compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def serialize_package(package: dict[str, Any]) -> bytes:
    fact_lines = ",\n".join(f"    {_compact(fact)}" for fact in package["facts"])
    text = (
        "{\n"
        f'  "practice_version":{_compact(package["practice_version"])},\n'
        f'  "block_id":{_compact(package["block_id"])},\n'
        f'  "representation_id":{_compact(package["representation_id"])},\n'
        "  \"facts\":[\n"
        f"{fact_lines}\n"
        "  ],\n"
        f'  "view":{_compact(package["view"])}\n'
        "}\n"
    )
    return text.encode("utf-8")


def transform_canonical(canonical: dict[str, Any], profile: str) -> bytes:
    """Return canonical package bytes for one opaque public profile."""

    _validate_canonical(canonical)
    if profile not in PROFILES:
        raise TransformationError("profile must be one of P01, P02, P03, or P04")
    package = {
        "practice_version": canonical["practice_version"],
        "block_id": canonical["block_id"],
        "representation_id": profile,
        "facts": copy.deepcopy(canonical["facts"]),
        "view": _build_view(canonical, profile),
    }
    return serialize_package(package)
