"""Bounded public I3 import-decision implementation candidate."""

from .boundaries import enforce_platform_isolation, run_s0, validate_durable_ledger, validate_witness
from .classifier import (
    ClassificationFactSet,
    bind_classification_fact_set,
    classify_import_attempt,
)
from .contract import verify_contract_bytes, verify_contract_file
from .errors import (
    I3BindingError,
    I3ByteError,
    I3Error,
    I3EventError,
    I3FieldError,
    I3HashError,
    I3InputError,
    I3RouteError,
    I3TupleError,
    I3UnsupportedBoundaryError,
    I3ValueError,
)
from .finalizer import finalize_import_attempt, validate_completion_event
from .models import ImportClassification, ImportDecision
from .records import (
    ADMISSION_FIELD_ORDER,
    OUTCOME_FIELD_ORDER,
    ImportAdmission,
    ImportOutcome,
    hash_import_admission,
    hash_import_outcome_frame,
    parse_import_admission,
    parse_import_outcome_frame,
    serialize_import_admission,
    serialize_import_outcome,
    validate_outcome_binding,
)

__all__ = [
    "ADMISSION_FIELD_ORDER",
    "ClassificationFactSet",
    "I3BindingError",
    "I3ByteError",
    "I3Error",
    "I3EventError",
    "I3FieldError",
    "I3HashError",
    "I3InputError",
    "I3RouteError",
    "I3TupleError",
    "I3UnsupportedBoundaryError",
    "I3ValueError",
    "ImportAdmission",
    "ImportClassification",
    "ImportDecision",
    "ImportOutcome",
    "OUTCOME_FIELD_ORDER",
    "bind_classification_fact_set",
    "classify_import_attempt",
    "enforce_platform_isolation",
    "finalize_import_attempt",
    "hash_import_admission",
    "hash_import_outcome_frame",
    "parse_import_admission",
    "parse_import_outcome_frame",
    "run_s0",
    "serialize_import_admission",
    "serialize_import_outcome",
    "validate_completion_event",
    "validate_durable_ledger",
    "validate_outcome_binding",
    "validate_witness",
    "verify_contract_bytes",
    "verify_contract_file",
]

__version__ = "0.1.0"
