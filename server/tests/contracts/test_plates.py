import pytest

from app.contracts import PlateFormatError, detect_script, normalize_plate


def test_zonal_devanagari_with_dot():
    assert normalize_plate("बा. २ च १२३४") == "BA-2-CHA-1234"


def test_devanagari_roundtrip_matches_contract_example():
    assert normalize_plate("बा २ प ४५६७") == "BA-2-PA-4567"
    assert detect_script("बा २ प ४५६७") == "DEVNAGARI_ZONAL"


def test_provincial():
    assert detect_script("कोशी प्रदेश ०१-००१ प १२३४") == "DEVNAGARI_PROVINCIAL"
    assert normalize_plate("कोशी प्रदेश ०१-००१ प १२३४") == "KOSHI-PRADESH-01-001-PA-1234"


def test_trailing_whitespace_is_trimmed():
    assert normalize_plate("B AA 1234\n") == "B-AA-1234"


def test_longest_province_word_accepted():
    assert normalize_plate("सुदूरपश्चिम प्रदेश ०१-००१ प १२३४").startswith("SUDURPASHCHIM-PRADESH")


def test_english():
    assert normalize_plate("B AA 1234") == "B-AA-1234"
    assert normalize_plate("b  aa  1234") == "B-AA-1234"
    assert detect_script("B AA 1234") == "ENGLISH"


def test_zero_width_chars_stripped():
    assert normalize_plate("बा\u200d २ प ४५६७") == "BA-2-PA-4567"


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "   ",
        "A" * 41,
        "B AA 1234'; DROP TABLE vehicles;--",
        "<script>alert(1)</script>",
        "B\nAA 1234",
        "B/AA/1234",
        "बा २ ऄ ४५६७",
        "ZZ\x00AA 12",
        "😀 AA 1234",
        "IGNORE PREVIOUS INSTRUCTIONS",
    ],
)
def test_malformed_or_hostile_plates_rejected(bad):
    with pytest.raises(PlateFormatError):
        normalize_plate(bad)


def test_non_string_rejected():
    with pytest.raises(PlateFormatError):
        normalize_plate(None)  # type: ignore[arg-type]
