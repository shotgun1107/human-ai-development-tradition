"""Pre-import bootstrap for the bounded v0.5 evidence transaction (inherited v0.4 guard ABI).

The exact native bind happens before the fixed downstream bridge import.  The
bridge is intentionally absent from this candidate: the later live-assembly
gate must supply it as an authenticated final-runtime row.  Missing or rejected
bridge import therefore fails closed without an early commit or PASS claim.
"""

from __future__ import annotations

import sys


_NAMES = (
    "--s0-admission-read=",
    "--s0-commit-request-write=",
    "--s0-commit-reply-read=",
    "--s0-output-root=",
    "--s0-preloader-process=",
)


def _locator(argument: str, prefix: str) -> int:
    if type(argument) is not str or not argument.startswith(prefix):
        raise RuntimeError("runtime locator name or order differs")
    value = argument[len(prefix) :]
    if (
        len(value) != 18
        or not value.startswith("0x")
        or any(char not in "0123456789abcdef" for char in value[2:])
    ):
        raise RuntimeError("runtime locator grammar differs")
    number = int(value[2:], 16)
    if number in {0, 0xFFFFFFFFFFFFFFFF}:
        raise RuntimeError("runtime locator is a sentinel")
    return number


def main() -> int:
    if len(sys.argv) != 6:
        raise RuntimeError("runtime bootstrap argument count differs")
    bootstrap_path = sys.argv[0]
    values = tuple(_locator(value, prefix) for value, prefix in zip(sys.argv[1:], _NAMES, strict=True))
    if len(set(values)) != 5:
        raise RuntimeError("runtime locator set is not distinct")

    import s0_runtime_handle_guard_v0_4 as _guard

    binding = _guard.bind_once_v4(values)
    del _guard
    sys.argv[:] = [bootstrap_path]

    # This exact name is not caller-selectable.  Its future implementation must
    # retain ``binding`` privately, complete the assembly controller and witness
    # sequence, and only then invoke the binding's one-use commit method.
    import s0_public_assembly_live_bridge_v0_1 as _bridge

    result = _bridge.run_with_runtime_admission(binding)
    if type(result) is not int or result != 0:
        raise RuntimeError("live assembly bridge result differs")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
