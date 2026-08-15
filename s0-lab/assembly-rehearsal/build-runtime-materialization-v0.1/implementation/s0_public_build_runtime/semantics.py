"""Effective v0.5 semantic reconstruction from authenticated design bytes."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .authority import AuthenticatedDesign
from .canonical import jcs_lf, semantic_relations_preimage, sha256_hex, strict_json
from .errors import SemanticError

_ROOT = "s0-lab/control/assembly-rehearsal/build-runtime-materialization-"
_OLD_RELATION = "application-directory-equals-parent-of-verifier_application-runtime-row"
_NEW_RELATION = "application-directory-equals-parent-of-verifier-application-runtime-row"
_RELATION_SHA256 = "5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db"
_POLICY_SHA256 = "3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b"
_V04_MATRIX_SHA256 = "9d2522bdce4a64b612fbac300ff3090d317da32e7bb85b7c021e2ae030a8bf0e"


def _path(version: int, filename: str) -> str:
    return f"{_ROOT}v0.{version}/{filename}"


def _object(design: AuthenticatedDesign, path: str) -> dict[str, object]:
    design.require_authenticated()
    raw = design.files.get(path)
    if raw is None:
        raise SemanticError("required authenticated design file is absent")
    value = strict_json(raw)
    if type(value) is not dict:
        raise SemanticError("design JSON root is not an exact object")
    return value


def _property_const(schema: Mapping[str, object], name: str) -> object:
    try:
        properties = schema["properties"]
        if type(properties) is not dict:
            raise KeyError
        property_schema = properties[name]
        if type(property_schema) is not dict or "const" not in property_schema:
            raise KeyError
        return property_schema["const"]
    except KeyError as error:
        raise SemanticError(f"schema property const is missing: {name}") from error


def _relation_inventory(design: AuthenticatedDesign) -> tuple[str, ...]:
    interface = _object(design, _path(4, "build-runtime-materialization-interface-map-v0.4.json"))
    schema = _object(design, _path(4, "build-runtime-materialization-profile-v0.4.schema.json"))
    map_relations = interface.get("semantic_relations")
    schema_relations = _property_const(schema, "semantic_relations")
    if type(map_relations) is not list or map_relations != schema_relations or len(map_relations) != 68:
        raise SemanticError("v0.4 relation authorities do not match exactly")
    if any(type(value) is not str for value in map_relations):
        raise SemanticError("v0.4 relation is not exact text")
    if map_relations[15] != _OLD_RELATION or map_relations.count(_OLD_RELATION) != 1:
        raise SemanticError("v0.4 required old relation is not unique at index 15")
    effective = tuple(map_relations[:15] + [_NEW_RELATION] + map_relations[16:])
    if len(set(effective)) != 68:
        raise SemanticError("effective relation inventory is not unique")
    raw = semantic_relations_preimage(effective)
    if len(raw) != 6805 or sha256_hex(raw) != _RELATION_SHA256:
        raise SemanticError("effective relation preimage identity differs")
    v05_interface = _object(design, _path(5, "build-runtime-materialization-interface-map-v0.5.json"))
    patch = v05_interface.get("semantic_relation_patch")
    if type(patch) is not dict:
        raise SemanticError("v0.5 relation patch is absent")
    expected = {
        "all_other_indices_byte_identical": True,
        "base_relation_count": 68,
        "effective_relation_count": 68,
        "effective_relations_preimage_grammar": "S0-BRM-SEMANTIC-RELATIONS-5",
        "effective_relations_sha256": _RELATION_SHA256,
        "replacement_index_zero_based": 15,
        "replacement_value": _NEW_RELATION,
        "required_old_value": _OLD_RELATION,
    }
    if patch != expected:
        raise SemanticError("v0.5 relation patch record differs")
    return effective


def _policy(design: AuthenticatedDesign) -> Mapping[str, object]:
    schema = _object(design, _path(4, "build-runtime-materialization-profile-v0.4.schema.json"))
    policy = _property_const(schema, "publication_no_replace_policy")
    if type(policy) is not dict or len(policy) != 20:
        raise SemanticError("normative publication policy is not the closed 20-field object")
    raw = jcs_lf(policy)
    if len(raw) != 896 or sha256_hex(raw) != _POLICY_SHA256:
        raise SemanticError("normative publication policy identity differs")
    v05_interface = _object(design, _path(5, "build-runtime-materialization-interface-map-v0.5.json"))
    authority = v05_interface.get("publication_no_replace_policy_authority")
    expected = {
        "base_interface_map_policy_summary_authoritative_for_hash": False,
        "base_profile_policy_hash_authoritative_without_v0_5_recomputation": False,
        "field_count": 20,
        "hash_preimage": "RFC8785-JCS-UTF8-exact-normative-object-plus-one-final-LF",
        "normative_object_path": "base_profile.publication_no_replace_policy",
        "normative_policy_sha256": _POLICY_SHA256,
        "single_normative_object": True,
    }
    if authority != expected:
        raise SemanticError("v0.5 publication policy authority differs")
    return MappingProxyType(dict(policy))


def _failure_suffix_matches(row: Mapping[str, object]) -> bool:
    failure = row.get("expected_primary_failure")
    output = row.get("output_created_before_primary_failure")
    if type(failure) is not str or type(output) is not bool:
        return False
    return failure.endswith("/1") if output else failure.endswith("/0")


def _effective_matrix(design: AuthenticatedDesign) -> tuple[Mapping[str, object], ...]:
    v1 = _object(design, _path(1, "build-runtime-materialization-mutation-matrix-v0.1.json"))
    v2 = _object(design, _path(2, "build-runtime-materialization-mutation-matrix-v0.2.json"))
    base = v1.get("mutations")
    retained = v2.get("retained_rows")
    replacements = v2.get("replacement_rows")
    removed = v2.get("removed_base_row_ids")
    if type(base) is not list or type(retained) is not list or type(replacements) is not list or type(removed) is not list:
        raise SemanticError("v0.1/v0.2 matrix structure differs")
    if len(base) != 46 or len(retained) != 43 or len(replacements) != 20:
        raise SemanticError("v0.1/v0.2 matrix cardinality differs")
    if removed != ["BRM-BUILD-003", "BRM-BUILD-005", "BRM-RETRY-001"]:
        raise SemanticError("v0.2 removed matrix IDs differ")
    retained_by_id = {row.get("id"): row for row in retained if type(row) is dict}
    if len(retained_by_id) != 43:
        raise SemanticError("v0.2 retained matrix IDs are not unique")
    effective: list[dict[str, object]] = []
    used_replacements: set[str] = set()
    for row in base:
        if type(row) is not dict or type(row.get("id")) is not str:
            raise SemanticError("v0.1 matrix row is malformed")
        identifier = row["id"]
        if identifier in removed:
            selected = [
                replacement
                for replacement in replacements
                if type(replacement) is dict
                and type(replacement.get("id")) is str
                and replacement["id"].startswith(identifier)
            ]
            if not selected:
                raise SemanticError("v0.2 replacement group is absent")
            effective.extend(selected)
            used_replacements.update(str(replacement["id"]) for replacement in selected)
        else:
            enriched = retained_by_id.get(identifier)
            if enriched is None:
                raise SemanticError("v0.2 retained row does not match v0.1 order")
            effective.append(enriched)
    if len(effective) != 63 or len(used_replacements) != 20:
        raise SemanticError("effective v0.2 matrix did not reconstruct to 63 rows")
    for version, key, expected_base, added, total in (
        (3, "v0_3_additional_rows", 63, 34, 97),
        (4, "v0_4_additional_rows", 97, 14, 111),
        (5, "v0_5_additional_rows", 111, 4, 115),
    ):
        value = _object(design, _path(version, f"build-runtime-materialization-mutation-matrix-v0.{version}.json"))
        rows = value.get(key)
        if (
            type(rows) is not list
            or value.get("base_effective_row_count") != expected_base
            or len(rows) != added
            or value.get("effective_row_count") != total
        ):
            raise SemanticError(f"v0.{version} matrix composition differs")
        if version == 4 and value.get("base_matrix_sha256") != "965606a860409dc6810ffd7b969d9eb77de0f23aae0dcc49130a8145767f5685":
            raise SemanticError("v0.4 matrix predecessor pin differs")
        if version == 5 and value.get("base_matrix_sha256") != _V04_MATRIX_SHA256:
            raise SemanticError("v0.5 matrix predecessor pin differs")
        effective.extend(rows)
    identifiers = [row.get("id") for row in effective]
    if len(effective) != 115 or any(type(value) is not str for value in identifiers) or len(set(identifiers)) != 115:
        raise SemanticError("effective v0.5 matrix IDs are not 115 unique strings")
    if not all(_failure_suffix_matches(row) for row in effective):
        raise SemanticError("effective matrix failure suffix differs from output-created bit")
    return tuple(MappingProxyType(dict(row)) for row in effective)


def _resources(design: AuthenticatedDesign) -> Mapping[str, int]:
    candidates: list[object] = []
    for version in (1, 2, 4):
        interface = _object(design, _path(version, f"build-runtime-materialization-interface-map-v0.{version}.json"))
        schema = _object(design, _path(version, f"build-runtime-materialization-profile-v0.{version}.schema.json"))
        candidates.extend((interface.get("resource_limits"), _property_const(schema, "resource_limits")))
    first = candidates[0]
    if type(first) is not dict or len(first) != 12 or any(value != first for value in candidates[1:]):
        raise SemanticError("twelve-field resource limits do not match across retained authorities")
    if any(type(key) is not str or type(value) is not int or type(value) is bool or value <= 0 for key, value in first.items()):
        raise SemanticError("resource limit type is invalid")
    return MappingProxyType(dict(first))


@dataclass(frozen=True)
class EffectiveDesign:
    relations: tuple[str, ...]
    relations_sha256: str
    publication_policy: Mapping[str, object]
    publication_policy_sha256: str
    mutation_rows: tuple[Mapping[str, object], ...]
    resource_limits: Mapping[str, int]


def validate_effective_design(design: AuthenticatedDesign) -> EffectiveDesign:
    design.require_authenticated()
    relations = _relation_inventory(design)
    policy = _policy(design)
    matrix = _effective_matrix(design)
    resources = _resources(design)
    return EffectiveDesign(relations, _RELATION_SHA256, policy, _POLICY_SHA256, matrix, resources)
