# HW06 — Kế hoạch triển khai Member 3

| Mục | Chi tiết |
| --- | --- |
| Sinh viên | Mai Thị Kim Duyên |
| MSSV | `23127185` |
| Vai trò | Thành viên 3 |
| Branch | `melyen` |
| Header bắt buộc | `X-Student-Id: 23127185` |
| ZIP | `23127185_HW06_AI_API_<000-100>.zip` |
| Bộ ba API | FR-01 Đăng ký · FR-09 Áp dụng coupon · FR-17 CRUD coupon (admin) |
| Trách nhiệm nhóm | Báo cáo chính (cấu trúc + gom summary) · Chuẩn AI Audit |
| Ngôn ngữ | Báo cáo tiếng Việt · Tên test / Postman script tiếng Anh |
| Công cụ thực thi | Postman + Newman (`htmlextra`) · GitHub Actions |
| SUT | EShop backend `http://localhost:3000` — spec thắng implementation |

Teammate đã chiếm API: Member 1 (`khanh`, `23127205`) FR-02/07/15 · Member 4 (`Bao`, `23127326`) FR-04/10/19. Không tái sử dụng collection, Student ID, prompt, hay diagram của họ.

---

## 1. Nguyên tắc phân loại công việc

Bốn chế độ, không được trộn:

| Chế độ | Ký hiệu | Nghĩa | Ranh giới |
| --- | --- | --- | --- |
| **AI chạy** | `RUN` | Claude Code / script tự viết file, cài SUT, chạy Newman, commit, export log | Được phép **thực thi thật**. Cấm bịa HTML, screenshot, hostname. |
| **Prompting** | `PROMPT` | Hỏi AI từng bước, nhận draft, người quyết định | Bắt buộc step-by-step theo kỹ thuật đã học. Cấm một prompt “generate all 35 cases”. |
| **Agent Skill** | `SKILL` | Gói tái sử dụng: input chuẩn → output chuẩn, không phải chat ad-hoc | Chỉ làm skill khi lặp lại ≥ 3 lần hoặc là deliverable G9.5. |
| **Bắt buộc tay** | `MANUAL` | Người phải nhìn, quyết, vẽ, chụp, hoặc chịu trách nhiệm nhãn | AI được **gợi ý**, không được **ký tên** hộ. |

Anti-cheat (TA kiểm tra, không được AI-generate hay bịa):

1. Console screenshot `X-Student-Id: 23127185` từ pre-request script.
2. Newman HTML có hostname khớp SUT thật (`localhost` / `127.0.0.1` chấp nhận).
3. Sơ đồ Agent Skill **tự vẽ** — AI không được generate ảnh diagram.

---

## 2. Ma trận toàn bộ công việc

### 2.1 Hạ tầng

| Task | Chế độ | Ghi chú |
| --- | --- | --- |
| Clone SUT (`ttbhanh/eshop-sut`), `npm install`, seed, start `:3000` | `RUN` | Pin commit nếu CI (Member 4 dùng `85af3ba`). |
| Fixture users riêng cho register/coupon (tránh đụng lockout Member 1) | `RUN` + `PROMPT` | AI viết seed; người xác nhận không phá SRS. Không “sửa bug” SUT. |
| Cấu trúc thư mục `postman/ newman/member-3/ test-cases/ bug-reports/ docs/ agent-skill/` | `RUN` | |
| Postman environment (`base_url`, `student_id=23127185`, admin/user tokens) | `RUN` | |
| Pre-request upsert `X-Student-Id` + `console.log` | `RUN` | Script AI viết được. **Chụp console = `MANUAL`.** |
| GitHub Actions: start SUT → health-check `GET /api/products` → Newman | `RUN` | Hai run: sanity xanh, một assertion fail có chủ đích. |
| `.gitignore` (`node_modules/`, `*.log`, `*.sqlite-journal`) | `RUN` | |

### 2.2 Sinh / audit / mở rộng test (lặp 3 API)

| Task | Chế độ | Ghi chú |
| --- | --- | --- |
| Đọc spec + SRS cho từng endpoint, liệt kê parameter / rule / role / schema | `PROMPT` | Prompt 1 của mỗi API — chỉ extract, chưa sinh case. |
| Equivalence partitioning + BVA từng tham số | `PROMPT` | Prompt 2 — từng field, không gộp 3 API. |
| Decision table (đặc biệt FR-09: 5 điều kiện coupon) | `PROMPT` | Prompt 3. |
| State / lifecycle (coupon hết hạn, max uses, xóa coupon đang dùng) | `PROMPT` | Prompt 4. |
| Security SEC-01–SEC-07 (SQLi, IDOR, role escalation, mass assignment) | `PROMPT` | Prompt 5. |
| Schema validation (đúng shape spec, status code) | `PROMPT` | Prompt 6. |
| Gộp thành ≥ 35 case / API, đánh ID | `SKILL` hoặc `PROMPT` | Skill generator nếu đã sẵn; nếu chưa thì prompt gộp có kiểm soát. |
| Gán nhãn `VALID` / `INVALID` / `INCOMPLETE` + lý do | **`MANUAL`** | AI được đề xuất nhãn (`PROMPT`). Người ký nhãn. Nộp raw AI = 0 tinh thần đề. |
| Sửa case INVALID/INCOMPLETE | `PROMPT` + `MANUAL` | AI sửa theo lý do audit; người duyệt bản cuối. |
| ≥ 5 case human-added / API, giải thích AI miss vì sao | **`MANUAL`** | AI được dùng như sparring partner. Case cuối phải do người chọn và giải thích. |
| Ghi AI Audit (tool, datetime, prompt, output) mỗi lần tương tác | `SKILL` | Member 3 owns format — đây là skill vận hành, không thay G9.5. |

### 2.3 Thực thi & bug

| Task | Chế độ | Ghi chú |
| --- | --- | --- |
| Implement request + test script Postman từ bảng case đã chốt | `RUN` + `PROMPT` | AI sinh script; người soi assertion (đừng assert bug thành “đúng hành vi”). |
| CSV data-driven (Collection Runner) | `RUN` | FR-01 email/password partitions; FR-09 coupon codes. |
| Chia folder `01_Sanity_Suite` (kỳ vọng xanh) vs `02_Bug_Discovery_Suite` (bắt defect SUT) | `RUN` | Học pattern Member 1, **không copy API của họ**. |
| `node database.js` rồi Newman từng folder, export HTML | `RUN` | Thực thi thật. Cấm generate HTML giả. |
| Chụp Postman Console ra `X-Student-Id` | **`MANUAL`** | Anti-cheat. |
| Phân loại fail: bug SUT / test sai / fixture bẩn | `PROMPT` + `MANUAL` | Người quyết bug nào là “thật”. |
| Bug report Markdown + GitHub Issue + screenshot | `PROMPT` draft, **`MANUAL`** file issue & chụp | Issue phải là repo thật, screenshot UI GitHub. |
| Mock server / environments / variables (liệt kê trong báo cáo) | `RUN` | Dùng vừa đủ để có mục “Postman features used”. |

### 2.4 Agent Skill G9.5 (10 điểm cá nhân)

| Task | Chế độ | Ghi chú |
| --- | --- | --- |
| Thiết kế generator: spec → test cases (parser → heuristic → LLM → validator) | `PROMPT` + `MANUAL` | Member 4 owns thiết kế nhóm; Member 3 **vẫn phải có diagram + pseudocode trong ZIP cá nhân**. |
| Sơ đồ tự vẽ (PNG) | **`MANUAL`** | Bất kỳ tool (draw.io, Excalidraw tay, giấy chụp). **Cấm AI vẽ hộ.** |
| Pseudocode `.md` | `PROMPT` + `MANUAL` | AI draft; người chốt quyết định thiết kế. |
| Implement skill tái sử dụng (optional nhưng nên làm) | `SKILL` + `RUN` | Input: `api_specification.md` hoặc OpenAPI. Output: CSV/JSON cases + skeleton collection. Demo 1 API (FR-09 hợp nhất vì decision table). |
| Video demo YouTube (optional) | **`MANUAL`** | Quay tay. |

### 2.5 Báo cáo, CI, đóng gói (Member 3 primary: report + audit format)

| Task | Chế độ | Ghi chú |
| --- | --- | --- |
| Template AI Audit cho cả nhóm (cột bắt buộc) | `SKILL` + `MANUAL` | Chốt format, phổ biến cho member 1/2/4. |
| `docs/ai-audit-report.md` cá nhân — log đủ từng interaction | `SKILL` điền, `MANUAL` rà | Thiếu datetime/prompt/output = audit hỏng. |
| AI Critique 200–300 từ | **`MANUAL`** | AI draft được, phải viết lại bằng giọng người, đúng số từ. |
| `docs/main-report.md` (pipeline 3 API + evidence links) | `PROMPT` + `MANUAL` | AI dựng skeleton; người điền số liệu thật từ Newman. |
| Gom test summary nhóm (nếu tới phase tích hợp) | `PROMPT` + `MANUAL` | Owner Member 3. Không bịa số teammate. |
| `docs/cicd-report.md` + screenshot 2 run GitHub Actions | `RUN` tạo workflow, **`MANUAL`** chụp Actions UI | |
| OpenAPI 3.0 từ spec (optional, nếu AI-gen thì phải audit) | `PROMPT` + `MANUAL` audit | |
| Excel `test-cases/member-3.xlsx` | `RUN` từ CSV đã audit | Cột thống nhất với template Member 2 nếu đã có. |
| `git-commit-log.txt` | `RUN` | `git log --author` / branch `melyen`. |
| README self-assessment + counts | `MANUAL` số liệu, `RUN` file | Điểm tự chấm người ghi. |
| PDF từ Markdown | `RUN` | pandoc/typst — nội dung PDF = nội dung MD đã chốt. |
| ZIP cuối | `RUN` + `MANUAL` checklist | Thiếu 1 artifact = 0. |

---

## 3. Hai Agent Skill nên xây (không hơn)

Skill chỉ đáng viết khi tái sử dụng hoặc được chấm. Phần còn lại prompting.

### Skill A — `ai-api-test-generator` (deliverable G9.5)

- **Input:** `eshop-sut/api_specification.md` + id feature (`FR-01` / `FR-09` / `FR-17`) + `student_id`.
- **Pipeline 4 tầng:**
  1. Parser: endpoint, method, params, constraints, roles, response schema.
  2. Heuristic: EP, BVA, decision table, auth matrix, SEC-01–07, schema asserts.
  3. Structured prompt tới LLM (một technique / một call — không one-shot).
  4. Validator: đủ ≥ 35, có expected status + expected body keys, không trùng ID.
- **Output:** `test-cases/generated/FR-xx.csv` + skeleton folder Postman.
- **Demo:** FR-09 (5 điều kiện coupon = decision table rõ, dễ bảo vệ vấn đáp).
- Diagram **vẽ tay**. Pseudocode trong `agent-skill/pseudocode.md`.

### Skill B — `hw06-ai-audit-logger` (vận hành, khớp trách nhiệm nhóm)

Đề bài khuyến khích skill tự trích xuất audit sau mỗi phiên AI. Member 3 owns format nên làm cái này.

- **Input:** transcript phiên (prompt + output) hoặc file MD nháp.
- **Output append** vào `docs/ai-audit-report.md`:

```text
### AUDIT-<n>
- Tool:
- Date/time: (ISO, local)
- Task:
- Prompt:
- AI output: (rút gọn có chủ đích, giữ nguyên ý; đính full trong docs/ai-audit-transcripts/)
- Human decision: ACCEPT / REVISE / REJECT
- Follow-up:
```

Không dùng Skill B để bịa log. Chỉ log phiên đã xảy ra.

**Không** viết skill cho: vẽ diagram, chấm VALID, file GitHub Issue, viết critique, chụp màn hình. Những việc đó cố ý để tay.

---

## 4. Protocol prompting (cấm one-shot)

Mỗi API = tối thiểu 6 prompt riêng, đúng thứ tự kỹ thuật. Mỗi prompt ghi vào AI Audit.

**Prompt 1 — Extract (Apply)**  
“Đây là đoạn spec + SRS của `<FR>`. Liệt kê parameters, ràng buộc, actor/role, status code, response schema. Chưa sinh test.”

**Prompt 2 — Domain partition**  
“Từ bảng constraint, làm equivalence partitioning + BVA cho **từng** parameter. Một hàng = một class. Chưa gộp test case.”

**Prompt 3 — Combinatorial / decision table**  
FR-01: email × password × missing field.  
FR-09: C1 tồn tại × C2 hạn × C3 min order × C4 login × C5 remaining uses.  
FR-17: role × method × field validity.

**Prompt 4 — State / lifecycle**  
FR-01: duplicate sau register thành công.  
FR-09: dùng 1 lần rồi dùng lại; coupon hết hạn; coupon bị admin xóa giữa chừng.  
FR-17: create → list → delete → apply mã đã xóa.

**Prompt 5 — Security**  
SQLi/XSS trên name/email/code; unauthenticated; user token gọi admin; mass-assign `role` / `is_active` / `user_id`; IDOR `user_id` trong apply-coupon; oversized payload.

**Prompt 6 — Schema + gom ID**  
“Gộp thành test case ID `M3-<FR>-<nnn>`. Mỗi case: precond, request, expected status, expected keys, technique tag. Mục tiêu ≥ 35. Đánh dấu chỗ thiếu.”

Sau đó **người** audit. Prompt 7 (optional): “Đây là case INCOMPLETE/INVALID và lý do. Sửa, không thêm case mới.”

Human-added: người liệt kê lỗ hổng (thường security + state) **trước**, mới hỏi AI formalize — không để AI tự “thêm 5 case”.

---

## 5. Chiến lược test theo API

Mục tiêu thiết kế mỗi API: ≥ 35 AI + ≥ 5 human ≈ 40+. Sanity (xanh) tách khỏi discovery (bắt bug). Re-seed DB trước mọi run lockout/CRUD/coupon usage.

### FR-01 `POST /api/register` — Pool A

| Nhóm | Coverage |
| --- | --- |
| Happy | name + email hợp lệ + password mạnh → 200, có `id`, message theo spec |
| Email EP | thiếu `@`, thiếu domain, unicode, dấu cách, empty, null, missing key, duplicate |
| Password EP/BVA | `<8`, đúng 8, thiếu hoa/thường/số/ký tự đặc biệt `@$!%*?&`, confirm mismatch (nếu API nhận), quá dài |
| Name | empty, missing, rất dài, XSS `<script>` |
| Security | SQLi trong email/name; mass-assign `role=admin` |
| Schema | success keys; error shape; không trả password |

Human-added gợi ý (chọn ≥ 5, giải thích AI miss): register với `role` trong body; email khác nhau chỉ khác case; password đúng policy nhưng email duplicate; Content-Type không JSON; double-submit.

### FR-09 `POST /api/apply-coupon` — Pool B

Spec: 5 điều kiện đồng thời + công thức percent/fixed. Body: `{ code, total_amount, user_id }`.

| Nhóm | Coverage |
| --- | --- |
| C1–C5 decision table | đủ 5 true; lần lượt từng điều kiện false |
| Boundary C3 | `total = min - 1`, `= min`, `= min + 1` (`SAVE10` min 300000) |
| Loại | `SAVE10` percent; `BIGBUY`/`VIP100` fixed; `EXPIRED` |
| Usage | `VIP100` lần 1, lần 2, lần 3 (max 2) |
| Auth | không token; token user; token admin; `user_id` của người khác (IDOR) |
| Tamper | `total_amount` client không khớp giỏ (nếu đi với checkout); code SQLi; code empty |
| Schema | `discount_amount`, `final_amount` |

Human-added gợi ý: coupon inactive `is_active=0` nếu tạo được qua FR-17; apply mã vừa xóa; percent > 100 do FR-17 không validate; `user_id` numeric vs string; gọi apply không login dù C4 yêu cầu.

### FR-17 Coupon CRUD — Pool C

`GET /api/coupons` (admin per spec) · `POST /api/admin/coupons` · `DELETE /api/admin/coupons/:id`.

| Nhóm | Coverage |
| --- | --- |
| AuthZ | no token / user token / admin token trên từng method |
| Create valid | percent + fixed, đủ field |
| Create invalid | code trùng, type lạ, discount ≤ 0, `min_order_amount` < 0, `max_uses_per_user` < 1, `expired_at` quá khứ, missing field |
| Delete | id tồn tại, id không tồn tại, id của người khác N/A, xóa 2 lần |
| List | admin thấy danh sách; user bị từ chối (nếu spec) |
| Privilege | user tạo coupon; user xóa; mass-assign |
| Schema | response create/list/delete khớp spec |

Human-added gợi ý: tạo `discount_value=1000` type percent; `expired_at` format sai; xóa coupon đang được user khác apply; GET `/api/coupons` không phải `/api/admin/coupons` (lệch path spec); admin xóa rồi FR-09 vẫn apply (nếu SUT sót).

Seed coupon dùng khi test FR-09: `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`. Tạo mã throwaway (`M3TEST*`) cho FR-17 để không phá fixture FR-09.

---

## 6. Thứ tự thực hiện

Không song song 3 API ở bước generate. Xong extract cả 3 (hiểu hệ), rồi đào sâu từng API đến audit, rồi mới implement Postman hàng loạt.

```text
P0  Hạ tầng          RUN: SUT + folder + env + pre-request + gitignore
P1  Chuẩn audit      SKILL B + MANUAL: template AI Audit phổ biến nhóm
P2  FR-01 generate   PROMPT ×6 → MANUAL audit → MANUAL +5 human
P3  FR-09 generate   PROMPT ×6 → MANUAL audit → MANUAL +5 human
P4  FR-17 generate   PROMPT ×6 → MANUAL audit → MANUAL +5 human
P5  Excel chốt       RUN từ CSV đã audit (đây là nguồn sự thật, không phải collection)
P6  Postman          RUN/PROMPT implement theo Excel; DDT CSV
P7  Execute          RUN reseed + Newman sanity + discovery; MANUAL screenshot header
P8  Bugs             MANUAL chọn defect thật; PROMPT draft; MANUAL GitHub Issue
P9  Skill G9.5       MANUAL vẽ diagram; PROMPT+MANUAL pseudocode; RUN implement; demo FR-09
P10 CI/CD            RUN workflow; MANUAL chụp 2 run (pass / fail chủ đích)
P11 Báo cáo          PROMPT skeleton; MANUAL số liệu; Critique tay; git log RUN
P12 Tích hợp nhóm    MANUAL gom summary (owner Member 3) — sau khi 1/2/4 có số
P13 ZIP              checklist tay
```

Commit tối thiểu (đề yêu cầu 1 commit / bước / API, ≥ 12):

```text
chore(member-3): scaffold folders env and X-Student-Id pre-request
docs(member-3): add AI audit template
test(member-3): generate API test cases for FR-01
test(member-3): audit generated API test cases for FR-01
test(member-3): add human-designed API test cases for FR-01
test(member-3): generate API test cases for FR-09
test(member-3): audit generated API test cases for FR-09
test(member-3): add human-designed API test cases for FR-09
test(member-3): generate API test cases for FR-17
test(member-3): audit generated API test cases for FR-17
test(member-3): add human-designed API test cases for FR-17
test(member-3): implement Postman tests and Newman reports
docs(member-3): add bug reports and evidence links
ci(member-3): add newman workflow
docs(member-3): add cicd report and ai critique
feat(member-3): add api test generator skill
```

---

## 7. Bằng chứng bắt buộc (map sang file)

| Bằng chứng | File |
| --- | --- |
| Test cases + audit labels + human-added | `test-cases/member-3.xlsx` (+ csv nguồn) |
| Collection / env / DDT | `postman/` |
| Newman HTML | `newman/member-3/fr01-report.html`, `fr09-*.html`, `fr17-*.html`, `ci-report.html`, `bug-discovery-report.html` |
| Header anti-cheat | screenshot console trong `docs/` hoặc `bug-reports/` |
| Bugs | `bug-reports/member-3.md` + link Issues |
| AI Audit | `docs/ai-audit-report.md` + `docs/ai-audit-transcripts/` |
| AI Critique | `docs/ai-critique.md` (đếm 200–300 từ) |
| CI | `docs/cicd-report.md` + `.github/workflows/` |
| Skill | `agent-skill/diagram.png` (tay), `pseudocode.md`, optional code |
| Commit log | `docs/git-commit-log.txt` |
| Self-assess | `README.md` |
| Báo cáo chính | `docs/main-report.md` + PDF |

Sanity kỳ vọng **xanh** trên hành vi SUT hiện tại đã biết. Discovery **cố ý đỏ** khi spec ≠ SUT — đó là bug, không phải test hỏng. CI commit xanh chỉ chạy Sanity. Commit fail chủ đích: một assertion Sanity bị đảo, rồi revert.

---

## 8. Ràng buộc khi dùng AI (để không chết điểm)

- Không sửa SUT cho test pass. Spec là oracle.
- Không copy prompt/collection từ `khanh` / `Bao`. Pattern (sanity vs discovery, pre-request) thì học được.
- Mỗi interaction AI phải có log. Skill B giúp, không thay phiên thật.
- Diagram G9.5: mở draw.io/Excalidraw, vẽ, export PNG. Không nhờ model ra hình.
- Critique: viết sau khi đã audit và chạy Newman, dựa trên miss cụ thể của FR-01/09/17 (thường: decision table coupon, mass-assign `role`, path `/api/coupons` vs `/api/admin/coupons`).
- Vấn đáp (30%): giải thích được vì sao 5 case human-added tồn tại, và vì sao một bug là bug so với spec — không đọc lại report.

---

## 9. Definition of done — Member 3

- [ ] 3 API, mỗi API ≥ 35 AI-generated đã audit hết, ≥ 5 human-added có giải thích miss
- [ ] Mọi request mang `X-Student-Id: 23127185` + screenshot console
- [ ] Newman HTML thật, hostname local, đủ 3 API
- [ ] ≥ 1 bug thật / có Issue + screenshot (nhiều hơn nếu SUT cho)
- [ ] AI Audit đủ cột; Critique 200–300 từ
- [ ] Diagram tự vẽ + pseudocode; skill generator chạy được trên FR-09
- [ ] CI: 1 run pass, 1 run fail chủ đích, có link
- [ ] README rubric + summary counts khớp Newman
- [ ] Commit log text; ZIP đúng tên
- [ ] Không trùng bộ ba API teammate
