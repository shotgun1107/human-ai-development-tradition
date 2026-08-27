"""Bounded weak-identity issuance registries for candidate v0.1."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from threading import RLock
from typing import TypeAlias
from weakref import ReferenceType, ref


Snapshot: TypeAlias = tuple[object, ...]
CanonicalSnapshot: TypeAlias = tuple[object, ...]


def make_bounded_issuance_registry(
    *,
    limits: Mapping[str, int],
    snapshot: Callable[[object], Snapshot],
    materialize: Callable[[object], object],
    error_type: type[Exception],
    capacity_error: str,
    invalid_kind_error: str,
    not_issued_error: str,
) -> tuple[
    Callable[[object, str], object],
    Callable[[object, str], object],
    Callable[[object, str], object],
    Callable[[object, str | None], bool],
]:
    """Freeze one thread-safe, generation-checked, weak issuance registry."""

    frozen_limits = dict(limits)
    if (
        not frozen_limits
        or any(type(kind) is not str or not kind for kind in frozen_limits)
        or any(type(limit) is not int or limit < 1 for limit in frozen_limits.values())
    ):
        raise error_type("issuance_registry_configuration_invalid")
    total_limit = sum(frozen_limits.values())
    frozen_snapshot = snapshot
    frozen_materialize = materialize
    frozen_error_type = error_type
    frozen_capacity_error = capacity_error
    frozen_invalid_kind_error = invalid_kind_error
    frozen_not_issued_error = not_issued_error
    frozen_id = id
    frozen_ref = ref
    frozen_type = type
    frozen_bool_type = bool
    frozen_int_type = int
    frozen_str_type = str
    frozen_tuple_type = tuple
    frozen_tuple_length = tuple.__len__
    frozen_tuple_item = tuple.__getitem__
    frozen_tuple_equal = tuple.__eq__
    frozen_tuple_from_items = tuple
    frozen_list_append = list.append
    lock = RLock()
    entries: dict[
        int,
        tuple[int, ReferenceType[object], str, CanonicalSnapshot],
    ] = {}
    counts = {kind: 0 for kind in frozen_limits}
    next_generation = 0

    def require_kind(kind: object) -> str:
        if frozen_type(kind) is not frozen_str_type or kind not in frozen_limits:
            raise frozen_error_type(frozen_invalid_kind_error)
        return kind

    def canonicalize_value(value: object) -> CanonicalSnapshot:
        value_type = frozen_type(value)
        if value is None:
            return ("none",)
        if value_type is frozen_bool_type:
            return ("bool", value)
        if value_type is frozen_int_type:
            return ("int", value)
        if value_type is frozen_str_type:
            return ("str", value)
        if value_type is frozen_tuple_type:
            item_count = frozen_tuple_length(value)
            canonical_items: list[CanonicalSnapshot] = []
            index = 0
            while index < item_count:
                frozen_list_append(
                    canonical_items,
                    canonicalize_value(frozen_tuple_item(value, index)),
                )
                index += 1
            return ("tuple", frozen_tuple_from_items(canonical_items))
        raise frozen_error_type(frozen_not_issued_error)

    def canonicalize_snapshot(value: object) -> CanonicalSnapshot:
        if frozen_type(value) is not frozen_tuple_type:
            raise frozen_error_type(frozen_not_issued_error)
        return canonicalize_value(value)

    def snapshots_equal(left: CanonicalSnapshot, right: CanonicalSnapshot) -> bool:
        return frozen_tuple_equal(left, right) is True

    def remove_entry(key: int, entry) -> None:
        current = entries.get(key)
        if current is entry:
            del entries[key]
            counts[entry[2]] -= 1

    def issue(value: object, kind: str) -> object:
        nonlocal next_generation
        frozen_kind = require_kind(kind)
        with lock:
            key = frozen_id(value)
            prior = entries.get(key)
            if prior is not None:
                if prior[1]() is value:
                    raise frozen_error_type(frozen_not_issued_error)
                remove_entry(key, prior)
            if counts[frozen_kind] >= frozen_limits[frozen_kind] or len(entries) >= total_limit:
                raise frozen_error_type(frozen_capacity_error)
            current_snapshot = canonicalize_snapshot(frozen_snapshot(value))
            next_generation += 1
            generation = next_generation

            def release_dropped(
                reference: ReferenceType[object],
                *,
                object_id: int = key,
                issued_generation: int = generation,
            ) -> None:
                with lock:
                    entry = entries.get(object_id)
                    if (
                        entry is not None
                        and entry[0] == issued_generation
                        and entry[1] is reference
                    ):
                        remove_entry(object_id, entry)

            reference = frozen_ref(value, release_dropped)
            entries[key] = (generation, reference, frozen_kind, current_snapshot)
            counts[frozen_kind] += 1
        return value

    def require(value: object, kind: str) -> object:
        frozen_kind = require_kind(kind)
        with lock:
            key = frozen_id(value)
            entry = entries.get(key)
            snapshot_complete = False
            try:
                current_snapshot = canonicalize_snapshot(frozen_snapshot(value))
                snapshot_complete = True
            finally:
                if not snapshot_complete and entry is not None:
                    remove_entry(key, entry)
            if (
                entry is None
                or entry[1]() is not value
                or entry[2] != frozen_kind
                or not snapshots_equal(entry[3], current_snapshot)
            ):
                raise frozen_error_type(frozen_not_issued_error)
        return value

    def consume(value: object, kind: str) -> object:
        frozen_kind = require_kind(kind)
        with lock:
            key = frozen_id(value)
            entry = entries.get(key)
            try:
                if entry is None:
                    raise frozen_error_type(frozen_not_issued_error)
                retained_value = entry[1]()
                if retained_value is not value or entry[2] != frozen_kind:
                    raise frozen_error_type(frozen_not_issued_error)
                expected_snapshot = entry[3]
                current_snapshot = canonicalize_snapshot(
                    frozen_snapshot(retained_value)
                )
                if not snapshots_equal(current_snapshot, expected_snapshot):
                    raise frozen_error_type(frozen_not_issued_error)
                result = frozen_materialize(retained_value)
                if result is retained_value:
                    raise frozen_error_type(frozen_not_issued_error)
                result_snapshot = canonicalize_snapshot(frozen_snapshot(result))
                if not snapshots_equal(result_snapshot, expected_snapshot):
                    raise frozen_error_type(frozen_not_issued_error)
                final_snapshot = canonicalize_snapshot(
                    frozen_snapshot(retained_value)
                )
                if not snapshots_equal(final_snapshot, expected_snapshot):
                    raise frozen_error_type(frozen_not_issued_error)
                if entries.get(key) is not entry:
                    raise frozen_error_type(frozen_not_issued_error)
            finally:
                if entry is not None:
                    remove_entry(key, entry)
        return result

    def release(value: object, kind: str | None = None) -> bool:
        frozen_kind = None if kind is None else require_kind(kind)
        with lock:
            key = frozen_id(value)
            entry = entries.get(key)
            if (
                entry is None
                or entry[1]() is not value
                or (frozen_kind is not None and entry[2] != frozen_kind)
            ):
                return False
            remove_entry(key, entry)
            return True

    return issue, require, consume, release


__all__: tuple[str, ...] = ()
