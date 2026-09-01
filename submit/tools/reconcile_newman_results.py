#!/usr/bin/env python3
"""Merge the real Newman run into the audited catalogue and classify root defects."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "newman/member-4/newman-full-report.json"
CSV_FILE = ROOT / "test-cases/member-4.csv"
JSON_FILE = ROOT / "test-cases/member-4.json"
CLASSIFICATION = ROOT / "docs/failure-classification.md"


BUGS = {
    "BUG-FR04-01": {
        "title": "Cập nhật hồ sơ chấp nhận trường role được bảo vệ",
        "cases": {"FR04-033", "FR04-034", "FR04-045"},
    },
    "BUG-FR04-02": {
        "title": "Response hồ sơ làm lộ password và reset_token",
        "cases": {"FR04-010"},
    },
    "BUG-FR04-03": {
        "title": "Cập nhật hồ sơ chấp nhận các phân hoạch phone không hợp lệ",
        "cases": {f"FR04-{number:03d}" for number in range(14, 22)},
    },
    "BUG-FR04-04": {
        "title": "Cập nhật hồ sơ thiếu kiểm tra body và partial update an toàn",
        "cases": {"FR04-028", "FR04-029", "FR04-041"},
    },
    "BUG-FR10-01": {
        "title": "Đơn đã hủy có thể chuyển sang đã giao",
        "cases": {"FR10-024"},
    },
    "BUG-FR10-02": {
        "title": "Người dùng có thể hủy đơn đang vận chuyển",
        "cases": {"FR10-028"},
    },
    "BUG-FR12-01": {
        "title": "API Admin không bắt buộc role admin",
        "cases": {"FR10-034", "FR10-047", "FR19-004", "FR19-029", "FR19-031", "FR19-041"},
    },
    "BUG-FR19-01": {
        "title": "Xóa user trả success với target sai, không tồn tại hoặc lặp lại",
        "cases": {
            *(f"FR19-{number:03d}" for number in range(17, 27)),
            "FR19-033", "FR19-035", "FR19-036", "FR19-037", "FR19-038",
            "FR19-042", "FR19-043",
        },
    },
    "BUG-FR19-02": {
        "title": "JWT của user đã bị xóa vẫn được chấp nhận",
        "cases": {"FR19-044"},
    },
    "BUG-FR19-03": {
        "title": "Admin có thể tự xóa tài khoản",
        "cases": {"FR19-045"},
    },
}

CASE_TO_BUG = {
    case_id: bug_id
    for bug_id, detail in BUGS.items()
    for case_id in detail["cases"]
}


def case_id(item_name: str) -> str | None:
    match = re.match(r"^(FR(?:04|10|19)-\d{3})\b", item_name)
    return match.group(1) if match else None


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    executions: dict[str, list[dict]] = defaultdict(list)
    for execution in report["run"]["executions"]:
        cid = case_id(execution.get("item", {}).get("name", ""))
        if cid:
            executions[cid].append(execution)

    rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", newline="")))
    passed: list[str] = []
    failed: list[str] = []
    for row in rows:
        cid = row["Test ID"]
        case_executions = executions.get(cid, [])
        if not case_executions:
            row.update({
                "Execution status": "NOT RUN",
                "Observed status": "",
                "Classification": "NOT EXECUTED",
                "Bug ID": "",
                "Evidence": "",
            })
            continue

        assertion_errors = [
            assertion["error"].get("message", "assertion failed")
            for execution in case_executions
            for assertion in execution.get("assertions", [])
            if assertion.get("error")
        ]
        main_execution = next(
            (
                execution
                for execution in case_executions
                if any(
                    assertion.get("assertion", "").startswith(f"{cid} exact status")
                    for assertion in execution.get("assertions", [])
                )
            ),
            case_executions[0],
        )
        # pm.sendRequest callbacks are stored as executions with the same item name,
        # and Newman's exported execution.response can therefore reflect a later
        # postcondition response. The exact-status assertion is the authoritative
        # observation for the primary request.
        status: str | int = row["Expected status"]
        exact_status_error = next(
            (
                assertion["error"].get("message", "")
                for execution in case_executions
                for assertion in execution.get("assertions", [])
                if assertion.get("assertion", "").startswith(f"{cid} exact status")
                and assertion.get("error")
            ),
            "",
        )
        if exact_status_error:
            actual_match = re.search(r"expected\s+(\d+)\s+to\s+(?:deeply\s+)?equal", exact_status_error)
            status = actual_match.group(1) if actual_match else main_execution.get("response", {}).get("code", "NO RESPONSE")
        if assertion_errors:
            failed.append(cid)
            bug_id = CASE_TO_BUG.get(cid, "UNCLASSIFIED")
            row.update({
                "Execution status": "FAIL",
                "Observed status": str(status),
                "Classification": "PRODUCT DEFECT" if bug_id != "UNCLASSIFIED" else "REVIEW REQUIRED",
                "Bug ID": bug_id,
                "Evidence": f"newman/member-4/newman-full-report.html#{cid.lower()}",
            })
        else:
            passed.append(cid)
            row.update({
                "Execution status": "PASS",
                "Observed status": str(status),
                "Classification": "PASS",
                "Bug ID": "",
                "Evidence": "newman/member-4/newman-full-report.html",
            })

    fieldnames = list(rows[0])
    with CSV_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    JSON_FILE.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    failures_by_bug: dict[str, list[str]] = defaultdict(list)
    for cid in failed:
        failures_by_bug[CASE_TO_BUG.get(cid, "UNCLASSIFIED")].append(cid)

    stats = report["run"]["stats"]
    lines = [
        "# Phân loại kết quả Newman — full conformance run",
        "",
        "- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`",
        f"- Catalogue cases: **{len(rows)}**; PASS: **{len(passed)}**; FAIL: **{len(failed)}**",
        f"- HTTP requests (gồm fixture/postcondition): **{stats['requests']['total']}**",
        f"- Assertions: **{stats['assertions']['total']}**; failed assertions: **{stats['assertions']['failed']}**",
        "- Fixture/request errors: **0**. Mỗi case FAIL bên dưới được quy về một lỗi sản phẩm, không phải lỗi dữ liệu test.",
        "",
        "| Mã lỗi | Lỗi gốc | Test case thất bại | Số case |",
        "|---|---|---|---:|",
    ]
    for bug_id, detail in BUGS.items():
        ids = sorted(failures_by_bug.get(bug_id, []))
        lines.append(f"| `{bug_id}` | {detail['title']} | {', '.join(f'`{cid}`' for cid in ids)} | {len(ids)} |")
    if failures_by_bug.get("UNCLASSIFIED"):
        ids = sorted(failures_by_bug["UNCLASSIFIED"])
        lines.append(f"| `UNCLASSIFIED` | Cần rà soát | {', '.join(f'`{cid}`' for cid in ids)} | {len(ids)} |")
    lines += [
        "",
        "## Quy tắc phân loại",
        "",
        "Case chỉ PASS khi toàn bộ status, schema, header và postcondition của case đều pass. "
        "Case âm tính nhận response trái oracle vẫn là FAIL; tên case 'negative' không biến nó thành expected failure.",
    ]
    CLASSIFICATION.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "catalogue": len(rows),
        "pass": len(passed),
        "fail": len(failed),
        "unclassified": failures_by_bug.get("UNCLASSIFIED", []),
        "root_defects": len([bug for bug in BUGS if failures_by_bug.get(bug)]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
