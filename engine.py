from __future__ import annotations

from cs2_guard.detectors import DEFAULT_DETECTORS
from cs2_guard.models import AnalysisResult, MatchTelemetry, Signal


class GuardEngine:
    WEIGHTS = {
        "fast_reaction": 0.18,
        "reaction_consistency": 0.14,
        "snap_aim": 0.20,
        "crosshair_placement": 0.12,
        "headshot_ratio": 0.10,
        "recoil_consistency": 0.16,
        "moving_accuracy": 0.10,
    }

    def analyze(self, match: MatchTelemetry) -> AnalysisResult:
        signals: list[Signal] = [detector.analyze(match) for detector in DEFAULT_DETECTORS]
        score = sum(signal.score * self.WEIGHTS.get(signal.name, 0.0) for signal in signals)
        risk_score = round(score * 100, 2)
        verdict, recommendation = self._verdict(risk_score, signals)

        return AnalysisResult(
            player_id=match.player_id,
            match_id=match.match_id,
            map_name=match.map_name,
            rank_group=match.rank_group,
            risk_score=risk_score,
            verdict=verdict,
            signals=signals,
            recommendation=recommendation,
        )

    @staticmethod
    def _verdict(risk_score: float, signals: list[Signal]) -> tuple[str, str]:
        strong = sum(signal.score >= 0.65 for signal in signals)
        medium = sum(signal.score >= 0.40 for signal in signals)

        if risk_score >= 70 and strong >= 2:
            return "high_risk", "Ручная проверка + сравнение с несколькими матчами игрока."
        if risk_score >= 40 or medium >= 3:
            return "review", "Собрать больше матчей и проверить демо вручную."
        return "low_risk", "Сильных признаков не найдено."
