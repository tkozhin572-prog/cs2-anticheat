# CS2 Guard — Safe Telemetry Anti-Cheat Prototype

Большой рабочий прототип античита для CS2, но безопасный: он анализирует только телеметрию матча.

## Что внутри

- FastAPI backend
- CLI-анализатор
- Risk scoring engine
- Несколько независимых детекторов
- JSONL/NDJSON датасет примерно на 100 МБ
- HTML dashboard
- Unit tests
- GitHub Actions
- Документация
- Без драйверов, инжекта, чтения памяти, обхода защиты и вмешательства в CS2

## Быстрый старт

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
uvicorn cs2_guard.api:app --reload
```

Открыть API:

```text
http://127.0.0.1:8000/docs
```

CLI:

```powershell
python -m cs2_guard.cli analyze-file data/demo_matches.ndjson --limit 50
```

Dashboard:

```text
src/cs2_guard/dashboard/index.html
```

## Важно

Нельзя банить игрока только по одному скору. Этот проект делает пометки:
`low_risk`, `review`, `high_risk`. Финальное решение всегда за человеком.
