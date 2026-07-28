from cs2_guard.engine import GuardEngine
from cs2_guard.models import MatchTelemetry, ShotEvent


def make_match(suspicious: bool) -> MatchTelemetry:
    shots: list[ShotEvent] = []
    for i in range(45):
        if suspicious:
            reaction = 82 + i % 3
            aim_delta = 35.0
            aim_duration = 60
            hit = True
            headshot = i < 38
            recoil = 0.2 + (i % 2) * 0.02
            movement = 220
            crosshair = 0.7
        else:
            reaction = 175 + (i * 19) % 210
            aim_delta = 4 + (i % 8) * 2.5
            aim_duration = 165 + (i % 7) * 30
            hit = i % 3 != 0
            headshot = i % 8 == 0
            recoil = 1.4 + (i % 5) * 0.35
            movement = 90 + (i % 5) * 25
            crosshair = 5 + (i % 6) * 2

        shots.append(
            ShotEvent(
                timestamp_ms=i * 650,
                target_visible_ms=180,
                reaction_ms=reaction,
                aim_delta_deg=aim_delta,
                aim_duration_ms=aim_duration,
                hit=hit,
                headshot=headshot,
                recoil_error_deg=recoil,
                movement_speed=movement,
                crosshair_distance_before_shot=crosshair,
            )
        )
    return MatchTelemetry(
        player_id="p",
        match_id="m",
        map_name="de_mirage",
        rank_group="sample",
        kills=25 if suspicious else 12,
        deaths=5 if suspicious else 17,
        assists=3,
        rounds_played=24,
        shots=shots,
    )


def test_high_risk() -> None:
    result = GuardEngine().analyze(make_match(True))
    assert result.verdict == "high_risk"
    assert result.risk_score >= 70


def test_low_risk() -> None:
    result = GuardEngine().analyze(make_match(False))
    assert result.verdict == "low_risk"
    assert result.risk_score < 40
