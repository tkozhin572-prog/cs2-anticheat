from __future__ import annotations

from cs2_guard.math_utils import clamp, safe_mean
from cs2_guard.models import MatchTelemetry, Signal


class MovingAccuracyDetector:
    name = "moving_accuracy"

    def analyze(self, match: MatchTelemetry) -> Signal:
        moving_shots = [shot for shot in match.shots if shot.movement_speed >= 190]
        moving_hits = [shot for shot in moving_shots if shot.hit]
        moving_hs = [shot for shot in moving_hits if shot.headshot]

        hit_ratio = len(moving_hits) / len(moving_shots) if moving_shots else 0.0
        hs_ratio = len(moving_hs) / len(moving_hits) if moving_hits else 0.0
        sample_factor = clamp(len(moving_shots) / 25)
        score = (clamp((hit_ratio - 0.42) / 0.4) * 0.6 + clamp((hs_ratio - 0.45) / 0.4) * 0.4) * sample_factor

        return Signal(
            name=self.name,
            score=clamp(score),
            reason="Необычно высокая точность при активном движении.",
            evidence={
                "moving_shots": len(moving_shots),
                "moving_hit_ratio": round(hit_ratio, 4),
                "moving_headshot_ratio": round(hs_ratio, 4),
                "average_movement_speed": round(safe_mean([s.movement_speed for s in moving_shots]), 2),
            },
        )
