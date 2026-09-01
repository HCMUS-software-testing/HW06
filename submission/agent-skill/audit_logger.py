#!/usr/bin/env python3
"""Skill B — append one AUDIT-n block to docs/ai-audit-report.md.

Does not invent sessions. Only records a prompt/output pair the caller supplies.
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "docs" / "ai-audit-report.md"


def next_n(text: str) -> int:
    found = [int(x) for x in re.findall(r"### AUDIT-(\d+)", text)]
    return (max(found) + 1) if found else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tool", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--output-file", required=True)
    p.add_argument("--decision", choices=["ACCEPT", "REVISE", "REJECT"], default="ACCEPT")
    p.add_argument("--follow-up", default="")
    p.add_argument("--report", default=str(DEFAULT_REPORT))
    p.add_argument("--when", default=dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    args = p.parse_args()

    prompt = pathlib.Path(args.prompt_file).read_text(encoding="utf-8").strip()
    output = pathlib.Path(args.output_file).read_text(encoding="utf-8").strip()
    report_path = pathlib.Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    existing = report_path.read_text(encoding="utf-8") if report_path.exists() else (
        "# AI Audit Report — Member 3 (23127185)\n\n"
    )
    n = next_n(existing)
    block = (
        f"\n### AUDIT-{n}\n"
        f"- Tool: {args.tool}\n"
        f"- Date/time: {args.when}\n"
        f"- Task: {args.task}\n"
        f"- Prompt:\n\n```text\n{prompt[:4000]}\n```\n\n"
        f"- AI output: (rút gọn; full: `{args.output_file}`)\n\n"
        f"```text\n{output[:2500]}\n```\n\n"
        f"- Human decision: {args.decision}\n"
        f"- Follow-up: {args.follow_up or '(none)'}\n"
    )
    report_path.write_text(existing.rstrip() + "\n" + block, encoding="utf-8")
    print(f"appended AUDIT-{n} → {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
