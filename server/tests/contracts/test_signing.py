import copy
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.contracts import (
    HashMismatchError,
    MalformedManifestError,
    SignatureVerificationError,
    canonical_json,
    load_manifest,
    manifest_hash,
    sha256_file,
    sign_manifest,
    verify_file_sha256,
    verify_manifest,
)


def test_valid_signature_verifies(signed_manifest, private_key):
    verify_manifest(signed_manifest, private_key.public_key())


def test_signature_stable_across_key_order(unsigned_manifest, private_key):
    reordered = dict(reversed(list(unsigned_manifest.items())))
    assert sign_manifest(unsigned_manifest, private_key) == sign_manifest(reordered, private_key)


def test_signature_field_excluded_from_canonical(signed_manifest, unsigned_manifest):
    assert canonical_json(signed_manifest) == canonical_json(unsigned_manifest)


def test_canonical_keeps_devanagari_as_utf8(unsigned_manifest):
    assert "बा".encode() in canonical_json(unsigned_manifest)


@pytest.mark.parametrize(
    "path",
    [
        ("counter",),
        ("signal_state",),
        ("anpr", "plate_text_raw"),
        ("evidence_files", "plate_crop_img", "sha256"),
    ],
)
def test_tampered_field_fails(signed_manifest, private_key, path):
    m = copy.deepcopy(signed_manifest)
    node = m
    for k in path[:-1]:
        node = node[k]
    node[path[-1]] = "TAMPERED" if path[-1] != "counter" else 999
    with pytest.raises(SignatureVerificationError):
        verify_manifest(m, private_key.public_key())


def test_wrong_key_fails(signed_manifest):
    with pytest.raises(SignatureVerificationError):
        verify_manifest(signed_manifest, Ed25519PrivateKey.generate().public_key())


@pytest.mark.parametrize("sig", [None, "", "zz", "a" * 127, "A" * 128, 123])
def test_missing_or_malformed_signature_fails(signed_manifest, private_key, sig):
    m = copy.deepcopy(signed_manifest)
    m["manifest_signature"] = sig
    with pytest.raises(SignatureVerificationError):
        verify_manifest(m, private_key.public_key())


def test_manifest_hash_changes_on_edit(unsigned_manifest):
    h1 = manifest_hash(unsigned_manifest)
    m = copy.deepcopy(unsigned_manifest)
    m["counter"] = 2
    assert h1 != manifest_hash(m) and len(h1) == 64


def test_load_manifest_rejects_duplicate_keys():
    with pytest.raises(MalformedManifestError):
        load_manifest(b'{"counter": 1, "counter": 2}')


@pytest.mark.parametrize("raw", [b"[]", b"not json", b"\xff\xfe", b'{"x": NaN}', b'{"x": Infinity}'])
def test_load_manifest_rejects_bad_input(raw):
    with pytest.raises(MalformedManifestError):
        load_manifest(raw)


def test_load_manifest_roundtrip(signed_manifest, private_key):
    loaded = load_manifest(json.dumps(signed_manifest, ensure_ascii=False).encode("utf-8"))
    verify_manifest(loaded, private_key.public_key())


def test_file_hash_ok_and_tampered(tmp_path):
    f = tmp_path / "scene.jpg"
    f.write_bytes(b"evidence-bytes")
    good = sha256_file(f)
    verify_file_sha256(f, good)
    f.write_bytes(b"evidence-bytez")
    with pytest.raises(HashMismatchError):
        verify_file_sha256(f, good)


@pytest.mark.parametrize("bad", ["", "abc", "G" * 64, None])
def test_malformed_expected_hash_rejected(tmp_path, bad):
    f = tmp_path / "x"
    f.write_bytes(b"1")
    with pytest.raises(HashMismatchError):
        verify_file_sha256(f, bad)  # type: ignore[arg-type]
