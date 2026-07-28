from __future__ import annotations

import argparse
import json

from cs2_guard.engine import GuardEngine
from cs2_guard.services.dataset import read_ndjson_matches
from cs2_guard.services.report import summarize


def main() -> None:
    parser = argparse.ArgumentParser(prog="cs2-guard")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_file = sub.add_parser("analyze-file")
    analyze_file.add_argument("path")
    analyze_file.add_argument("--limit", type=int, default=100)
    analyze_file.add_argument("--pretty", action="store_true")

    args = parser.parse_args()

    if args.command == "analyze-file":
        engine = GuardEngine()
        matches = read_ndjson_matches(args.path, limit=args.limit)
        results = [engine.analyze(match) for match in matches]
        summary = summarize(results)
        payload = {
            "summary": summary.__dict__,
            "results": [result.model_dump() for result in results],
        }
        if args.pretty:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
