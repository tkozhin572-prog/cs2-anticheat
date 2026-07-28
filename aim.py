from __future__ import annotations

from cs2_guard.math_utils import clamp, safe_mean
from cs2_guard.models import MatchTelemetry, Signal


class SnapAimDetector:
    name = "snap_aim"

    def analyze(self, match: MatchTelemetry) -> Signal:
        snaps = [
            shot for shot in match.shots
            if shot.aim_delta_deg >= 22
            and shot.aim_duration_ms <= 130
            and shot.hit
        ]
        snap_ratio = len(snaps) / len(match.shots)
        speeds = [
            shot.aim_delta_deg / (shot.aim_duration_ms / 1000)
            for shot in snaps
        ]
        score = clamp((snap_ratio - 0.06) / 0.34)
        return Signal(
            name=self.name,
            score=score,
            reason="Много быстрых точных переводов прицела на большой угол.",
            evidence={
                "snap_ratio": round(snap_ratio, 4),
                "average_snap_speed_deg_s": round(safe_mean(speeds), 2),
                "sample_size": len(snaps),
            },
        )


class CrosshairPlacementDetector:
    name = "crosshair_placement"

    def analyze(self, match: MatchTelemetry) -> Signal:
        hits = [shot for shot in match.shots if shot.hit]
        very_close = [
            shot for shot in hits
            if shot.crosshair_distance_before_shot <= 1.15 and shot.aim_duration_ms <= 90
        ]
        ratio = len(very_close) / len(hits) if hits else 0.0
        sample_factor = clamp(len(hits) / 30)
        score = clamp((ratio - 0.28) / 0.52) * sample_factor
        return Signal(
            name=self.name,
            score=score,
            reason="Перед выстрелом прицел слишком часто уже почти идеально на цели.",
            evidence={
                "perfect_pre_aim_ratio": round(ratio, 4),
                "hit_sample_size": len(hits),
            },
        )
