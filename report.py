from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from cs2_guard.models import AnalysisResult


@dataclass(frozen=True)
class ReportSummary:
    total: int
    low_risk: int
    review: int
    high_risk: int
    average_score: float


def summarize(results: list[AnalysisResult]) -> ReportSummary:
    verdicts = Counter(result.verdict for result in results)
    avg = sum(result.risk_score for result in results) / len(results) if results else 0.0
    return ReportSummary(
        total=len(results),
        low_risk=verdicts["low_risk"],
        review=verdicts["review"],
        high_risk=verdicts["high_risk"],
        average_score=round(avg, 2),
    )
