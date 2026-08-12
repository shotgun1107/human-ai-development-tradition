"""Small public CLI for authenticating the machine-readable I3 contract."""

from __future__ import annotations

import argparse
from pathlib import Path

from .contract import verify_contract_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True, type=Path)
    args = parser.parse_args()
    document = verify_contract_file(args.contract)
    print(f"I3_CONTRACT=PASS VERSION={document['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
