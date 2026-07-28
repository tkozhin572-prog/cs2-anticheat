from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from cs2_guard.models import MatchTelemetry


def read_ndjson_matches(path: str | Path, limit: int | None = None) -> list[MatchTelemetry]:
    result: list[MatchTelemetry] = []
    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            result.append(MatchTelemetry.model_validate(json.loads(line)))
            if limit is not None and len(result) >= limit:
                break
    return result


def write_ndjson_matches(path: str | Path, matches: Iterable[MatchTelemetry]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as file:
        for match in matches:
            file.write(match.model_dump_json())
            file.write("\n")
