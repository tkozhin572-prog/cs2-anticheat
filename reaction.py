from __future__ import annotations

from cs2_guard.math_utils import clamp, population_std, safe_mean
from cs2_guard.models import MatchTelemetry, Signal


class FastReactionDetector:
    name = "fast_reaction"

    def analyze(self, match: MatchTelemetry) -> Signal:
        reactions = [
            float(shot.reaction_ms)
            for shot in match.shots
            if shot.target_visible_ms > 0 and shot.hit
        ]
        fast_count = sum(value < 115 for value in reactions)
        fast_ratio = fast_count / len(reactions) if reactions else 0.0
        score = clamp((fast_ratio - 0.12) / 0.48)
        return Signal(
            name=self.name,
            score=score,
            reason="Слишком много попаданий с реакцией быстрее нормального диапазона.",
            evidence={
                "average_reaction_ms": round(safe_mean(reactions), 2),
                "reaction_std_ms": round(population_std(reactions), 2),
                "fast_ratio": round(fast_ratio, 4),
                "sample_size": len(reactions),
            },
        )


class ReactionConsistencyDetector:
    name = "reaction_consistency"

    def analyze(self, match: MatchTelemetry) -> Signal:
        reactions = [
            float(shot.reaction_ms)
            for shot in match.shots
            if shot.target_visible_ms > 0 and shot.hit
        ]
        std = population_std(reactions)
        sample_factor = clamp(len(reactions) / 24)
        score = clamp((35.0 - std) / 25.0) * sample_factor
        return Signal(
            name=self.name,
            score=score,
            reason="Реакция слишком одинаковая на большой выборке.",
            evidence={
                "reaction_std_ms": round(std, 2),
                "sample_size": len(reactions),
            },
        )
