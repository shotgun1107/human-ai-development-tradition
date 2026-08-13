"""Child-process entrypoint for the bounded public controller."""

from __future__ import annotations

from .runtime_guard import (
    install_runtime_sentinels,
    require_file_open_sentinel_configured,
)


# Import/capability denial precedes controller/component imports.  The parent
# supplies the authenticated file set before main installs the open sentinel.
install_runtime_sentinels()
require_file_open_sentinel_configured()

import argparse
import sys
from pathlib import Path

from .canonical import canonical_json_bytes
from .channel import FixedAsciiPipeChannel
from .controller import AssemblyController
from .errors import AssemblyRunFailed
from .records import ExternalPins


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="s0-public-assembly-candidate-child")
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--assembly-implementation-manifest-sha256", required=True)
    parser.add_argument("--design-package-manifest-sha256", required=True)
    parser.add_argument("--design-independent-review-sha256", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    workspace_root = Path(arguments.workspace_root)
    output_root = Path(arguments.output_root)
    pins = ExternalPins(
        assembly_implementation_manifest_sha256=(
            arguments.assembly_implementation_manifest_sha256
        ),
        design_package_manifest_sha256=arguments.design_package_manifest_sha256,
        design_independent_review_sha256=arguments.design_independent_review_sha256,
    )
    channel = FixedAsciiPipeChannel(
        request_writer=sys.stdout.buffer,
        reply_reader=sys.stdin.buffer,
    )
    controller = AssemblyController(
        workspace_root=workspace_root,
        output_root=output_root,
        external_pins=pins,
        publication_channel=channel,
    )
    try:
        controller.run()
    except AssemblyRunFailed as exc:
        sys.stderr.buffer.write(canonical_json_bytes(exc.diagnostic.as_dict()))
        sys.stderr.buffer.flush()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
