"""Bounded public I2 trust-root and role-isolation candidate."""

from .contract import (
    signer_context_from_contract_bytes,
    signer_context_from_contract_file,
    verify_contract_bytes,
    verify_contract_file,
)
from .errors import (
    BindingError,
    CanonicalRecordError,
    I2Error,
    LifecycleError,
    UnsupportedBoundaryError,
    VectorBindingError,
)
from .lifecycle import (
    ImportRouteContext,
    bind_import_route_context,
    classify_event_variant,
    classify_outcome_medium,
    validate_durable_ledger,
    validate_event_global_chain,
    validate_event_global_link,
    validate_import_route,
    validate_supplied_route_set,
    validate_witness,
)
from .records import (
    ImportLedgerEvent,
    SignerRegistryContext,
    bind_public_i1_signer_context,
    import_event_sha256,
    parse_import_admission,
    parse_import_event,
    parse_import_outcome,
    serialize_import_admission,
    serialize_import_event,
    serialize_import_outcome,
    validate_complete_import,
    validate_outcome_binding,
)
from .vectors import FrozenVectorPackage, bind_frozen_tri2_vec_02

__all__ = [
    "BindingError",
    "CanonicalRecordError",
    "FrozenVectorPackage",
    "I2Error",
    "ImportLedgerEvent",
    "ImportRouteContext",
    "LifecycleError",
    "SignerRegistryContext",
    "UnsupportedBoundaryError",
    "VectorBindingError",
    "bind_frozen_tri2_vec_02",
    "bind_import_route_context",
    "bind_public_i1_signer_context",
    "classify_event_variant",
    "classify_outcome_medium",
    "import_event_sha256",
    "parse_import_admission",
    "parse_import_event",
    "parse_import_outcome",
    "serialize_import_admission",
    "serialize_import_event",
    "serialize_import_outcome",
    "signer_context_from_contract_bytes",
    "signer_context_from_contract_file",
    "validate_complete_import",
    "validate_durable_ledger",
    "validate_event_global_chain",
    "validate_event_global_link",
    "validate_import_route",
    "validate_supplied_route_set",
    "validate_outcome_binding",
    "validate_witness",
    "verify_contract_bytes",
    "verify_contract_file",
]

__version__ = "0.3.0"
