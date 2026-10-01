"""Small, local-only CLI for the I0 public-development harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .answer_validation import validate_public_answer_file
from .authentication import (
    PUBLIC_CANONICALS,
    _authenticate_bundle_manifest,
    authenticate_public_file,
)
from .error_reporting import safe_exception_message
from .integrity import verify_public_bundle
from .json_validation import load_json
from .paths import resolve_workspace_path
from .schema_suite import audit_broader_upstream_id_impact, validate_public_schema_instances
from .transform import PROFILES, transform_canonical
from .verification import build_public_verification_record


class CliUsageError(ValueError):
    """Raised instead of argparse writing a non-JSON error and exiting."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def _json_print(value: object, *, stream: object | None = None) -> None:
    print(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        file=sys.stdout if stream is None else stream,
    )


def _parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(prog="s0-i0", description="Public I0 format checks only")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("integrity")
    sub.add_parser("schema-check")
    sub.add_parser("verify")
    transform = sub.add_parser("transform")
    transform.add_argument("--canonical", required=True)
    transform.add_argument("--profile", choices=sorted(PROFILES), required=True)
    transform.add_argument("--output", required=True)
    answer = sub.add_parser("answer-check")
    answer.add_argument("--answer", required=True)
    answer.add_argument("--answer-schema", required=True)
    answer.add_argument("--questions", required=True)
    answer.add_argument("--input", required=True)
    return parser


def _approved_output(workspace_root: Path, raw: str) -> Path:
    path = resolve_workspace_path(workspace_root, raw, must_exist=False)
    approved = (workspace_root / "s0-lab" / "i0").resolve(strict=True)
    try:
        path.relative_to(approved)
    except ValueError as exc:
        raise ValueError("output must remain below s0-lab/i0") from exc
    if not path.parent.exists():
        raise ValueError("output parent directory must already exist")
    return path


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        workspace_root = Path.cwd().resolve(strict=True)
        if args.command in {"integrity", "schema-check", "verify"}:
            _authenticate_bundle_manifest(workspace_root)
        if args.command == "integrity":
            _json_print(verify_public_bundle(workspace_root))
            return 0
        if args.command == "schema-check":
            result = validate_public_schema_instances(workspace_root)
            result["broader_upstream_impact"] = audit_broader_upstream_id_impact(
                workspace_root
            )
            _json_print(result)
            return 0 if result["error_count"] == 0 else 1
        if args.command == "verify":
            result = build_public_verification_record(workspace_root)
            _json_print(result)
            return 0 if result["status"] == "pass" else 1
        if args.command == "transform":
            canonical_path = authenticate_public_file(
                workspace_root, args.canonical, PUBLIC_CANONICALS
            )
            canonical, _ = load_json(canonical_path)
            generated = transform_canonical(canonical, args.profile)
            output_path = _approved_output(workspace_root, args.output)
            with output_path.open("xb") as handle:
                handle.write(generated)
            _json_print({"status": "pass", "output": output_path.relative_to(workspace_root).as_posix()})
            return 0
        if args.command == "answer-check":
            errors = validate_public_answer_file(
                workspace_root,
                args.answer,
                answer_schema=args.answer_schema,
                questions=args.questions,
                input_package=args.input,
            )
            result = {"status": "pass" if not errors else "fail", "errors": [error.as_dict() for error in errors]}
            _json_print(result)
            return 0 if not errors else 1
        raise AssertionError("unreachable command")
    except Exception as exc:
        _json_print(
            {
                "status": "error",
                "error": {
                    "category": type(exc).__name__,
                    "message": safe_exception_message(exc),
                },
            },
            stream=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
