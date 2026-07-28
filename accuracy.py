from __future__ import annotations

from cs2_guard.math_utils import clamp, population_std, safe_mean
from cs2_guard.models import MatchTelemetry, Signal


class HeadshotRatioDetector:
    name = "headshot_ratio"

    def analyze(self, match: MatchTelemetry) -> Signal:
        hits = [shot for shot in match.shots if shot.hit]
        headshots = [shot for shot in hits if shot.headshot]
        hs_ratio = len(headshots) / len(hits) if hits else 0.0
        sample_factor = clamp(len(hits) / 35)
        score = clamp((hs_ratio - 0.58) / 0.35) * sample_factor
        return Signal(
            name=self.name,
            score=score,
            reason="Доля хедшотов слишком высокая для выборки.",
            evidence={
                "headshot_ratio": round(hs_ratio, 4),
                "hit_sample_size": len(hits),
            },
        )


class RecoilConsistencyDetector:
    name = "recoil_consistency"

    def analyze(self, match: MatchTelemetry) -> Signal:
        errors = [float(shot.recoil_error_deg) for shot in match.shots if shot.hit]
        avg = safe_mean(errors)
        std = population_std(errors)
        sample_factor = clamp(len(errors) / 25)
        score = (
            clamp((1.25 - avg) / 1.05) * 0.6
            + clamp((0.7 - std) / 0.55) * 0.4
        ) * sample_factor
        return Signal(
            name=self.name,
            score=clamp(score),
            reason="Компенсация отдачи слишком точная и стабильная.",
            evidence={
                "average_recoil_error_deg": round(avg, 3),
                "recoil_std_deg": round(std, 3),
                "sample_size": len(errors),
            },
        )
