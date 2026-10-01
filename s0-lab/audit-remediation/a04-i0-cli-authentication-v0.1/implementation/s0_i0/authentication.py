"""Hash-authenticated allowlists for the frozen public-development inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from .integrity import BUNDLE_RELATIVE, parse_bundle_manifest, sha256_bytes
from .paths import resolve_workspace_path


class AuthenticationError(ValueError):
    """A path or digest is outside the frozen public input contract."""


FROZEN_BUNDLE_MANIFEST_SHA256 = "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637"
ANSWER_SCHEMA_PATH = "s0-lab/control/sm0/answer.schema.json"
ANSWER_SCHEMA_SHA256 = "e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b"

PUBLIC_CANONICALS = {
    "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/canonical-input.json": "5cdde94ea1651c2353b4f228f891859d2dbc82539ab467a129efa792a0c16be9",
    "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/canonical-input.json": "bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863",
}

PUBLIC_QUESTIONS = {
    "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0001/questions.json": "cb66e5b3c51e824e5d7c7caec1770249d2330ea3ad05e0e213c9b82fce886707",
    "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json": "661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90",
}

PUBLIC_PACKAGES = {
    "s0-lab/public-practice/v0.1/packages/P01B1MOSS001/input.json": "268d9bda5e9938b354f9e9acebb72046226a88d598a0dcd366d347e85eacb4ef",
    "s0-lab/public-practice/v0.1/packages/P01B2EMBR001/input.json": "15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7",
    "s0-lab/public-practice/v0.1/packages/P02B1MOSS001/input.json": "1e75ea5d44f6aba9048e3291b82df50b2e6e7e4c95e753c3f8aa75a7a7d09e2d",
    "s0-lab/public-practice/v0.1/packages/P02B2EMBR001/input.json": "5a87fbe35c56c0a754149ba47e5f42a7af046ebd705514cf208639caaccf3aae",
    "s0-lab/public-practice/v0.1/packages/P03B1MOSS001/input.json": "fee0bee4e25ad0a7a56974e197bf678b9aca770331d25204c1287dc087cc769c",
    "s0-lab/public-practice/v0.1/packages/P03B2EMBR001/input.json": "7785e4ece12a23fcb9f70c334bb8218fd8eb3c2bdcad2593a2a9c56b6e1a2807",
    "s0-lab/public-practice/v0.1/packages/P04B1MOSS001/input.json": "faf88e98210b41c16e9dfab915107ea506e01b1748d2522610f3ad6b875cfbcb",
    "s0-lab/public-practice/v0.1/packages/P04B2EMBR001/input.json": "a27de682b641907685db3052656c200edb866b5e3356288426bd5f0bab226af6",
}

PUBLIC_ANSWERS = {
    "s0-lab/public-practice/v0.1/examples/answer.json": "e66d631210fae9519cd94e618061674f68ac869b04fc38416c8ee50a3f85b43f",
    "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json": "c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf",
}


def _relative(workspace_root: Path, path: Path) -> str:
    return path.relative_to(workspace_root.resolve(strict=True)).as_posix()


def _authenticate_bundle_manifest(workspace_root: Path) -> tuple[Path, dict[str, str]]:
    bundle_root = (workspace_root / BUNDLE_RELATIVE).resolve(strict=True)
    raw = (bundle_root / "bundle-files.sha256").read_bytes()
    if sha256_bytes(raw) != FROZEN_BUNDLE_MANIFEST_SHA256:
        raise AuthenticationError("frozen public bundle manifest hash mismatch")
    return bundle_root, parse_bundle_manifest(bundle_root)


def authenticate_public_file(
    workspace_root: Path, value: str | Path, allowlist: Mapping[str, str]
) -> Path:
    path = resolve_workspace_path(workspace_root, value)
    relative = _relative(workspace_root, path)
    expected = allowlist.get(relative)
    if expected is None:
        raise AuthenticationError("path is not in the approved frozen public allowlist")
    bundle_root, manifest = _authenticate_bundle_manifest(workspace_root)
    bundle_relative = path.relative_to(bundle_root).as_posix()
    if manifest.get(bundle_relative) != expected or sha256_bytes(path.read_bytes()) != expected:
        raise AuthenticationError("frozen public file hash mismatch")
    return path


def authenticate_answer_schema(workspace_root: Path, value: str | Path) -> Path:
    path = resolve_workspace_path(workspace_root, value)
    if _relative(workspace_root, path) != ANSWER_SCHEMA_PATH:
        raise AuthenticationError("answer schema is not the frozen approved schema")
    if sha256_bytes(path.read_bytes()) != ANSWER_SCHEMA_SHA256:
        raise AuthenticationError("frozen answer schema hash mismatch")
    return path


def authenticate_answer_candidate(workspace_root: Path, value: str | Path) -> Path:
    path = resolve_workspace_path(workspace_root, value)
    relative = _relative(workspace_root, path)
    if relative in PUBLIC_ANSWERS:
        return authenticate_public_file(workspace_root, value, PUBLIC_ANSWERS)
    candidate_root = (workspace_root / "s0-lab" / "i0").resolve(strict=True)
    try:
        path.relative_to(candidate_root)
    except ValueError as exc:
        raise AuthenticationError(
            "answer must be an approved public answer or an untrusted s0-lab/i0 candidate"
        ) from exc
    return path
