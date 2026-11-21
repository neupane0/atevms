"""Canonical JSON, SHA-256 helpers and Ed25519 manifest signing/verification.

Fail closed: any problem raises a ContractError subclass. Never catch and ignore these.
Uses only the `cryptography` library (no hand-rolled crypto).

Limitation: canonical JSON relies on Python's deterministic float repr. Edge and server are
both Python in Phase 0. Revisit (e.g. RFC 8785) if a non-Python signer is introduced.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

SIGNATURE_FIELD = "manifest_signature"
GENESIS_HASH = "0" * 64  # prev_event_hash of the first event of a device
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SIG_RE = re.compile(r"^[0-9a-f]{128}$")
_CHUNK = 1 << 20


class ContractError(Exception):
    """Base class for contract/integrity failures."""


class MalformedManifestError(ContractError):
    pass


class SignatureVerificationError(ContractError):
    pass


class HashMismatchError(ContractError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise MalformedManifestError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(name: str) -> Any:
    raise MalformedManifestError(f"non-finite number not allowed: {name}")


def load_manifest(raw: bytes) -> dict[str, Any]:
    """Parse untrusted JSON bytes. Rejects duplicate keys, NaN/Infinity and non-objects."""
    try:
        text = raw.decode("utf-8")
        obj = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MalformedManifestError("manifest is not valid UTF-8 JSON") from exc
    if not isinstance(obj, dict):
        raise MalformedManifestError("manifest must be a JSON object")
    return obj


def canonical_json(manifest: Mapping[str, Any]) -> bytes:
    """Sorted keys, no whitespace, UTF-8, excluding manifest_signature."""
    body = {k: v for k, v in manifest.items() if k != SIGNATURE_FIELD}
    try:
        return json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise MalformedManifestError("manifest cannot be canonicalized") from exc


def manifest_hash(manifest: Mapping[str, Any]) -> str:
    """SHA-256 of the canonical manifest. Used as the next event's prev_event_hash."""
    return hashlib.sha256(canonical_json(manifest)).hexdigest()


def sign_manifest(manifest: Mapping[str, Any], private_key: Ed25519PrivateKey) -> str:
    return private_key.sign(canonical_json(manifest)).hex()


def verify_manifest(manifest: Mapping[str, Any], public_key: Ed25519PublicKey) -> None:
    """Raise SignatureVerificationError unless the signature is valid for this manifest."""
    signature = manifest.get(SIGNATURE_FIELD)
    if not isinstance(signature, str) or not _SIG_RE.fullmatch(signature):
        raise SignatureVerificationError("missing or malformed signature")
    try:
        public_key.verify(bytes.fromhex(signature), canonical_json(manifest))
    except InvalidSignature as exc:
        raise SignatureVerificationError("signature does not match manifest") from exc


def sha256_file(path: str | Path) -> str:
    """Streaming SHA-256 of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file_sha256(path: str | Path, expected: str) -> None:
    """Constant-time comparison of a file's hash with the manifest value."""
    if not isinstance(expected, str) or not _SHA256_RE.fullmatch(expected):
        raise HashMismatchError("expected hash is malformed")
    if not hmac.compare_digest(sha256_file(path), expected):
        raise HashMismatchError("file hash does not match manifest")
