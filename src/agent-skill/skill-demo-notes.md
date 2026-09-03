# Ghi Chú Minh Họa Agent Skill (AI Test Generator)

**Sinh viên:** Lê Trung Kiên (MSSV: 23127075)

## 1. Demo có thể trình bày thật

Skill **không** tự chạy end-to-end trong repo này như một CLI đóng gói. Demo trung thực gồm:

1. Đầu vào: `eshop-sut/api_specification.md`, FR/SEC trong README SUT, và endpoint đích (FR-05 / FR-08 / FR-18).
2. Lệnh quan sát artifact có thật:
   - đọc `src/agent-skill/diagram.mermaid` (không regenerate);
   - đọc `src/agent-skill/pseudocode.md`;
   - chỉ case Markdown + `src/test-cases/member-2-traceability.md`;
   - `npm run test:validator` và (nếu SUT local) `npm run test:api`.
3. Artifact kỳ vọng sau generator-in-the-loop: bảng AI 35 cases, audit VALID/INVALID/INCOMPLETE, human extensions, mapping NEWMAN 1-1, Newman reports đã redact.

## 2. Giới hạn

- Không có video recording trong repo.
- `src/agent-skill/diagram.png` phải do sinh viên export thủ công từ mermaid đã tự vẽ.
- Skill không được bịa passing CI public hay GitHub issue.

## 3. Recording checklist (khi quay)

- [ ] Mở spec FR-08 hoặc FR-18 và chỉ đúng endpoint trong phạm vi.
- [ ] Chỉ mermaid do người vẽ, không bảo AI vẽ lại.
- [ ] Chỉ một case INVALID bị exclude và một case human bổ sung.
- [ ] Chỉ Newman assertion ID trùng case ID.
- [ ] Không paste JWT lên màn hình.

**Video URL:** MANUAL-EVIDENCE-REQUIRED
