"""Externally supplied public trust pins.

These values are accepted only as explicit caller inputs.  Candidate code is
never allowed to discover or select them from neighboring files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


LOWER_SHA256 = re.compile(r"^[0-9a-f]{64}$")

I0_IMPLEMENTATION_MANIFEST_SHA256 = "f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae"
I1_IMPLEMENTATION_MANIFEST_SHA256 = "668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c"
I2_IMPLEMENTATION_MANIFEST_SHA256 = "18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6"
I3_IMPLEMENTATION_MANIFEST_SHA256 = "e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648"
DESIGN_PACKAGE_MANIFEST_SHA256 = "6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802"
DESIGN_INDEPENDENT_REVIEW_SHA256 = "7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137"


def _digest(value: str, label: str) -> str:
    if type(value) is not str or LOWER_SHA256.fullmatch(value) is None:
        raise ValueError(f"{label} must be exactly 64 lowercase hexadecimal characters")
    return value


@dataclass(frozen=True)
class ExternalPins:
    assembly_implementation_manifest_sha256: str
    design_package_manifest_sha256: str
    design_independent_review_sha256: str

    def __post_init__(self) -> None:
        _digest(self.assembly_implementation_manifest_sha256, "implementation pin")
        _digest(self.design_package_manifest_sha256, "design-package pin")
        _digest(self.design_independent_review_sha256, "independent-review pin")
        if self.design_package_manifest_sha256 != DESIGN_PACKAGE_MANIFEST_SHA256:
            raise ValueError("design-package pin is not the accepted v0.5 authority")
        if self.design_independent_review_sha256 != DESIGN_INDEPENDENT_REVIEW_SHA256:
            raise ValueError("independent-review pin is not the accepted v0.5 authority")

    def receipt_fields(self) -> dict[str, str]:
        return {
            "assembly_implementation_manifest_sha256": self.assembly_implementation_manifest_sha256,
            "design_package_manifest_sha256": self.design_package_manifest_sha256,
            "design_independent_review_sha256": self.design_independent_review_sha256,
        }
