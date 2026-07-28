from __future__ import annotations

from fastapi import FastAPI, HTTPException

from cs2_guard.engine import GuardEngine
from cs2_guard.models import AnalysisResult, MatchTelemetry
from cs2_guard.services.dataset import read_ndjson_matches

app = FastAPI(
    title="CS2 Guard",
    version="0.2.0",
    description="Safe telemetry-based anti-cheat prototype.",
)

engine = GuardEngine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
def analyze(match: MatchTelemetry) -> AnalysisResult:
    return engine.analyze(match)


@app.post("/analyze-batch", response_model=list[AnalysisResult])
def analyze_batch(matches: list[MatchTelemetry]) -> list[AnalysisResult]:
    if len(matches) > 500:
        raise HTTPException(status_code=413, detail="batch limit is 500 matches")
    return [engine.analyze(match) for match in matches]


@app.get("/analyze-demo", response_model=list[AnalysisResult])
def analyze_demo(limit: int = 25) -> list[AnalysisResult]:
    matches = read_ndjson_matches("data/demo_matches.ndjson", limit=limit)
    return [engine.analyze(match) for match in matches]
