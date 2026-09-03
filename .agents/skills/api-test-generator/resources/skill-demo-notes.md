# Ghi Chú Minh Họa Agent Skill (AI Test Generator)

**Sinh viên:** Lê Trung Kiên (MSSV: 23127075)

## 1. Agent Skill Location

Skill đã được triển khai dưới dạng reusable Agent Skill tại:
- **SKILL.md:** `.agents/skills/api-test-generator/SKILL.md`
- **Resources:** `.agents/skills/api-test-generator/resources/` (pseudocode, diagram.mermaid, chart.png)
- **Examples:** `.agents/skills/api-test-generator/examples/` (FR-05 sample output)

Khi nộp bài, thư mục `.agents/` được đưa vào `src/` để đi kèm sản phẩm.

## 2. Demo có thể trình bày thật

Skill **không** tự chạy end-to-end trong repo này như một CLI đóng gói. Demo trung thực gồm:

1. **Đầu vào:** `eshop-sut/api_specification.md`, FR/SEC trong README SUT, và endpoint đích (FR-05 / FR-08 / FR-18).
2. **Kích hoạt Skill:** Mở agent IDE (ví dụ Antigravity), yêu cầu agent sinh test cases cho một FR. Agent tự động phát hiện và invoke skill `api-test-generator`.
3. **Pipeline 6 bước quan sát được:**
   - Đọc `resources/diagram.mermaid` & `resources/chart.png` (sơ đồ do sinh viên tự vẽ);
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
#    "Kích hoạt Agent Skill api-test-generator để tự động sinh bộ 35 test cases API cho FR-18..."
# 3. Agent tự phát hiện skill api-test-generator và thực hiện pipeline
# 4. Review output, gán VALID/INVALID/INCOMPLETE cho từng case
# 5. Yêu cầu agent xuất traceability matrix
```

## 4. Giới hạn

- `chart.png` do sinh viên vẽ và lưu tại `resources/chart.png`.
- Skill không được bịa passing CI public hay GitHub issue.
- Skill không tự gán verdict — luôn dừng chờ human review.

## 5. Recording checklist

- [x] Mở spec FR-18 và chỉ đúng endpoint trong phạm vi.
- [x] Chỉ mermaid/chart do người vẽ.
- [x] Case ID và assertion ID trùng 1-1.
- [x] Không paste JWT lên màn hình.

**Video URL:** https://youtu.be/WtXNlbtjnk4
