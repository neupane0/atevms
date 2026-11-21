import copy

import pytest
from pydantic import ValidationError

from app.contracts import EvidencePayload


def test_valid_payload(signed_manifest):
    p = EvidencePayload.model_validate(signed_manifest)
    assert p.anpr.plate_text_normalized == "BA-2-PA-4567"


def test_unknown_top_level_field_rejected(signed_manifest):
    signed_manifest["owner_name"] = "should never reach the edge"
    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(signed_manifest)


def test_unknown_nested_field_rejected(signed_manifest):
    signed_manifest["violation"]["extra"] = 1
    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(signed_manifest)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda m: m["gps"].update(lat=91),
        lambda m: m["gps"].update(lng=-181),
        lambda m: m["violation"].update(confidence=1.5),
        lambda m: m["anpr"].update(ocr_confidence=-0.1),
        lambda m: m["violation"].update(type="JAYWALKING"),
        lambda m: m.update(schema_version="1.0"),
        lambda m: m.update(event_id="not-a-uuid"),
        lambda m: m.update(event_id="00000000-0000-1000-8000-000000000000"),  # not v4
        lambda m: m.update(counter=-1),
        lambda m: m.update(counter="5"),
        lambda m: m.update(prev_event_hash="xyz"),
        lambda m: m.update(timestamp_utc="2026-11-21T05:35:12+05:45"),
        lambda m: m.update(timestamp_utc="2026-13-45T05:35:12Z"),
        lambda m: m.update(intersection_name="A" * 121),
        lambda m: m.update(intersection_name="bad\x00name"),
        lambda m: m.update(device_id="x"),
        lambda m: m["evidence_files"]["full_scene_img"].update(filename="../../etc/passwd"),
        lambda m: m["evidence_files"]["full_scene_img"].update(sha256="ABC"),
        lambda m: m["anpr"].update(plate_text_normalized="BA 2 PA"),
        lambda m: m["anpr"].update(plate_text_raw="<script>alert(1)</script>"),
        lambda m: m["anpr"].update(plate_text_normalized="BA-2-PA-4567'; DROP TABLE x;--"),
        lambda m: m["violation"].update(measured_speed_kmh=-5),
        lambda m: m.pop("manifest_signature"),
        lambda m: m["evidence_files"].pop("violation_clip_mp4"),
    ],
)
def test_invalid_payloads_rejected(signed_manifest, mutate):
    m = copy.deepcopy(signed_manifest)
    mutate(m)
    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(m)


def test_model_is_immutable(signed_manifest):
    p = EvidencePayload.model_validate(signed_manifest)
    with pytest.raises(ValidationError):
        p.counter = 5  # type: ignore[misc]
