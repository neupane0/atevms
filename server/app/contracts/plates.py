"""Plate text normalization and validation.

OCR output is UNTRUSTED input (printed plates and signs can carry arbitrary text).
Everything here fails closed: unknown tokens raise PlateFormatError.

TODO(verify): every mapping table below must be checked against official DoTM plate
specifications and real plates before field use. They are a working baseline only.
"""

from __future__ import annotations

import re
import unicodedata

MAX_RAW_LEN = 40

# Characters allowed in raw OCR text: Devanagari block, ASCII alphanumerics, space, dot, hyphen.
RAW_ALLOWED_RE = re.compile(r"^[\u0900-\u097F A-Za-z0-9.\-]+$")
# Output format of the normalized plate (uppercase ASCII tokens joined by hyphens).
NORMALIZED_PLATE_RE = re.compile(r"^[A-Z0-9]{1,14}(-[A-Z0-9]{1,14}){1,7}$")
# Plain tokens (letters/digits read from a plate) are short; long tokens must be known province words.
MAX_PLAIN_TOKEN_LEN = 5
MAX_NORMALIZED_LEN = 48

_DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_INVISIBLE = dict.fromkeys([0x200B, 0x200C, 0x200D, 0xFEFF])  # zero-width chars
_SPLIT_RE = re.compile(r"[\s.\-]+")
_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

# TODO(verify): zonal codes and vehicle-letter codes.
ZONE_CODES = {
    "बा": "BA",
    "को": "KO",
    "सा": "SA",
    "ज": "JA",
    "ना": "NA",
    "लु": "LU",
    "रा": "RA",
    "भे": "BHE",
    "क": "KA",
    "म": "MA",
    "मे": "ME",
    "ग": "GA",
}
LETTER_CODES = {
    "क": "KA",
    "ख": "KHA",
    "ग": "GA",
    "घ": "GHA",
    "च": "CHA",
    "छ": "CHHA",
    "ज": "JA",
    "झ": "JHA",
    "प": "PA",
    "फ": "PHA",
    "ब": "BA",
    "भ": "BHA",
    "म": "MA",
    "य": "YA",
    "र": "RA",
    "ल": "LA",
    "व": "VA",
    "स": "SA",
}
# TODO(verify): provincial plate words.
PROVINCE_WORDS = {
    "प्रदेश": "PRADESH",
    "कोशी": "KOSHI",
    "मधेश": "MADHESH",
    "बागमती": "BAGMATI",
    "गण्डकी": "GANDAKI",
    "लुम्बिनी": "LUMBINI",
    "कर्णाली": "KARNALI",
    "सुदूरपश्चिम": "SUDURPASHCHIM",
}
_TOKEN_MAP = {**LETTER_CODES, **ZONE_CODES, **PROVINCE_WORDS}
_KNOWN_LONG_TOKENS = frozenset(PROVINCE_WORDS.values())


class PlateFormatError(ValueError):
    """Raised when plate text is malformed or cannot be normalized safely."""


def clean_raw(raw: str) -> str:
    """NFC-normalize, strip zero-width chars, enforce length and allowed charset."""
    if not isinstance(raw, str):
        raise PlateFormatError("plate text must be a string")
    text = unicodedata.normalize("NFC", raw).translate(_INVISIBLE).strip()
    if not text or len(text) > MAX_RAW_LEN:
        raise PlateFormatError("plate text empty or too long")
    if not RAW_ALLOWED_RE.fullmatch(text):
        raise PlateFormatError("plate text contains disallowed characters")
    return text


def detect_script(raw: str) -> str:
    """Return a ScriptType value: DEVNAGARI_ZONAL, DEVNAGARI_PROVINCIAL, ENGLISH or UNKNOWN."""
    text = clean_raw(raw)
    if not _DEVANAGARI_RE.search(text):
        return "ENGLISH"
    if "प्रदेश" in text or any(w in text for w in PROVINCE_WORDS if w != "प्रदेश"):
        return "DEVNAGARI_PROVINCIAL"
    return "DEVNAGARI_ZONAL"


def normalize_plate(raw: str) -> str:
    """Convert raw plate text to normalized form, e.g. 'बा. २ च १२३४' -> 'BA-2-CHA-1234'."""
    text = clean_raw(raw).translate(_DEVANAGARI_DIGITS)
    tokens = [t for t in _SPLIT_RE.split(text) if t]
    out: list[str] = []
    for tok in tokens:
        if tok.isascii() and tok.isalnum():
            if len(tok) > MAX_PLAIN_TOKEN_LEN:
                raise PlateFormatError("plate token too long")
            out.append(tok.upper())
        elif tok in _TOKEN_MAP:
            out.append(_TOKEN_MAP[tok])
        else:
            raise PlateFormatError("unmapped plate token")
    normalized = "-".join(out)
    if not is_valid_normalized(normalized):
        raise PlateFormatError("normalized plate has invalid format")
    return normalized


def is_valid_normalized(value: str) -> bool:
    if len(value) > MAX_NORMALIZED_LEN or not NORMALIZED_PLATE_RE.fullmatch(value):
        return False
    return all(len(t) <= MAX_PLAIN_TOKEN_LEN or t in _KNOWN_LONG_TOKENS for t in value.split("-"))
