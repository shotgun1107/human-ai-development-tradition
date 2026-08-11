"""Public model-free verification entrypoint for the I2 candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contract import CONTRACT_SHA256, verify_contract_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m s0_i2.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--contract", type=Path, required=True)
    args = parser.parse_args(argv)
    document = verify_contract_file(args.contract)
    print(
        json.dumps(
            {
                "contract_sha256": CONTRACT_SHA256,
                "records": {
                    name: value["line_count"]
                    for name, value in document["records"].items()
                },
                "status": "PASS",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
