#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: Automated AI Interaction Audit Logger
Author: Lam Huu Khanh (Student ID: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing
Bloom-AI Level: G9.4 (Collaborate) / G9.5 (Create)

Description:
  Automatically appends structured interaction logs to ai-audit-report.md
  with Tool Name, Timestamp, Prompt, AI Output, Audit Decision (VALID/INVALID/INCOMPLETE),
  and Human Engineering notes as required by HW06 Section 9.
=============================================================================
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def find_audit_report_path() -> Path:
    candidates = [
        Path("reports/ai-audit-report.md"),
        Path("23127205_HW06_AI_API_100/reports/ai-audit-report.md"),
        Path("HW06/docs/ai-audit-report.md"),
        Path("HW06/reports/ai-audit-report.md"),
        Path("../reports/ai-audit-report.md"),
        Path("../../reports/ai-audit-report.md"),
    ]
    for c in candidates:
        if c.exists():
            return c.resolve()
    return Path("reports/ai-audit-report.md").resolve()


def log_interaction(
    ai_tool: str,
    prompt: str,
    ai_output: str,
    human_audit_label: str = "VALID",
    human_review_note: str = "",
    timestamp_str: str = None
):
    if not timestamp_str:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S +07:00")

    report_file = find_audit_report_path()
    report_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize file if not existing
    if not report_file.exists():
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Phụ Lục: Báo Cáo Kiểm Toán AI (AI Audit Report)\n\n")
            f.write("**Sinh viên thực hiện:** Lâm Hữu Khánh  \n")
            f.write("**Mã số sinh viên:** 23127205  \n")
            f.write("**Môn học:** Software Testing (HCMUS) — HW06: API Testing  \n\n")
            f.write("---\n\n")
            f.write("## 1. Khai Báo Sử Dụng AI (Mandatory AI Declaration)\n\n")
            f.write("> **\"I use AI tools for the following tasks:\"**\n")
            f.write("> 1. Sinh test cases API theo 4 kỹ thuật cho FR-02, FR-07, FR-15.\n")
            f.write("> 2. Chuyển đổi đặc tả SUT sang chuẩn OpenAPI 3.0.\n")
            f.write("> 3. Thiết kế JSON Schema và Chai Assertions cho Postman.\n")
            f.write("> 4. Xây dựng sơ đồ kiến trúc và Agent Skill sinh test tự động.\n\n")
            f.write("---\n\n")
            f.write("## 2. Nhật Ký Toàn Bộ Các Phiên Tương Tác AI (Detailed AI Audit Logs)\n\n")

    # Determine session number
    session_num = 1
    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()
        matches = re.findall(r"### 🔹 Phiên (\d+):", content)
        if matches:
            session_num = max([int(m) for m in matches]) + 1

    entry = f"""
---

### 🔹 Phiên {session_num}: Tương tác AI Mới ({timestamp_str})

- **Tên công cụ AI:** {ai_tool}
- **Ngày và giờ:** {timestamp_str}
- **Prompt của bạn:**
```text
{prompt.strip()}
```

- **Đầu ra của AI:**
```markdown
{ai_output.strip()}
```

- **Đánh giá kiểm toán của con người (Human Audit Decision):**
  - **Nhãn kiểm toán:** `{human_audit_label}`
  - **Ghi chú & Hành động chỉnh sửa:** {human_review_note.strip() if human_review_note else "Đã kiểm toán và xác nhận hợp lệ."}

"""
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ [SUCCESS] Logged Session #{session_num} to: {report_file}")
    return report_file


if __name__ == "__main__":
    print("[*] Automated AI Audit Logger utility ready.")
