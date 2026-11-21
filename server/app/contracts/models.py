"""Pydantic models for the Violation Evidence Payload v1.1 (see .context/03_CONTRACTS.md).

Order of operations on ingestion: load_manifest -> verify_manifest (raw dict) -> EvidencePayload.model_validate.
All models forbid unknown fields.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from enum import Enum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    StringConstraints,
    field_validator,
)

from .plates import RAW_ALLOWED_RE, is_valid_normalized

SCHEMA_VERSION = "1.1"

Sha256Hex = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
SignatureHex = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{128}$")]
DeviceId = Annotated[str, StringConstraints(pattern=r"^[A-Z0-9][A-Z0-9_-]{2,63}$")]
Filename = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")]
Confidence = Annotated[float, Field(ge=0.0, le=1.0)]


class ViolationType(str, Enum):
    RED_LIGHT_JUMP = "RED_LIGHT_JUMP"  # only active type in Phase 0
    OVER_SPEED = "OVER_SPEED"
    NO_HELMET = "NO_HELMET"
    WRONG_WAY = "WRONG_WAY"


class SignalState(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    UNKNOWN = "UNKNOWN"


class VehicleClass(str, Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    BUS = "BUS"
    TRUCK = "TRUCK"
    THREE_WHEELER = "THREE_WHEELER"


class ScriptType(str, Enum):
    DEVNAGARI_ZONAL = "DEVNAGARI_ZONAL"
    DEVNAGARI_PROVINCIAL = "DEVNAGARI_PROVINCIAL"
    ENGLISH = "ENGLISH"
    UNKNOWN = "UNKNOWN"


class PlateColor(str, Enum):
    # TODO(verify): confirm the official colour scheme with DoTM before relying on these.
    UNKNOWN = "UNKNOWN"
    WHITE_BLACK = "WHITE_BLACK"
    BLACK_WHITE = "BLACK_WHITE"
    RED_WHITE = "RED_WHITE"
    GREEN_WHITE = "GREEN_WHITE"
    BLUE_WHITE = "BLUE_WHITE"
    YELLOW_BLACK = "YELLOW_BLACK"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Gps(StrictModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lng: float = Field(ge=-180.0, le=180.0)


class Violation(StrictModel):
    type: ViolationType
    measured_speed_kmh: float | None = Field(default=None, ge=0.0, le=300.0)  # null in Phase 0
    speed_limit_kmh: float | None = Field(default=None, ge=0.0, le=200.0)  # null in Phase 0
    vehicle_class: VehicleClass
    confidence: Confidence


class Anpr(StrictModel):
    plate_text_raw: Annotated[str, StringConstraints(min_length=1, max_length=40)]
    plate_text_normalized: Annotated[str, StringConstraints(min_length=3, max_length=48)]
    script_type: ScriptType
    plate_color: PlateColor
    ocr_confidence: Confidence

    @field_validator("plate_text_raw")
    @classmethod
    def _raw_charset(cls, v: str) -> str:
        if not RAW_ALLOWED_RE.fullmatch(unicodedata.normalize("NFC", v)):
            raise ValueError("plate_text_raw contains disallowed characters")
        return v

    @field_validator("plate_text_normalized")
    @classmethod
    def _normalized_format(cls, v: str) -> str:
        if not is_valid_normalized(v):
            raise ValueError("plate_text_normalized has invalid format")
        return v


class FileRef(StrictModel):
    filename: Filename
    sha256: Sha256Hex


class EvidenceFiles(StrictModel):
    full_scene_img: FileRef
    vehicle_crop_img: FileRef
    plate_crop_img: FileRef
    violation_clip_mp4: FileRef


class EvidencePayload(StrictModel):
    schema_version: Literal["1.1"]
    event_id: UUID
    device_id: DeviceId
    counter: StrictInt = Field(ge=0)
    prev_event_hash: Sha256Hex  # 64 zeros for a device's first event
    camera_id: DeviceId
    intersection_name: Annotated[str, StringConstraints(min_length=1, max_length=120)]
    gps: Gps
    timestamp_utc: str
    signal_state: SignalState
    violation: Violation
    anpr: Anpr
    evidence_files: EvidenceFiles
    manifest_signature: SignatureHex

    @field_validator("event_id")
    @classmethod
    def _uuid4(cls, v: UUID) -> UUID:
        if v.version != 4:
            raise ValueError("event_id must be a UUID v4")
        return v

    @field_validator("intersection_name")
    @classmethod
    def _no_control_chars(cls, v: str) -> str:
        if any(unicodedata.category(c).startswith("C") for c in v):
            raise ValueError("control characters not allowed")
        return v

    @field_validator("timestamp_utc")
    @classmethod
    def _utc_timestamp(cls, v: str) -> str:
        # Kept as a string so the signed bytes are never altered by re-serialization.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z", v):
            raise ValueError("timestamp_utc must be ISO-8601 UTC ending in 'Z'")
        try:
            datetime.fromisoformat(v)
        except ValueError as exc:
            raise ValueError("timestamp_utc is not a valid datetime") from exc
        return v
