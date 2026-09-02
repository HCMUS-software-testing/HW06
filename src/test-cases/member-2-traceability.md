# Member 2 authoritative case traceability

This matrix is the source of truth for the 135 authored cases. `Latest result source` names a future deterministic Newman JSON target or an honest not-run reason; it does not claim PASS/FAIL. Every NEWMAN assertion ID is identical to its case ID and is reserved for Task 3.

## Authored and execution-class totals

| Metric | FR-05 | FR-08 | FR-18 | Total |
| --- | ---: | ---: | ---: | ---: |
| Authored | 45 | 45 | 45 | 135 |
| NEWMAN-automated | 35 | 29 | 40 | 104 |
| Browser-manual | 7 | 3 | 1 | 11 |
| Fault-injection | 0 | 0 | 2 | 2 |
| Excluded | 3 | 13 | 2 | 18 |

No row is counted as executed, passed, or failed in Task 2.

## FR-05 — Product list and search

| Case ID | Final intent | Execution class | Postman folder/request or manual procedure | Assertion ID | Latest result source |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | Baseline list returns 200 JSON array with required product fields. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-001 - baseline list` — GET /api/products | TC-FR05-AI-001 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-002 | Dynamically selected product name is found and every result matches it. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-002 - fixture keyword` — GET /api/products | TC-FR05-AI-002 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-003 | Unique no-match keyword returns an empty array. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-003 - no match` — GET /api/products | TC-FR05-AI-003 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-004 | Empty search is equivalent to omitted search. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-004 - empty normalization` — GET /api/products | TC-FR05-AI-004 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-005 | Special ASCII search does not 500, leak errors, or mutate state. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-005 - special ASCII` — GET /api/products | TC-FR05-AI-005 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-006 | Unique Vietnamese sentinel is handled as UTF-8 and returns empty JSON array. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-006 - Vietnamese UTF-8` — GET /api/products | TC-FR05-AI-006 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-007 | A 256-character search satisfies the non-500 JSON/state invariant. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-007 - long search` — GET /api/products | TC-FR05-AI-007 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-008 | Spaces-only search satisfies the non-500 JSON/state invariant. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-008 - spaces only` — GET /api/products | TC-FR05-AI-008 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-009 | Unique numeric name sentinel returns an empty array. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-009 - numeric sentinel` — GET /api/products | TC-FR05-AI-009 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-010 | FR-06 original is replaced by empty/omitted search normalization. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-010 - replacement normalization` — GET /api/products | TC-FR05-AI-010 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-011 | FR-06 original is replaced by duplicate-query robustness. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-011 - duplicate query` — GET /api/products | TC-FR05-AI-011 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-012 | FR-06 original is replaced by percent-decoding equivalence. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-012 - percent decoding` — GET /api/products | TC-FR05-AI-012 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-013 | FR-06 original is replaced by boolean-SQLi differential equality. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-013 - SQLi differential` — GET /api/products | TC-FR05-AI-013 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-014 | FR-06 original is replaced by search response JSON media type. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-014 - search content type` — GET /api/products | TC-FR05-AI-014 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-015 | FR-06 original is replaced by raw-query non-reflection. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-015 - raw non-reflection` — GET /api/products | TC-FR05-AI-015 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-016 | SQL tautology does not expand results or leak DB errors. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-016 - tautology cardinality` — GET /api/products | TC-FR05-AI-016 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-017 | UNION payload returns safe JSON without schema/error leakage. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-017 - union payload` — GET /api/products | TC-FR05-AI-017 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-018 | Engine-specific timing probe lacks a deterministic DB/latency contract. | EXCLUDED | `Excluded / TC-FR05-AI-018 - engine-specific timing` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR05-AI-019 | SQL comment payload does not expand results or leak errors. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-019 - SQL comment` — GET /api/products | TC-FR05-AI-019 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-020 | Script query is neither reflected in product JSON nor result-expanding. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-020 - API XSS invariant` — GET /api/products | TC-FR05-AI-020 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-021 | Event-handler keyword renders only as text with one heading and empty state. | BROWSER-MANUAL | `FR05-BROWSER-AI-021`: open search, inspect DOM/events after response | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-AI-022 | JavaScript-scheme keyword cannot navigate/execute; loading and empty state render safely. | BROWSER-MANUAL | `FR05-BROWSER-AI-022`: throttle response, inspect loading, DOM, heading, empty state | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-AI-023 | Oversized search satisfies non-500 JSON/state invariant. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-023 - oversized search` — GET /api/products | TC-FR05-AI-023 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-024 | Null-byte search does not 500 or leak paths/stacks. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-024 - null byte` — GET /api/products | TC-FR05-AI-024 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-025 | Emoji search returns valid UTF-8 empty JSON array. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-025 - emoji UTF-8` — GET /api/products | TC-FR05-AI-025 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-026 | Every product ID is a positive integer. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-026 - id schema` — GET /api/products | TC-FR05-AI-026 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-027 | Every product name is a non-empty string. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-027 - name schema` — GET /api/products | TC-FR05-AI-027 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-028 | Every price is a finite positive number. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-028 - price schema` — GET /api/products | TC-FR05-AI-028 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-029 | Every description is a string. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-029 - description schema` — GET /api/products | TC-FR05-AI-029 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-030 | Every imageUrl is a string. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-030 - image URL schema` — GET /api/products | TC-FR05-AI-030 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-031 | Every category ID is an integer. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-031 - category schema` — GET /api/products | TC-FR05-AI-031 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-032 | FR-06 detail original is replaced by required fields on list items. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-032 - replacement list schema` — GET /api/products | TC-FR05-AI-032 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-033 | Baseline media type is application/json. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-033 - baseline content type` — GET /api/products | TC-FR05-AI-033 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-034 | Unique no-match search is exactly an empty array. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-034 - empty array schema` — GET /api/products | TC-FR05-AI-034 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-035 | Product JSON recursively omits credential/internal denylist keys. | NEWMAN | `FR-05 - Product Search / TC-FR05-AI-035 - sensitive fields` — GET /api/products | TC-FR05-AI-035 | src/newman/member-2/fr-05.json |
| TC-FR05-HUMAN-001 | Blind-SQLi true/false responses are identical and non-expanding. | NEWMAN | `FR-05 - Product Search / TC-FR05-HUMAN-001 - blind SQLi pair` — GET /api/products | TC-FR05-HUMAN-001 | src/newman/member-2/fr-05.json |
| TC-FR05-HUMAN-002 | SVG keyword is text only; one heading, loading, and empty state are safe. | BROWSER-MANUAL | `FR05-BROWSER-HUMAN-002`: inspect DOM and event execution; API half is AI-015 | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-HUMAN-003 | Two different search parameters do not crash, leak, or mutate. | NEWMAN | `FR-05 - Product Search / TC-FR05-HUMAN-003 - HPP pair` — GET /api/products | TC-FR05-HUMAN-003 | src/newman/member-2/fr-05.json |
| TC-FR05-HUMAN-004 | Historical product-detail path probe is FR-06, not final FR-05. | EXCLUDED | `Excluded / TC-FR05-HUMAN-004 - FR-06 path probe` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR05-HUMAN-005 | Historical list/detail consistency check crosses into FR-06. | EXCLUDED | `Excluded / TC-FR05-HUMAN-005 - FR-06 consistency` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR05-HUMAN-006 | Empty and SQLi searches render as safe text with stable page states. | BROWSER-MANUAL | `FR05-BROWSER-HUMAN-006`: inspect both renders; API halves are AI-010 and AI-016 | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-HUMAN-007 | Whitespace plus image-event payload cannot create executable DOM. | BROWSER-MANUAL | `FR05-BROWSER-HUMAN-007`: inspect normalized text, DOM events, heading, empty state | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-HUMAN-008 | Empty-plus-SVG duplicate query is non-reflecting and non-expanding. | NEWMAN | `FR-05 - Product Search / TC-FR05-HUMAN-008 - HPP XSS pair` — GET /api/products | TC-FR05-HUMAN-008 | src/newman/member-2/fr-05.json |
| TC-FR05-HUMAN-009 | Decoded SQLi/script keyword remains text and creates no executable DOM. | BROWSER-MANUAL | `FR05-BROWSER-HUMAN-009`: inspect decoded DOM; API halves are AI-012/013/015 | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR05-HUMAN-010 | Empty/omitted searches have equal data and safe heading/loading rendering. | BROWSER-MANUAL | `FR05-BROWSER-HUMAN-010`: compare browser states; API half is AI-010 | — | `NOT-RUN-BROWSER-MANUAL` |

## FR-08 — Checkout

| Case ID | Final intent | Execution class | Postman folder/request or manual procedure | Assertion ID | Latest result source |
| --- | --- | --- | --- | --- | --- |
| TC-FR08-AI-001 | Isolated populated cart checks out once at exact server total. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-001 - successful checkout` — POST /api/checkout | TC-FR08-AI-001 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-002 | Isolated empty cart returns 400 with no order. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-002 - empty cart` — POST /api/checkout | TC-FR08-AI-002 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-003 | Out-of-stock setup is not observable or mutable through the public contract. | EXCLUDED | `Excluded / TC-FR08-AI-003 - stock setup unavailable` | — | `NOT-RUN-NO-SUT-HOOK` |
| TC-FR08-AI-004 | Empty shipping address returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-004 - empty address` — POST /api/checkout | TC-FR08-AI-004 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-005 | Whitespace-only shipping address returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-005 - whitespace address` — POST /api/checkout | TC-FR08-AI-005 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-006 | Missing shipping_address returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-006 - missing address` — POST /api/checkout | TC-FR08-AI-006 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-007 | Null shipping_address returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-007 - null address` — POST /api/checkout | TC-FR08-AI-007 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-008 | Object shipping_address returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-008 - object address` — POST /api/checkout | TC-FR08-AI-008 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-009 | Client total 1 is ignored in favor of exact cart total. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-009 - tampered total` — POST /api/checkout | TC-FR08-AI-009 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-010 | SAVE10 coupon assumptions belong to FR-09. | EXCLUDED | `Excluded / TC-FR08-AI-010 - FR-09 percentage coupon` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-011 | BIGBUY coupon assumptions belong to FR-09. | EXCLUDED | `Excluded / TC-FR08-AI-011 - FR-09 fixed coupon` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-012 | Expired coupon assumptions belong to FR-09. | EXCLUDED | `Excluded / TC-FR08-AI-012 - FR-09 expired coupon` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-013 | Minimum-order coupon rule belongs to FR-09. | EXCLUDED | `Excluded / TC-FR08-AI-013 - FR-09 minimum` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-014 | Per-user coupon limit belongs to FR-09. | EXCLUDED | `Excluded / TC-FR08-AI-014 - FR-09 usage limit` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-015 | Unknown coupon behavior lacks a selected contract. | EXCLUDED | `Excluded / TC-FR08-AI-015 - FR-09 unknown coupon` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-016 | Successful checkout creates one order and clears its isolated cart. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-016 - cart cleared` — POST /api/checkout | TC-FR08-AI-016 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-017 | New order starts in pending state. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-017 - initial pending` — POST /api/checkout | TC-FR08-AI-017 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-018 | Notes field persistence is absent from the checkout contract. | EXCLUDED | `Excluded / TC-FR08-AI-018 - notes field` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-019 | Missing authorization returns 401 without cart/order mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-019 - missing auth` — POST /api/checkout | TC-FR08-AI-019 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-020 | Invalid JWT returns 401 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-020 - invalid JWT` — POST /api/checkout | TC-FR08-AI-020 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-021 | Expired JWT returns 401 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-021 - expired JWT` — POST /api/checkout | TC-FR08-AI-021 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-022 | Empty bearer returns 401 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-022 - empty bearer` — POST /api/checkout | TC-FR08-AI-022 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-023 | Token A checks out only cart A; cart/order B stays unchanged. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-023 - cart ownership` — POST /api/checkout | TC-FR08-AI-023 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-024 | SQL-like address round-trips literally without SQL errors. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-024 - address literal` — POST /api/checkout | TC-FR08-AI-024 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-025 | Script-like address renders as text in the order/admin browser view. | BROWSER-MANUAL | `FR08-BROWSER-AI-025`: create isolated order, inspect rendered address DOM | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR08-AI-026 | GET method probe is outside selected POST execution scope. | EXCLUDED | `Excluded / TC-FR08-AI-026 - unsupported method` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-027 | Malformed JSON returns 400 without mutation. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-027 - malformed JSON` — POST /api/checkout | TC-FR08-AI-027 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-028 | Unknown role-field policy is not specified for checkout. | EXCLUDED | `Excluded / TC-FR08-AI-028 - unknown role field` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-AI-029 | Negative client total is ignored; exact server total wins. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-029 - negative client total` — POST /api/checkout | TC-FR08-AI-029 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-030 | String client total is ignored; exact server total wins. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-030 - string client total` — POST /api/checkout | TC-FR08-AI-030 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-031 | Exactly one persisted order has a positive ID independent of response alias. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-031 - persisted order ID` — POST /api/checkout | TC-FR08-AI-031 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-032 | Persisted order status is pending. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-032 - pending schema` — POST /api/checkout | TC-FR08-AI-032 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-033 | Persisted total is finite, positive, and equal to server cart total. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-033 - total schema` — POST /api/checkout | TC-FR08-AI-033 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-034 | Successful response media type is application/json. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-034 - content type` — POST /api/checkout | TC-FR08-AI-034 | src/newman/member-2/fr-08.json |
| TC-FR08-AI-035 | Client total zero is ignored for a non-empty cart. | NEWMAN | `FR-08 - Checkout / TC-FR08-AI-035 - zero client total` — POST /api/checkout | TC-FR08-AI-035 | src/newman/member-2/fr-08.json |
| TC-FR08-HUMAN-001 | Browser session B empties cart before releasing session A checkout. | BROWSER-MANUAL | `FR08-BROWSER-HUMAN-001`: two-tab READY/RELEASE barrier and network/order inspection | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR08-HUMAN-002 | Last-stock race has no public stock field/mutation hook. | EXCLUDED | `Excluded / TC-FR08-HUMAN-002 - stock reaches zero` | — | `NOT-RUN-NO-SUT-HOOK` |
| TC-FR08-HUMAN-003 | Browser double-click produces exactly one order and an empty cart. | BROWSER-MANUAL | `FR08-BROWSER-HUMAN-003`: double-click behind READY barrier; inspect both requests | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR08-HUMAN-004 | Coupon-array behavior belongs to FR-09. | EXCLUDED | `Excluded / TC-FR08-HUMAN-004 - coupon array` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR08-HUMAN-005 | Cart changes after client reads total; checkout uses new server total. | NEWMAN | `FR-08 - Checkout / TC-FR08-HUMAN-005 - stale client total` — POST /api/checkout | TC-FR08-HUMAN-005 | src/newman/member-2/fr-08.json |
| TC-FR08-HUMAN-006 | Session B confirms empty cart before releasing A checkout; no order is created. | NEWMAN | `FR-08 - Checkout / TC-FR08-HUMAN-006 - emptied cart barrier` — POST /api/checkout | TC-FR08-HUMAN-006 | src/newman/member-2/fr-08.json |
| TC-FR08-HUMAN-007 | Inter-user last-stock race has no public stock hook. | EXCLUDED | `Excluded / TC-FR08-HUMAN-007 - last stock race` | — | `NOT-RUN-NO-SUT-HOOK` |
| TC-FR08-HUMAN-008 | Two simultaneous POSTs create at most one order for one cart snapshot. | NEWMAN | `FR-08 - Checkout / TC-FR08-HUMAN-008 - simultaneous checkout` — POST /api/checkout | TC-FR08-HUMAN-008 | src/newman/member-2/fr-08.json |
| TC-FR08-HUMAN-009 | Session B removes last cart item before releasing A; checkout returns 400. | NEWMAN | `FR-08 - Checkout / TC-FR08-HUMAN-009 - last item removed` — POST /api/checkout | TC-FR08-HUMAN-009 | src/newman/member-2/fr-08.json |
| TC-FR08-HUMAN-010 | Concurrent cart update cannot mix stale total with current snapshot. | NEWMAN | `FR-08 - Checkout / TC-FR08-HUMAN-010 - snapshot consistency` — POST /api/checkout | TC-FR08-HUMAN-010 | src/newman/member-2/fr-08.json |

## FR-18 — Admin order management

| Case ID | Final intent | Execution class | Postman folder/request or manual procedure | Assertion ID | Latest result source |
| --- | --- | --- | --- | --- | --- |
| TC-FR18-AI-001 | Admin list contains orders from two isolated users. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-001 - admin list` — GET /api/admin/orders | TC-FR18-AI-001 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-002 | User token gets 403 and no admin-order data. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-002 - user list denied` — GET /api/admin/orders | TC-FR18-AI-002 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-003 | Missing authorization gets 401 and no order data. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-003 - missing list auth` — GET /api/admin/orders | TC-FR18-AI-003 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-004 | Invalid JWT gets 401 and no order data. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-004 - invalid list JWT` — GET /api/admin/orders | TC-FR18-AI-004 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-005 | Expired admin JWT gets 401 and no order data. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-005 - expired list JWT` — GET /api/admin/orders | TC-FR18-AI-005 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-006 | Fresh pending order transitions to confirmed. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-006 - pending confirmed` — PUT /api/admin/orders/:id/status | TC-FR18-AI-006 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-007 | User mutation gets 403 and pending snapshot remains unchanged. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-007 - user mutation denied` — PUT /api/admin/orders/:id/status | TC-FR18-AI-007 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-008 | Missing mutation auth gets 401 and snapshot remains unchanged. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-008 - missing mutation auth` — PUT /api/admin/orders/:id/status | TC-FR18-AI-008 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-009 | Empty bearer gets 401 and snapshot remains unchanged. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-009 - empty bearer` — PUT /api/admin/orders/:id/status | TC-FR18-AI-009 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-010 | Malformed JSON gets 400 and pending snapshot remains unchanged. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-010 - malformed JSON` — PUT /api/admin/orders/:id/status | TC-FR18-AI-010 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-011 | User JWT plus X-Role admin still gets 403. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-011 - forged role header` — GET /api/admin/orders | TC-FR18-AI-011 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-012 | Captured order details are validated inside the documented list response. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-012 - list item fields` — GET /api/admin/orders | TC-FR18-AI-012 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-013 | Script-like shipping address renders as text in admin UI. | BROWSER-MANUAL | `FR18-BROWSER-AI-013`: seed marked order and inspect admin order DOM | — | `NOT-RUN-BROWSER-MANUAL` |
| TC-FR18-AI-014 | Profile role assignment cannot grant access to admin list. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-014 - profile escalation chain` — GET /api/admin/orders | TC-FR18-AI-014 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-015 | Tampered user JWT with admin payload gets 401. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-015 - tampered role JWT` — GET /api/admin/orders | TC-FR18-AI-015 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-016 | Fresh confirmed order transitions to shipping. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-016 - confirmed shipping` — PUT /api/admin/orders/:id/status | TC-FR18-AI-016 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-017 | Fresh shipping order transitions to delivered. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-017 - shipping delivered` — PUT /api/admin/orders/:id/status | TC-FR18-AI-017 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-018 | Fresh pending order transitions to canceled without stock claim. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-018 - pending canceled` — PUT /api/admin/orders/:id/status | TC-FR18-AI-018 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-019 | Pending to confirmed follows allowed state machine. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-019 - state pending confirmed` — PUT /api/admin/orders/:id/status | TC-FR18-AI-019 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-020 | Confirmed to shipping follows allowed state machine. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-020 - state confirmed shipping` — PUT /api/admin/orders/:id/status | TC-FR18-AI-020 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-021 | Shipping to delivered follows allowed state machine. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-021 - state shipping delivered` — PUT /api/admin/orders/:id/status | TC-FR18-AI-021 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-022 | Pending to canceled follows allowed state machine. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-022 - state pending canceled` — PUT /api/admin/orders/:id/status | TC-FR18-AI-022 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-023 | Confirmed to canceled follows allowed state machine. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-023 - state confirmed canceled` — PUT /api/admin/orders/:id/status | TC-FR18-AI-023 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-024 | Delivered to pending is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-024 - reject delivered pending` — PUT /api/admin/orders/:id/status | TC-FR18-AI-024 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-025 | Delivered to canceled is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-025 - reject delivered canceled` — PUT /api/admin/orders/:id/status | TC-FR18-AI-025 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-026 | Canceled to shipping is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-026 - reject canceled shipping` — PUT /api/admin/orders/:id/status | TC-FR18-AI-026 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-027 | Canceled to delivered is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-027 - reject canceled delivered` — PUT /api/admin/orders/:id/status | TC-FR18-AI-027 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-028 | Delivered to confirmed is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-028 - reject delivered confirmed` — PUT /api/admin/orders/:id/status | TC-FR18-AI-028 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-029 | Unknown status is rejected 400 with unchanged snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-029 - reject unknown status` — PUT /api/admin/orders/:id/status | TC-FR18-AI-029 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-030 | Nonexistent positive order ID gets 404 without control mutation. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-030 - missing order` — PUT /api/admin/orders/:id/status | TC-FR18-AI-030 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-031 | Negative ID satisfies non-500 JSON and unchanged-control invariant. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-031 - negative ID` — PUT /api/admin/orders/:id/status | TC-FR18-AI-031 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-032 | Alphabetic ID satisfies non-500 JSON and unchanged-control invariant. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-032 - alphabetic ID` — PUT /api/admin/orders/:id/status | TC-FR18-AI-032 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-033 | Order ID zero gets 404 without control mutation. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-033 - zero ID` — PUT /api/admin/orders/:id/status | TC-FR18-AI-033 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-034 | Missing status gets 400 with unchanged pending snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-034 - missing status` — PUT /api/admin/orders/:id/status | TC-FR18-AI-034 | src/newman/member-2/fr-18.json |
| TC-FR18-AI-035 | JSON null gets 400 with unchanged pending snapshot. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-AI-035 - JSON null` — PUT /api/admin/orders/:id/status | TC-FR18-AI-035 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-001 | User token cannot cancel a shipping order through admin mutation. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-001 - user shipping cancel denied` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-001 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-002 | Same-state confirmed request is rejected 400 and unchanged. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-002 - reject same state` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-002 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-003 | Inventory restoration cannot be observed through public stock APIs. | EXCLUDED | `Excluded / TC-FR18-HUMAN-003 - inventory restoration` | — | `NOT-RUN-NO-SUT-HOOK` |
| TC-FR18-HUMAN-004 | Admin status update cannot mass-assign non-status order fields. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-004 - status mass assignment` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-004 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-005 | Multi-tenant store authorization is absent from the contract. | EXCLUDED | `Excluded / TC-FR18-HUMAN-005 - undocumented tenancy` | — | `NOT-RUN-CONTRACT-EXCLUDED` |
| TC-FR18-HUMAN-006 | Profile role assignment followed by admin mutation still gets 403 and no mutation. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-006 - profile to mutation chain` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-006 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-007 | alg:none and invalid-kid forged tokens each get 401 with unchanged order. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-007 - forged JWT variants` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-007 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-008 | User token plus admin-looking body gets 403 before mutation. | NEWMAN | `FR-18 - Admin Orders / TC-FR18-HUMAN-008 - authz before body` — PUT /api/admin/orders/:id/status | TC-FR18-HUMAN-008 | src/newman/member-2/fr-18.json |
| TC-FR18-HUMAN-009 | Audit/event failure must roll back confirmed-to-shipping transaction. | FAULT-INJECTION | `FR18-FAULT-HUMAN-009`: enable deterministic post-state/pre-event failure hook, then compare snapshots | — | `NOT-RUN-NO-SUT-HOOK` |
| TC-FR18-HUMAN-010 | Inventory-restoration failure must roll back confirmed-to-canceled transaction. | FAULT-INJECTION | `FR18-FAULT-HUMAN-010`: enable deterministic stock-write failure hook, then compare snapshots | — | `NOT-RUN-NO-SUT-HOOK` |
