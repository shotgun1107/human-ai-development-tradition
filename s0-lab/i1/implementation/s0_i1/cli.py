"""Local public-only CLI for I1 structural verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import safe_exception_message
from .verification import build_public_verification_record


class CliUsageError(ValueError):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def _parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        prog="s0-i1", description="URC-0.14 public structural checks only"
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("verify")
    return parser


def _emit(value: object, stream: object | None = None) -> None:
    print(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")),
        file=sys.stdout if stream is None else stream,
    )


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _parser().parse_args(argv)
        if arguments.command == "verify":
            record = build_public_verification_record(Path.cwd().resolve(strict=True))
            _emit(record)
            return 0 if record["status"] == "pass" else 1
        raise AssertionError("unreachable command")
    except Exception as exc:
        _emit(
            {
                "status": "error",
                "error": {
                    "category": type(exc).__name__,
                    "message": safe_exception_message(exc),
                },
            },
            sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
