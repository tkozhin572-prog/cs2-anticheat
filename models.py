from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ShotEvent(BaseModel):
    timestamp_ms: int = Field(ge=0)
    target_visible_ms: int = Field(ge=0)
    reaction_ms: int = Field(ge=0, le=5000)
    aim_delta_deg: float = Field(ge=0, le=180)
    aim_duration_ms: int = Field(ge=1, le=5000)
    hit: bool
    headshot: bool
    recoil_error_deg: float = Field(ge=0, le=180)
    movement_speed: float = Field(ge=0, le=1000)
    crosshair_distance_before_shot: float = Field(ge=0, le=180)


class MatchTelemetry(BaseModel):
    player_id: str = Field(min_length=1, max_length=128)
    match_id: str = Field(min_length=1, max_length=128)
    map_name: str = Field(default="unknown", max_length=64)
    rank_group: str = Field(default="unknown", max_length=64)
    kills: int = Field(ge=0)
    deaths: int = Field(ge=0)
    assists: int = Field(ge=0)
    rounds_played: int = Field(ge=1, le=100)
    shots: list[ShotEvent] = Field(min_length=1)

    @field_validator("shots")
    @classmethod
    def timestamps_must_be_sorted(cls, shots: list[ShotEvent]) -> list[ShotEvent]:
        timestamps = [shot.timestamp_ms for shot in shots]
        if timestamps != sorted(timestamps):
            raise ValueError("shot timestamps must be sorted")
        return shots


class Signal(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)
    reason: str
    evidence: dict[str, float | int | str]


class AnalysisResult(BaseModel):
    player_id: str
    match_id: str
    map_name: str
    rank_group: str
    risk_score: float = Field(ge=0, le=100)
    verdict: str
    signals: list[Signal]
    recommendation: str
