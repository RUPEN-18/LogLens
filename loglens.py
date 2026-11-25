"""Summarize text logs without external dependencies."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

LEVEL = re.compile(r"\b(TRACE|DEBUG|INFO|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b", re.I)

def analyze(lines, top=5):
    counts, errors = Counter(), Counter()
    total = 0
    for line in lines:
        if not line.strip():
            continue
        total += 1
        match = LEVEL.search(line)
        level = match.group(1).upper() if match else "UNKNOWN"
        level = "WARNING" if level == "WARN" else level
        counts[level] += 1
        if level in {"ERROR", "CRITICAL", "FATAL"}:
            message = line[match.end():].strip(" :|-[]\t\r\n") or "(no message)"
            errors[message] += 1
    return {"lines": total, "levels": dict(sorted(counts.items())),
            "top_errors": [{"message": msg, "count": n} for msg, n in errors.most_common(top)]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--json", type=Path, help="Save a JSON report")
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top must be positive")
    try:
        if args.json and args.json.resolve() == args.log.resolve():
            parser.error("Output cannot overwrite the input log")
        with args.log.open(encoding="utf-8", errors="replace") as source:
            report = analyze(source, args.top)
        print(f"LogLens | {report['lines']} non-empty lines")
        for level, count in report["levels"].items():
            print(f"{level:10} {count:>6}")
        print("\nMost frequent errors:")
        for error in report["top_errors"]:
            print(f"{error['count']:>4}  {error['message']}")
        if args.json:
            args.json.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    except OSError as exc:
        parser.exit(2, f"LogLens: {exc}\n")

if __name__ == "__main__":
    main()
