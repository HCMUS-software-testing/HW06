# Danh sách kiểm tra minh chứng thật

Không dùng ảnh console/Issue/Actions do AI hoặc HTML card dựng. Chỉ chụp trực tiếp giao diện thật, đủ thanh địa chỉ, tên Issue/run và nội dung then chốt.

## Ảnh chụp GitHub Issue

| File cần lưu | Trang phải chụp |
|---|---|
| ![GitHub Issue 1](github-issue-01.png) | <https://github.com/HCMUS-software-testing/HW06/issues/1> |
| ![GitHub Issue 2](github-issue-02.png) | <https://github.com/HCMUS-software-testing/HW06/issues/2> |
| ![GitHub Issue 3](github-issue-03.png) | <https://github.com/HCMUS-software-testing/HW06/issues/3> |
| ![GitHub Issue 4](github-issue-04.png) | <https://github.com/HCMUS-software-testing/HW06/issues/4> |
| ![GitHub Issue 35](github-issue-35.png) | <https://github.com/HCMUS-software-testing/HW06/issues/35> |
| ![GitHub Issue 36](github-issue-36.png) | <https://github.com/HCMUS-software-testing/HW06/issues/36> |
| ![GitHub Issue 37](github-issue-37.png) | <https://github.com/HCMUS-software-testing/HW06/issues/37> |
| ![GitHub Issue 38](github-issue-38.png) | <https://github.com/HCMUS-software-testing/HW06/issues/38> |
| ![GitHub Issue 39](github-issue-39.png) | <https://github.com/HCMUS-software-testing/HW06/issues/39> |
| ![GitHub Issue 40](github-issue-40.png) | <https://github.com/HCMUS-software-testing/HW06/issues/40> |

## Ảnh chụp execution/CI

- [x] ![Postman console](postman-console-student-id.png): ảnh chụp Postman thật, request `GET /api/users/me`, header `X-Student-Id: 23127326`, response `200 OK` và Console log.
- [x] ![Newman localhost](newman-full-localhost.png): ảnh chụp Newman HTML thật hiển thị 467 request và 839 assertion.
- [x] ![GitHub Actions pass](github-actions-pass.png): ảnh chụp trang Actions run pass của commit demo xanh.
- [x] ![GitHub Actions one failure](github-actions-one-fail.png): ảnh chụp trang Actions run đỏ của controlled-failure commit.
- [x] ![GitHub Actions full pass](github-actions-full-pass.png): ảnh chụp run [33604446982](https://github.com/HCMUS-software-testing/HW06/actions/runs/33604446982) của commit [`359841a`](https://github.com/HCMUS-software-testing/HW06/commit/359841a49691af2049fb8ca4a043ce473dce5d62), trạng thái `Success`; số liệu 467 request/839 assertion/0 fail được đối chiếu trong `ci-full-pass-report.html` và `.json`.
- [x] ![GitHub Actions full conformance](github-actions-full-conformance.png): ảnh chụp run [33498724665](https://github.com/HCMUS-software-testing/HW06/actions/runs/33498724665).

## Video demo

- [x] [DemoAgentSkill-HW06](https://youtu.be/1X8fNBIZYV0): video minh họa Agent Skill sinh test cho API.

Mười ảnh GitHub Issue trong bảng đã được chụp trực tiếp bằng trình duyệt từ đúng các URL công khai; không dùng ảnh dựng hoặc thẻ HTML giả.

Ghi chú: ảnh Newman, CI demo và full conformance là minh chứng lịch sử từ trước khi đổi tên workflow/collection sang MSSV `23127326`, vì vậy một số ảnh hiển thị “Member 4”. Ảnh `github-actions-full-pass.png` là run hiện tại của workflow `hw06-23127326.yml`. Không chỉnh sửa nội dung ảnh. Report/collection/workflow hiện tại dùng tên `23127326`.
