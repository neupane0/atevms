import copy
import uuid

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.contracts import GENESIS_HASH, sign_manifest


@pytest.fixture
def private_key():
    return Ed25519PrivateKey.generate()


@pytest.fixture
def unsigned_manifest():
    return {
        "schema_version": "1.1",
        "event_id": str(uuid.uuid4()),
        "device_id": "KTM-KOTESHWOR-CAM-01",
        "counter": 1,
        "prev_event_hash": GENESIS_HASH,
        "camera_id": "KTM-KOTESHWOR-CAM-01",
        "intersection_name": "Koteshwor Chowk Northbound",
        "gps": {"lat": 27.6781, "lng": 85.3492},
        "timestamp_utc": "2026-11-21T05:35:12.450Z",
        "signal_state": "RED",
        "violation": {
            "type": "RED_LIGHT_JUMP",
            "measured_speed_kmh": None,
            "speed_limit_kmh": None,
            "vehicle_class": "MOTORCYCLE",
            "confidence": 0.94,
        },
        "anpr": {
            "plate_text_raw": "बा २ प ४५६७",
            "plate_text_normalized": "BA-2-PA-4567",
            "script_type": "DEVNAGARI_ZONAL",
            "plate_color": "UNKNOWN",
            "ocr_confidence": 0.91,
        },
        "evidence_files": {
            "full_scene_img": {"filename": "scene.jpg", "sha256": "a" * 64},
            "vehicle_crop_img": {"filename": "vehicle.jpg", "sha256": "b" * 64},
            "plate_crop_img": {"filename": "plate.jpg", "sha256": "c" * 64},
            "violation_clip_mp4": {"filename": "clip.mp4", "sha256": "d" * 64},
        },
    }


@pytest.fixture
def signed_manifest(unsigned_manifest, private_key):
    m = copy.deepcopy(unsigned_manifest)
    m["manifest_signature"] = sign_manifest(m, private_key)
    return m
