"""Public I2 trust-root and role-isolation implementation candidate."""

from .lifecycle import (
    OutcomeClassification,
    classify_outcome_medium,
    validate_event_global_link,
    validate_import_route,
)
from .contract import verify_contract_bytes, verify_contract_file
from .records import (
    ImportAdmission,
    ImportLedgerEvent,
    ImportOutcome,
    parse_import_admission,
    parse_import_event,
    parse_import_outcome,
    serialize_import_admission,
    serialize_import_event,
    serialize_import_outcome,
    validate_outcome_binding,
)
from .vectors import FrozenVectorPackage, bind_frozen_tri2_vec_02

__all__ = [
    "FrozenVectorPackage",
    "ImportAdmission",
    "ImportLedgerEvent",
    "ImportOutcome",
    "OutcomeClassification",
    "bind_frozen_tri2_vec_02",
    "classify_outcome_medium",
    "parse_import_admission",
    "parse_import_event",
    "parse_import_outcome",
    "serialize_import_admission",
    "serialize_import_event",
    "serialize_import_outcome",
    "validate_event_global_link",
    "validate_import_route",
    "validate_outcome_binding",
    "verify_contract_bytes",
    "verify_contract_file",
]

__version__ = "0.1.0"
