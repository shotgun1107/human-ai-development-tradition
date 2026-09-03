"""Command-line entry point for the v0.7 Windows runtime materializer."""

from __future__ import annotations

import argparse
import json
import sys

from .materialize import materialize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="s0-public-build-runtime-v0.7")
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--final-root", required=True)
    arguments = parser.parse_args(argv)
    try:
        result = materialize(arguments.repository_root, arguments.cache_root, arguments.final_root)
    except Exception as error:
        print(json.dumps({"error_type": type(error).__name__, "status": "REJECTED"}, separators=(",", ":"), sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps({"final_root": result.final_root, "payload_manifest_sha256": result.payload_manifest_sha256, "runtime_record_sha256": result.runtime_record_sha256, "status": result.status}, separators=(",", ":"), sort_keys=True))
    return 0
