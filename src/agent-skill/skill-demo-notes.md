# Ghi Chú Minh Họa Agent Skill (AI Test Generator)

**Sinh viên:** Lê Trung Kiên (MSSV: 23127075)

## 1. Agent Skill Location

Skill đã được triển khai dưới dạng reusable Agent Skill tại:
- **SKILL.md:** `.agents/skills/api-test-generator/SKILL.md`
- **Resources:** `.agents/skills/api-test-generator/resources/` (pseudocode, diagram)
- **Examples:** `.agents/skills/api-test-generator/examples/` (FR-05 sample output)

Khi nộp bài, thư mục `.agents/` được copy vào `src/` để đi kèm sản phẩm.

## 2. Demo có thể trình bày thật

Skill **không** tự chạy end-to-end trong repo này như một CLI đóng gói. Demo trung thực gồm:

1. **Đầu vào:** `eshop-sut/api_specification.md`, FR/SEC trong README SUT, và endpoint đích (FR-05 / FR-08 / FR-18).
2. **Kích hoạt Skill:** Mở agent IDE (ví dụ Antigravity), yêu cầu agent sinh test cases cho một FR. Agent tự động phát hiện và invoke skill `api-test-generator`.
3. **Pipeline 6 bước quan sát được:**
   - Đọc `resources/diagram.mermaid` (không regenerate — sơ đồ do sinh viên tự vẽ);
   - Đọc `resources/pseudocode.md`;
   - Sinh bảng test cases Markdown theo format trong `examples/fr-05-sample-output.md`;
   - Dừng tại Human Review Gate — chờ user gán VALID/INVALID/INCOMPLETE;
   - Export traceability matrix với assertion ID trùng case ID;
   - `npm run test:validator` và (nếu SUT local) `npm run test:api`.
4. **Artifact kỳ vọng sau generator-in-the-loop:** Bảng AI 35 cases, audit VALID/INVALID/INCOMPLETE, human extensions ≥5, mapping NEWMAN 1-1, Newman reports đã redact.

## 3. Cách chạy demo

```bash
# 1. Mở Antigravity IDE tại thư mục repo
# 2. Nhập prompt:
#    "Sinh 35 test cases API cho FR-08 (POST /api/checkout) dựa trên eshop-sut/api_specification.md"
# 3. Agent tự phát hiện skill api-test-generator và thực hiện pipeline
# 4. Review output, gán VALID/INVALID/INCOMPLETE cho từng case
# 5. Yêu cầu agent xuất traceability matrix
```

## 4. Giới hạn

- `src/agent-skill/diagram.png` phải do sinh viên export thủ công từ mermaid đã tự vẽ.
- Skill không được bịa passing CI public hay GitHub issue.
- Skill không tự gán verdict — luôn dừng chờ human review.

## 5. Recording checklist (khi quay)

- [ ] Mở spec FR-08 hoặc FR-18 và chỉ đúng endpoint trong phạm vi.
- [ ] Chỉ mermaid do người vẽ, không bảo AI vẽ lại.
- [ ] Chỉ một case INVALID bị exclude và một case human bổ sung.
- [ ] Chỉ Newman assertion ID trùng case ID.
- [ ] Không paste JWT lên màn hình.

**Video URL:** *(tùy chọn — ghi link YouTube nếu có)*
