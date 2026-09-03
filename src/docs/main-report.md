# Báo Cáo Chi Tiết HW06 - API Testing

**Sinh viên:** Lê Trung Kiên (23127075) — Thành viên 2  
**SUT:** EShop backend `http://localhost:3000`  
**Nguồn thực thi:** `src/newman/member-2/summary.json` (`generatedAt: 2026-09-03T02:43:08.840Z`)

## 1. Phạm vi API

- FR-05: `GET /api/products` và `GET /api/products?search=keyword`. Product detail `GET /api/products/:id` thuộc FR-06 và không được tự động hóa như FR-05.
- FR-08: `POST /api/checkout`.
- FR-18: `GET /api/admin/orders` và `PUT /api/admin/orders/:id/status`.

## 2. Generate, audit, extend, execute

Mỗi FR giữ 35 AI IDs đã audit VALID/INVALID/INCOMPLETE và ít nhất 10 human IDs. Final intent nằm ở bảng audit + `member-2-traceability.md`.

| Metric | FR-05 | FR-08 | FR-18 | Total |
| --- | ---: | ---: | ---: | ---: |
| authored | 45 | 45 | 45 | 135 |
| automated | 32 | 24 | 35 | 91 |
| BROWSER-MANUAL | 7 | 3 | 1 | 11 |
| FAULT-INJECTION | 0 | 0 | 2 | 2 |
| EXCLUDED | 6 | 18 | 7 | 31 |
| Tổng số test cases thực thi | 32 | 23 | 35 | 90 |
| PASS | 28 | 2 | 22 | 52 |
| FAIL | 4 | 21 | 13 | 38 |
| pending | 0 | 0 | 0 | 0 |
| requests | 132 | 262 | 398 | 792 |

FR-08 có 24 hàng Newman trong traceability nhưng suite JSON chỉ ghi 23 assertions vì runner ghi 2 request pending. PASS/FAIL là assertion Newman, không phải số case Markdown.

## 3. Tính năng Postman đã dùng

- Collection-level header script gắn `X-Student-Id`.
- Environment local không chứa JWT.
- Test scripts map 1-1 assertion ID với case NEWMAN.
- `pm.sendRequest` cho register/login/cart/order fixtures, postcondition, và race FR-08.
- Data files JSON theo suite.
- Newman reporters CLI/JSON/HTML Extra; runner redact Authorization/JWT trước khi ghi `src/newman/member-2/`.

## 4. Kết quả và bug

Local `npm run test:api` exit khác 0 vì 38 assertion failures. Không diễn giải đó thành “toàn bộ API passed”.

12 defect đã tái hiện trên SUT và ghi trong `src/bug-reports/member-2-bugs.md`:

- FR-05: BUG-001 (SQLi / SQL error leakage trên search).
- FR-08: BUG-002, BUG-003, BUG-007 … BUG-012 (client total, cart không xóa, checkout chấp nhận cart/address không hợp lệ).
- FR-18: BUG-004, BUG-005, BUG-006 (thiếu RBAC admin, mass-assignment `role`, canceled → delivered).

GitHub issue URL và screenshot chưa thu thập trong repo này.

## 5. CI/CD

Workflow `.github/workflows/newman-api-tests.yml` checkout bài nộp + `ttbhanh/eshop-sut`, health-check `GET http://127.0.0.1:3000/api/products`, rồi `npm run test:api`. Public passing/failing run chưa có; xem `src/docs/cicd-report.md` và `src/docs/ci-manual-evidence.md`.

## 6. Tự đánh giá

Self-assessment hiện tại **84/100** (26 + 25 + 26 + 7). Trừ điểm vì thiếu bằng chứng public CI, issue/screenshot, `diagram.png`, và video Agent Skill. Chi tiết checklist: `src/docs/manual-submission-checklist.md`.
