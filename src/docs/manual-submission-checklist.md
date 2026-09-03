# Manual submission checklist

Các việc sau vẫn mở trong repo local. Marker thủ công nằm ở cột/file đích, không dùng để tuyên bố xong.

| Unresolved action | Evidence destination |
| --- | --- |
| Confirm/redraw and export Agent Skill diagram | `src/agent-skill/diagram.png` (source remains `src/agent-skill/diagram.mermaid`; do not let AI regenerate the mermaid) |
| Capture Postman console showing `X-Student-Id` | screenshot path referenced from `src/docs/main-report.md` or `src/README.md` |
| Create public GitHub issues and screenshots for confirmed bugs | each record in `src/bug-reports/bug-report.md` (`External issue`, `Screenshot`) |
| Run and link one passing CI commit | `src/docs/cicd-report.md` and `src/docs/ci-manual-evidence.md` |
| Run and link one intentionally failing CI commit | `src/docs/cicd-report.md` and `src/docs/ci-manual-evidence.md` |
| Record optional Agent Skill video | `src/agent-skill/skill-demo-notes.md` (`Video URL`) |
| Choose final self-assessed grade after inserting the evidence above | `src/README.md` self-assessment table |
| Copy `src/` to `23127075_HW06_AI_API_<grade>` and zip only after chosen evidence is inserted | submission zip outside git |

PDF export of Markdown reports is intentionally left to the student.
