from __future__ import annotations

from typing import Protocol

from cs2_guard.models import MatchTelemetry, Signal


class Detector(Protocol):
    name: str

    def analyze(self, match: MatchTelemetry) -> Signal:
        ...
