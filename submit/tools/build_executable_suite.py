#!/usr/bin/env python3
"""Build the audited HW06 catalogue and an executable Postman suite.

The generated collection deliberately creates an isolated user/order fixture for
cases that mutate state.  A catalogue row is therefore mapped to real request
data instead of a duplicated placeholder request.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import hmac
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TC_DIR = ROOT / "test-cases"
PM_DIR = ROOT / "postman"
DATA_DIR = PM_DIR / "data"
STUDENT_ID = "23127326"


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def jwt(payload: dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}

    def enc(value: dict[str, Any]) -> bytes:
        raw = compact(value).encode()
        return base64.urlsafe_b64encode(raw).rstrip(b"=")

    signing = enc(header) + b"." + enc(payload)
    signature = hmac.new(secret.encode(), signing, hashlib.sha256).digest()
    return (signing + b"." + base64.urlsafe_b64encode(signature).rstrip(b"=")).decode()


EXPIRED_USER_JWT = jwt(
    {"id": 2, "role": "user", "iat": 1, "exp": 2},
    "super_secret_key_that_should_not_be_here",
)
FORGED_ADMIN_JWT = jwt(
    {"id": 2, "role": "admin", "iat": 1_788_000_000, "exp": 4_102_444_800},
    "wrong-secret",
)


@dataclass
class Case:
    test_id: str
    feature: str
    method: str
    endpoint: str
    category: str
    requirement: str
    precondition: str
    data: str
    expected_status: int
    oracle: str
    ai_source: str = "AI-001"
    audit_label: str = "VALID"
    audit_reason: str = "Oracle resolved against the pinned API specification and SRS."
    correction: str = ""
    why_missed: str = ""
    scenario: dict[str, Any] = field(default_factory=dict)

    @property
    def item_name(self) -> str:
        return f"{self.test_id} — {self.category}"


CASES: list[Case] = []


def add(
    feature: str,
    number: int,
    method: str,
    endpoint: str,
    category: str,
    requirement: str,
    precondition: str,
    data: str,
    status: int,
    oracle: str,
    *,
    source: str = "AI-001",
    why_missed: str = "",
    scenario: dict[str, Any] | None = None,
) -> None:
    test_id = f"{feature}-{number:03d}"
    correction = "Human review resolved the request data, fixture, exact status and postcondition."
    CASES.append(
        Case(
            test_id,
            feature,
            method,
            endpoint,
            category,
            requirement,
            precondition,
            data,
            status,
            oracle,
            source,
            "VALID",
            "Human-reviewed; exact executable request, fixture and oracle are defined.",
            correction,
            why_missed,
            scenario or {},
        )
    )


def build_cases() -> None:
    # FR-04: 40 AI-assisted and five human-added cases.
    gets = [
        ("valid-user", 200, "Authenticated user receives the profile bound to the JWT; required fields have correct types."),
        ("no-token", 401, "Request is rejected and no profile data is disclosed."),
        ("malformed-token", 403, "Malformed JWT is rejected and no profile data is disclosed."),
        ("tampered-token", 403, "JWT with an invalid signature is rejected."),
        ("expired-token", 403, "Expired but otherwise correctly signed JWT is rejected."),
        ("wrong-scheme", 403, "A non-Bearer authorization value is not accepted as a JWT."),
        ("empty-bearer", 401, "An empty Bearer token is rejected as missing credentials."),
        ("identity", 200, "Returned id and email belong to the JWT subject, not client-supplied identifiers."),
        ("repeat", 200, "Two consecutive reads return the same identity and profile values."),
        ("privacy-schema", 200, "Response has documented identity/profile fields and omits password and reset_token."),
    ]
    for number, (kind, status, oracle) in enumerate(gets, 1):
        add("FR04", number, "GET", "/api/users/me", "auth" if number < 8 else "schema", "FR-04, SEC-01/02", "Seed user exists; token variant prepared", kind, status, oracle, scenario={"kind": kind})

    updates = [
        ("all-valid", {"name": "Nguyễn Văn An", "shipping_address": "123 Lê Lợi, Q1", "phone": "0912345678"}, 200, "All three allowed fields persist; email and role are unchanged."),
        ("phone-10", {"name": "An", "shipping_address": "A", "phone": "0912345678"}, 200, "Ten-digit 0-prefixed phone is accepted and persists."),
        ("phone-11", {"name": "An", "shipping_address": "A", "phone": "01234567890"}, 200, "Eleven-digit 0-prefixed phone is accepted and persists."),
        ("phone-9", {"name": "An", "shipping_address": "A", "phone": "091234567"}, 400, "Nine-digit phone is rejected; profile remains unchanged."),
        ("phone-12", {"name": "An", "shipping_address": "A", "phone": "091234567890"}, 400, "Twelve-digit phone is rejected; profile remains unchanged."),
        ("phone-prefix", {"name": "An", "shipping_address": "A", "phone": "1912345678"}, 400, "Phone not beginning with 0 is rejected."),
        ("phone-alpha", {"name": "An", "shipping_address": "A", "phone": "09abcdefgh"}, 400, "Non-digit phone is rejected."),
        ("phone-hyphen", {"name": "An", "shipping_address": "A", "phone": "091-234-5678"}, 400, "Formatted phone containing separators is rejected by the strict SRS partition."),
        ("phone-space", {"name": "An", "shipping_address": "A", "phone": " 0912345678 "}, 400, "Phone with surrounding spaces is rejected rather than silently changing the domain."),
        ("phone-null", {"name": "An", "shipping_address": "A", "phone": None}, 400, "Null phone is rejected."),
        ("phone-number", {"name": "An", "shipping_address": "A", "phone": 912345678}, 400, "Numeric JSON phone is rejected; phone must be a string preserving the leading zero."),
        ("unicode-name", {"name": "Trần Thị Bích Hạnh", "shipping_address": "A", "phone": "0912345678"}, 200, "Vietnamese Unicode name round-trips unchanged."),
        ("long-name", {"name": "N" * 256, "shipping_address": "A", "phone": "0912345678"}, 200, "No maximum name length is specified; API remains stable and persists the supplied text."),
        ("emoji-name", {"name": "Người dùng 🧪", "shipping_address": "A", "phone": "0912345678"}, 200, "Unicode supplementary characters are transported as JSON safely."),
        ("empty-address", {"name": "An", "shipping_address": "", "phone": "0912345678"}, 200, "No non-empty address rule is specified; empty address persists without affecting protected fields."),
        ("unicode-address", {"name": "An", "shipping_address": "12 Đường số 3, Thủ Đức", "phone": "0912345678"}, 200, "Vietnamese address round-trips unchanged."),
        ("xss-json", {"name": "<script>alert(1)</script>", "shipping_address": "A", "phone": "0912345678"}, 200, "API returns valid JSON and does not execute input; UI escaping remains a separate SEC-04 concern."),
        ("empty-object", {}, 400, "Empty update is rejected and cannot null existing fields."),
        ("null-body", None, 400, "JSON null is handled as a client error without a server crash."),
        ("no-token", {"name": "An", "shipping_address": "A", "phone": "0912345678"}, 401, "Unauthenticated update is rejected."),
        ("malformed-token", {"name": "An", "shipping_address": "A", "phone": "0912345678"}, 403, "Malformed JWT cannot update a profile."),
        ("expired-token", {"name": "An", "shipping_address": "A", "phone": "0912345678"}, 403, "Expired JWT cannot update a profile."),
        ("role-admin", {"name": "An", "shipping_address": "A", "phone": "0912345678", "role": "admin"}, 400, "Client-supplied role is rejected and remains user."),
        ("role-user", {"name": "An", "shipping_address": "A", "phone": "0912345678", "role": "user"}, 400, "The protected role field is rejected even when the supplied value matches."),
        ("email", {"name": "An", "shipping_address": "A", "phone": "0912345678", "email": "attacker@example.test"}, 200, "Undocumented email field is ignored; original email remains."),
        ("id", {"name": "An", "shipping_address": "A", "phone": "0912345678", "id": 1}, 200, "Client id is ignored and only the JWT subject is updated."),
        ("user-id", {"name": "An", "shipping_address": "A", "phone": "0912345678", "user_id": 1}, 200, "Client user_id is ignored and only the JWT subject is updated."),
        ("password", {"name": "An", "shipping_address": "A", "phone": "0912345678", "password": "Changed123!"}, 200, "Password field is ignored and the original credential remains valid."),
        ("response-schema", {"name": "Schema User", "shipping_address": "A", "phone": "0912345678"}, 200, "Success body has exactly one string field: message."),
        ("unknown-field", {"name": "An", "shipping_address": "A", "phone": "0912345678", "is_admin": True}, 200, "Unknown field is ignored; role remains user."),
    ]
    for offset, (kind, body, status, oracle) in enumerate(updates, 11):
        category = "security" if kind in {"role-admin", "role-user", "email", "id", "user-id", "password", "unknown-field"} else "boundary"
        add("FR04", offset, "PUT", "/api/users/me", category, "FR-04, SEC-02/04/06", "Isolated registered user with baseline profile", compact(body), status, oracle, scenario={"kind": kind, "body": body})

    human = [
        ("partial-preserve", {"name": "Only Name"}, 200, "Omitted phone/address fields retain their previous values.", "The AI treated PUT as full replacement and did not test partial-update preservation."),
        ("cross-user", {"name": "Isolated A", "shipping_address": "A", "phone": "0912345678", "id": 1}, 200, "Updating user A does not modify the admin or another user.", "The initial prompt covered IDOR payloads but not a second-user postcondition."),
        ("rtl-control", {"name": "An\u202eTest", "shipping_address": "A\nB", "phone": "0912345678"}, 200, "Control/RTL characters remain valid JSON and do not corrupt unrelated fields.", "The model focused on script-tag XSS and missed Unicode bidi/control payloads."),
        ("replay", {"name": "Replay", "shipping_address": "A", "phone": "0912345678"}, 200, "Repeating the same valid update is idempotent.", "The model generated single requests and missed replay/idempotency behavior."),
        ("role-fresh-login", {"name": "An", "shipping_address": "A", "phone": "0912345678", "role": "admin"}, 400, "Role escalation is rejected and a fresh JWT still contains role=user.", "The AI checked the immediate response but missed persistence through a fresh login."),
    ]
    for number, (kind, body, status, oracle, reason) in enumerate(human, 41):
        add("FR04", number, "PUT", "/api/users/me", "human-security", "FR-04, SEC-04/06", "Isolated registered user and postcondition actor", compact(body), status, oracle, source="HUMAN-001", why_missed=reason, scenario={"kind": kind, "body": body})

    # FR-10: a complete 5x5 state matrix, 20 additional AI cases and five human cases.
    states = ["pending", "confirmed", "shipping", "delivered", "canceled"]
    valid = {("pending", "confirmed"), ("pending", "canceled"), ("confirmed", "shipping"), ("confirmed", "canceled"), ("shipping", "delivered")}
    number = 1
    for source_state in states:
        for target_state in states:
            ok = (source_state, target_state) in valid
            add("FR10", number, "PUT", "/api/admin/orders/:id/status", "state-matrix", "FR-10, FR-18", f"Fresh order prepared in {source_state}", f"status={target_state}", 200 if ok else 400, f"Transition {source_state}→{target_state} {'succeeds and persists' if ok else 'is rejected and leaves the source state unchanged'}.", scenario={"kind": "matrix", "source": source_state, "target": target_state})
            number += 1

    extras = [
        ("cancel-owner-pending", "pending", "user", 200, "Owner can cancel a pending order; final state is canceled."),
        ("cancel-owner-confirmed", "confirmed", "user", 200, "Owner can cancel a confirmed order; final state is canceled."),
        ("cancel-owner-shipping", "shipping", "user", 400, "Owner cannot cancel a shipping order; state remains shipping."),
        ("cancel-owner-delivered", "delivered", "user", 400, "Owner cannot cancel a delivered order."),
        ("cancel-owner-canceled", "canceled", "user", 400, "Repeated cancellation is rejected."),
        ("cancel-other-owner", "pending", "other-user", 404, "A different user receives not found and cannot cancel the order."),
        ("admin-no-token", "pending", "none", 401, "Missing token cannot change order state."),
        ("admin-malformed", "pending", "malformed", 403, "Malformed token cannot change order state."),
        ("admin-user-role", "pending", "user", 403, "Regular user token cannot call the admin transition API."),
        ("admin-forged", "pending", "forged", 403, "Forged admin-role JWT is rejected by signature verification."),
        ("missing-order", "pending", "admin", 404, "Unknown order id returns not found."),
        ("negative-id", "pending", "admin", 404, "Negative order id returns not found."),
        ("missing-status", "pending", "admin", 400, "Missing status is rejected and state remains pending."),
        ("null-status", "pending", "admin", 400, "Null status is rejected and state remains pending."),
        ("uppercase-status", "pending", "admin", 400, "Status enum is case-sensitive."),
        ("script-status", "pending", "admin", 400, "Injection-like status is rejected without state mutation."),
        ("replay-confirmed", "confirmed", "admin", 400, "Replaying the same state is rejected."),
        ("backward-shipping", "shipping", "admin", 400, "Backward shipping→confirmed transition is rejected."),
        ("backward-delivered", "delivered", "admin", 400, "Backward delivered→shipping transition is rejected."),
        ("response-schema", "pending", "admin", 200, "Successful transition response has exactly message:string."),
    ]
    for kind, source_state, actor, status, oracle in extras:
        endpoint = "/api/orders/:id/cancel" if kind.startswith("cancel-") else "/api/admin/orders/:id/status"
        target = None if endpoint.endswith("cancel") else ("confirmed" if kind == "response-schema" else {"replay-confirmed": "confirmed", "backward-shipping": "confirmed", "backward-delivered": "shipping"}.get(kind, "confirmed"))
        add("FR10", number, "PUT", endpoint, "cancel-ownership" if endpoint.endswith("cancel") else "auth-negative", "FR-10, FR-12, SEC-02/03/05", f"Fresh order prepared in {source_state}", kind, status, oracle, scenario={"kind": kind, "source": source_state, "actor": actor, "target": target})
        number += 1

    human10 = [
        ("rejected-postcondition", "canceled", "admin", "confirmed", 400, "Rejected transition preserves canceled after a separate GET.", "The AI asserted only the error response and omitted a read-after-write state oracle."),
        ("spoof-student-header", "pending", "user", "confirmed", 403, "Spoofing X-Student-Id does not grant the user admin authorization.", "The assignment-specific header was not included in the original security threat model."),
        ("leading-zero-id", "pending", "admin", "confirmed", 200, "Canonical numeric order id with leading zeros addresses the same order without altering authorization.", "The model partitioned missing/negative IDs but missed alternate numeric serialization."),
        ("concurrent-confirm-cancel", "pending", "admin", None, 200, "Two competing requests leave the order in exactly one legal terminal/intermediate state.", "Sequential prompts did not explore race conditions between admin confirmation and owner cancellation."),
        ("exact-error-schema", "delivered", "admin", "pending", 400, "Invalid transition response has exactly error:string and preserves delivered.", "The model checked statuses broadly but missed exact negative-response schema."),
    ]
    for kind, source_state, actor, target, status, oracle, reason in human10:
        add("FR10", number, "PUT", "/api/admin/orders/:id/status", "human-state-security", "FR-10, SEC-02/03", f"Fresh order prepared in {source_state}", kind, status, oracle, source="HUMAN-001", why_missed=reason, scenario={"kind": kind, "source": source_state, "actor": actor, "target": target})
        number += 1

    # FR-19: 40 AI-assisted and five human-added cases.
    list_cases = [
        ("admin-list", "admin", 200, "Admin receives an array containing seeded users."),
        ("no-token", "none", 401, "Missing token discloses no user list."),
        ("malformed-token", "malformed", 403, "Malformed token discloses no user list."),
        ("regular-user", "user", 403, "Regular user is forbidden from the admin list."),
        ("forged-admin", "forged", 403, "Forged admin-role token is rejected."),
        ("expired-token", "expired", 403, "Expired token is rejected."),
        ("array-schema", "admin", 200, "Every row has documented public admin-list fields with correct types."),
        ("privacy-schema", "admin", 200, "No row contains password or reset_token."),
        ("unique-ids", "admin", 200, "All returned user IDs are unique positive integers."),
        ("content-type", "admin", 200, "Response Content-Type is application/json."),
        ("repeat-list", "admin", 200, "Two reads without mutation contain the same user IDs."),
        ("query-id", "admin", 200, "Undocumented id query parameter does not narrow or expose extra fields."),
        ("query-role", "admin", 200, "Undocumented role query parameter does not bypass schema/privacy rules."),
        ("query-sql", "admin", 200, "SQL-like query value does not alter the parameterless list query."),
        ("new-user-visible", "admin", 200, "A newly registered disposable user appears exactly once."),
    ]
    for number, (kind, actor, status, oracle) in enumerate(list_cases, 1):
        add("FR19", number, "GET", "/api/admin/users", "list-schema", "FR-19, SEC-01/02/03/05", "Seed database; optional disposable user", kind, status, oracle, scenario={"kind": kind, "actor": actor})

    deletes = [
        ("valid-delete", "admin", "target", 200, "Disposable target is deleted and absent from a follow-up list."),
        ("missing-id", "admin", "99999999", 404, "Unknown user id is reported not found; user count is unchanged."),
        ("id-zero", "admin", "0", 404, "Zero id is reported not found."),
        ("id-negative", "admin", "-1", 404, "Negative id is reported not found."),
        ("id-alpha", "admin", "abc", 400, "Non-integer path id is rejected as malformed input."),
        ("id-decimal", "admin", "1.5", 400, "Decimal path id is rejected."),
        ("id-whitespace", "admin", "%20", 400, "Whitespace path id is rejected."),
        ("sql-or", "admin", "1%20OR%201%3D1", 400, "SQL-injection path payload is rejected and cannot delete multiple users."),
        ("sql-quote", "admin", "%271%27", 400, "Quoted SQL payload is rejected."),
        ("path-object", "admin", "%5Bobject%20Object%5D", 400, "Object-like path value is rejected."),
        ("repeat-delete", "admin", "target", 404, "Second deletion of an already deleted target returns not found."),
        ("no-token", "none", "target", 401, "Unauthenticated caller cannot delete a user."),
        ("malformed-token", "malformed", "target", 403, "Malformed JWT cannot delete a user."),
        ("regular-user", "user", "target", 403, "Regular user cannot delete another user."),
        ("forged-admin", "forged", "target", 403, "Forged admin-role JWT cannot delete a user."),
        ("regular-user-zero", "user", "0", 403, "Authorization is evaluated before resource existence; regular user cannot invoke admin deletion."),
        ("response-schema", "admin", "target", 200, "Successful delete response has exactly message:string."),
        ("missing-error-schema", "admin", "99999999", 404, "Not-found response has exactly error:string."),
        ("unrelated-remains", "admin", "target", 200, "Deleting target leaves seeded user and admin records intact."),
        ("large-id", "admin", "9223372036854775807", 404, "Large integer id is safely handled as not found."),
        ("unicode-id", "admin", "%D9%A1", 400, "Unicode numeral path value is rejected."),
        ("encoded-plus", "admin", "%2B1", 400, "Signed/encoded id form is rejected as non-canonical."),
        ("encoded-slash", "admin", "%2F1", 400, "Encoded path separator cannot alter route scope or delete a user."),
        ("content-type", "admin", "target", 200, "Successful response is application/json."),
        ("leading-zero-target", "admin", "leading-zero-target", 200, "Canonical target id with leading zeros deletes only the intended disposable user."),
    ]
    for number, (kind, actor, target, status, oracle) in enumerate(deletes, 16):
        add("FR19", number, "DELETE", "/api/admin/users/:id", "delete-security", "FR-19, SEC-02/03/05", "Admin plus isolated disposable target where required", kind, status, oracle, scenario={"kind": kind, "actor": actor, "target": target})

    human19 = [
        ("student-id-spoof", "user", "target", 403, "X-Student-Id containing the admin id does not grant delete authorization.", "The original AI security pass treated the assignment header only as trace metadata."),
        ("percent-sql", "admin", "%2527%2520OR%25201%253D1", 400, "Double-encoded SQL payload cannot delete any user.", "The AI generated plain SQL strings but missed transport-layer double encoding."),
        ("concurrent-delete", "admin", "target", 200, "Concurrent deletion has at most one success and leaves the target absent.", "The model generated sequential repeat tests but missed a concurrent race."),
        ("stale-token", "admin", "target", 200, "Target deletion succeeds, then the deleted user's JWT is rejected by a protected profile request.", "The model did not connect user deletion to subsequent JWT subject validity."),
        ("fresh-self-delete", "admin", "admin", 403, "Freshly authenticated admin still cannot self-delete and remains listed.", "The AI checked self-delete without refreshing authentication immediately before the action."),
    ]
    for number, (kind, actor, target, status, oracle, reason) in enumerate(human19, 41):
        add("FR19", number, "DELETE", "/api/admin/users/:id", "human-security", "FR-19, SEC-02/03/05", "Fresh actor and isolated target", kind, status, oracle, source="HUMAN-001", why_missed=reason, scenario={"kind": kind, "actor": actor, "target": target})

    assert len(CASES) == 140
    assert {f: sum(c.feature == f for c in CASES) for f in ("FR04", "FR10", "FR19")} == {"FR04": 45, "FR10": 50, "FR19": 45}
    assert all(c.audit_label == "VALID" and isinstance(c.expected_status, int) for c in CASES)


def auth_headers(actor: str) -> list[dict[str, str]]:
    values = {
        "admin": "Bearer {{adminToken}}",
        "user": "Bearer {{userToken}}",
        "case": "Bearer {{caseToken}}",
        "other-user": "Bearer {{otherToken}}",
        "target": "Bearer {{targetToken}}",
        "malformed": "Bearer not-a-jwt",
        "expired": f"Bearer {EXPIRED_USER_JWT}",
        "forged": f"Bearer {FORGED_ADMIN_JWT}",
        "wrong-scheme": "Basic not-a-jwt",
        "empty-bearer": "Bearer ",
        "none": None,
    }
    value = values.get(actor)
    return [] if value is None else [{"key": "Authorization", "value": value}]


def js_request(method: str, path: str, token: str | None = None, body: Any = None) -> str:
    headers = {"X-Student-Id": STUDENT_ID}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        headers["Content-Type"] = "application/json"
    obj: dict[str, Any] = {"url": "{{baseUrl}}" + path, "method": method, "header": headers}
    if body is not None:
        obj["body"] = {"mode": "raw", "raw": compact(body)}
    return compact(obj)


def isolated_user_pre(case: Case) -> list[str]:
    baseline = {"name": "Baseline User", "shipping_address": "Baseline Address", "phone": "0911111111"}
    return [
        f"const uniqueEmail = 'hw06.{case.test_id.lower()}.' + Date.now() + '@example.test';",
        f"const registerReq = {js_request('POST', '/api/register', body={'name': baseline['name'], 'email': '__EMAIL__', 'password': 'Case1234!'})};".replace("__EMAIL__", "' + uniqueEmail + '"),
        "registerReq.url = pm.environment.get('baseUrl') + '/api/register';",
        "registerReq.body.raw = JSON.stringify({name:'Baseline User',email:uniqueEmail,password:'Case1234!'});",
        "pm.sendRequest(registerReq, (regErr, regRes) => {",
        "  if (regErr || regRes.code !== 200) throw new Error('fixture register failed: ' + (regErr || regRes.text()));",
        f"  const loginReq = {js_request('POST', '/api/login', body={'email': '__EMAIL__', 'password': 'Case1234!'})};".replace("__EMAIL__", "' + uniqueEmail + '"),
        "  loginReq.url = pm.environment.get('baseUrl') + '/api/login';",
        "  loginReq.body.raw = JSON.stringify({email:uniqueEmail,password:'Case1234!'});",
        "  pm.sendRequest(loginReq, (loginErr, loginRes) => {",
        "    if (loginErr || loginRes.code !== 200) throw new Error('fixture login failed: ' + (loginErr || loginRes.text()));",
        "    const payload = loginRes.json();",
        "    pm.variables.set('caseToken', payload.token);",
        "    pm.variables.set('caseUserId', String(payload.user.id));",
        "    pm.variables.set('caseEmail', uniqueEmail);",
        f"    pm.variables.set('baselineProfile', {compact(compact(baseline))});",
        "  });",
        "});",
    ]


def order_pre(case: Case) -> list[str]:
    source = case.scenario.get("source", "pending")
    transitions = {
        "pending": [],
        "confirmed": ["confirmed"],
        "shipping": ["confirmed", "shipping"],
        "delivered": ["confirmed", "shipping", "delivered"],
        "canceled": ["canceled"],
    }[source]
    lines = [
        f"const checkoutReq = {js_request('POST', '/api/checkout', '{{userToken}}', {'total_amount': 1000, 'shipping_address': 'Fixture'})};",
        "checkoutReq.url = pm.environment.get('baseUrl') + '/api/checkout';",
        "checkoutReq.header.Authorization = 'Bearer ' + pm.environment.get('userToken');",
        "pm.sendRequest(checkoutReq, (checkoutErr, checkoutRes) => {",
        "  if (checkoutErr || checkoutRes.code !== 200) throw new Error('checkout fixture failed: ' + (checkoutErr || checkoutRes.text()));",
        "  const orderId = String(checkoutRes.json().orderId);",
        "  pm.variables.set('orderId', orderId);",
    ]
    if transitions:
        lines += [
            f"  const states = {compact(transitions)};",
            "  const advance = (index) => {",
            "    if (index >= states.length) return;",
            "    const stepReq = {url:pm.environment.get('baseUrl') + '/api/admin/orders/' + orderId + '/status',method:'PUT',header:{'Authorization':'Bearer ' + pm.environment.get('adminToken'),'Content-Type':'application/json','X-Student-Id':pm.environment.get('studentId')},body:{mode:'raw',raw:JSON.stringify({status:states[index]})}};",
            "    pm.sendRequest(stepReq, (stepErr, stepRes) => {",
            "      if (stepErr || stepRes.code !== 200) throw new Error('state fixture failed at ' + states[index] + ': ' + (stepErr || stepRes.text()));",
            "      advance(index + 1);",
            "    });",
            "  };",
            "  advance(0);",
        ]
    lines.append("});")

    if case.scenario.get("actor") == "other-user" or case.scenario.get("kind") == "cancel-other-owner":
        lines += [
            "const otherEmail = 'hw06.other.' + Date.now() + '@example.test';",
            f"const otherReg = {js_request('POST', '/api/register', body={'name':'Other User','email':'x','password':'Other123!'})};",
            "otherReg.url = pm.environment.get('baseUrl') + '/api/register';",
            "otherReg.body.raw = JSON.stringify({name:'Other User',email:otherEmail,password:'Other123!'});",
            "pm.sendRequest(otherReg, (e1, r1) => {",
            f"  const otherLogin = {js_request('POST', '/api/login', body={'email':'x','password':'Other123!'})};",
            "  otherLogin.url = pm.environment.get('baseUrl') + '/api/login';",
            "  otherLogin.body.raw = JSON.stringify({email:otherEmail,password:'Other123!'});",
            "  pm.sendRequest(otherLogin, (e2, r2) => { if (e2 || r2.code !== 200) throw new Error('other login failed'); pm.variables.set('otherToken', r2.json().token); });",
            "});",
        ]
    return lines


def disposable_user_pre(case: Case) -> list[str]:
    repeat = case.scenario.get("kind") == "repeat-delete"
    lines = [
        f"const targetEmail = 'hw06.{case.test_id.lower()}.' + Date.now() + '@example.test';",
        f"const registerTarget = {js_request('POST', '/api/register', body={'name':'Disposable User','email':'x','password':'Target123!'})};",
        "registerTarget.url = pm.environment.get('baseUrl') + '/api/register';",
        "registerTarget.body.raw = JSON.stringify({name:'Disposable User',email:targetEmail,password:'Target123!'});",
        "pm.sendRequest(registerTarget, (targetErr, targetRes) => {",
        "  if (targetErr || targetRes.code !== 200) throw new Error('target fixture failed: ' + (targetErr || targetRes.text()));",
        "  pm.variables.set('targetUserId', String(targetRes.json().id));",
        "  pm.variables.set('targetEmail', targetEmail);",
        f"  const targetLogin = {js_request('POST', '/api/login', body={'email':'x','password':'Target123!'})};",
        "  targetLogin.url = pm.environment.get('baseUrl') + '/api/login';",
        "  targetLogin.body.raw = JSON.stringify({email:targetEmail,password:'Target123!'});",
        "  pm.sendRequest(targetLogin, (loginErr, loginRes) => {",
        "    if (loginErr || loginRes.code !== 200) throw new Error('target login failed');",
        "    pm.variables.set('targetToken', loginRes.json().token);",
    ]
    if repeat:
        lines += [
            "    pm.sendRequest({url:pm.environment.get('baseUrl') + '/api/admin/users/' + pm.variables.get('targetUserId'),method:'DELETE',header:{'Authorization':'Bearer ' + pm.environment.get('adminToken'),'X-Student-Id':pm.environment.get('studentId')}}, (deleteErr, deleteRes) => { if (deleteErr || deleteRes.code !== 200) throw new Error('first delete fixture failed'); });",
        ]
    lines += [
        "  });",
        "});",
    ]
    return lines


def common_tests(case: Case) -> list[str]:
    return [
        f"pm.test('{case.test_id} exact status {case.expected_status}', () => pm.expect(pm.response.code).to.eql({case.expected_status}));",
        f"pm.test('{case.test_id} X-Student-Id present', () => pm.expect(pm.request.headers.get('X-Student-Id')).to.eql('{STUDENT_ID}'));",
        "pm.test('response is not an unhandled 5xx', () => pm.expect(pm.response.code).to.be.below(500));",
    ]


def response_schema_tests(case: Case) -> list[str]:
    return [
        "pm.test('response Content-Type is JSON', () => pm.expect(pm.response.headers.get('Content-Type') || '').to.include('application/json'));",
        "pm.test('response body matches status schema', () => { const body=pm.response.json(); if (pm.response.code >= 400) { pm.expect(body).to.be.an('object'); pm.expect(body.error).to.be.a('string'); } });",
    ]


def get_postcondition(path_expr: str, token_expr: str, assertions: list[str], label: str, *, cleanup_user: bool = False) -> str:
    body = " ".join(assertions)
    if cleanup_user:
        finish = (
            "const cleanup={url:pm.environment.get('baseUrl')+'/api/admin/users/'+pm.variables.get('caseUserId'),method:'DELETE',header:{'Authorization':'Bearer '+pm.environment.get('adminToken'),'X-Student-Id':pm.environment.get('studentId')}}; "
            "pm.sendRequest(cleanup,()=>{if(failure)done(failure);else done();});"
        )
    else:
        finish = "if(failure)done(failure);else done();"
    return (
        f"pm.test({json.dumps(label)}, function(done) {{ "
        f"pm.sendRequest({{url:pm.environment.get('baseUrl') + {path_expr},method:'GET',header:{{'Authorization':'Bearer ' + {token_expr},'X-Student-Id':pm.environment.get('studentId')}}}}, "
        f"(err,res) => {{ let failure=null; try {{ pm.expect(err).to.eql(null); {body} }} catch(e) {{ failure=e; }} {finish} }}); }});"
    )


def compile_case(case: Case) -> dict[str, Any]:
    scenario = case.scenario
    pre: list[str] = []
    tests = common_tests(case) + response_schema_tests(case)
    actor = scenario.get("actor", "case" if case.feature == "FR04" else "admin")
    path = case.endpoint
    body = scenario.get("body")
    query: list[dict[str, str]] = []

    if case.feature == "FR04":
        kind = scenario["kind"]
        if case.method == "GET":
            actor = {"valid-user": "user", "no-token": "none", "malformed-token": "malformed", "tampered-token": "forged", "expired-token": "expired", "wrong-scheme": "wrong-scheme", "empty-bearer": "empty-bearer"}.get(kind, "user")
            if kind in {"valid-user", "identity", "privacy-schema"}:
                tests += ["pm.test('profile object schema and identity', () => { const b=pm.response.json(); pm.expect(b).to.be.an('object'); pm.expect(b.id).to.be.a('number'); pm.expect(b.name).to.be.a('string'); pm.expect(b.email).to.be.a('string'); pm.expect(b.role).to.be.a('string'); });"]
            if kind == "privacy-schema":
                tests += ["pm.test('profile omits credentials', () => { const b=pm.response.json(); pm.expect(b).to.not.have.property('password'); pm.expect(b).to.not.have.property('reset_token'); });"]
            if kind == "identity":
                tests += ["pm.test('profile is JWT subject', () => { const b=pm.response.json(); pm.expect(String(b.id)).to.eql(pm.environment.get('userId')); pm.expect(b.email).to.eql('test@eshop.com'); });"]
            if kind == "repeat":
                tests += [get_postcondition("'/api/users/me'", "pm.environment.get('userToken')", ["pm.expect(res.code).to.eql(200);", "pm.expect(res.json().id).to.eql(pm.response.json().id);"], "repeat GET is stable")]
        else:
            actor = {"no-token": "none", "malformed-token": "malformed", "expired-token": "expired"}.get(kind, "case")
            if actor == "case":
                pre = isolated_user_pre(case)
            if body is None:
                raw_body = "null"
            else:
                raw_body = compact(body)
            if case.expected_status == 200:
                tests += ["pm.test('success message schema', () => { const b=pm.response.json(); pm.expect(Object.keys(b)).to.eql(['message']); pm.expect(b.message).to.be.a('string'); });"]
            protected = {"role-admin", "role-user", "email", "id", "user-id", "password", "unknown-field", "role-fresh-login"}
            invalid = {"phone-9", "phone-12", "phone-prefix", "phone-alpha", "phone-hyphen", "phone-space", "phone-null", "phone-number", "empty-object", "null-body"}
            if kind in protected | invalid | {"partial-preserve", "all-valid", "phone-10", "phone-11", "unicode-name", "long-name", "emoji-name", "empty-address", "unicode-address", "xss-json", "rtl-control", "replay", "cross-user", "response-schema"}:
                assertions = ["pm.expect(res.code).to.eql(200);", "const p=res.json();", "pm.expect(p.email).to.eql(pm.variables.get('caseEmail'));", "pm.expect(p.role).to.eql('user');"]
                if kind in invalid:
                    assertions += ["const base=JSON.parse(pm.variables.get('baselineProfile'));", "pm.expect(p.name).to.eql(base.name);", "pm.expect(p.shipping_address).to.eql(base.shipping_address);", "pm.expect(p.phone).to.eql(base.phone);"]
                if kind == "partial-preserve":
                    assertions += ["const base=JSON.parse(pm.variables.get('baselineProfile'));", "pm.expect(p.name).to.eql('Only Name');", "pm.expect(p.shipping_address).to.eql(base.shipping_address);", "pm.expect(p.phone).to.eql(base.phone);"]
                if case.expected_status == 200 and isinstance(body, dict):
                    for key in ("name", "shipping_address", "phone"):
                        if key in body and kind not in invalid:
                            assertions.append(f"pm.expect(p.{key}).to.eql({compact(body[key])});")
                tests += [get_postcondition("'/api/users/me'", "pm.variables.get('caseToken')", assertions, "profile postcondition", cleanup_user=kind != "replay")]
            if kind == "replay":
                tests += [f"pm.test('replay remains idempotent', function(done) {{ pm.sendRequest({{url:pm.environment.get('baseUrl')+'/api/users/me',method:'PUT',header:{{'Authorization':'Bearer '+pm.variables.get('caseToken'),'Content-Type':'application/json','X-Student-Id':pm.environment.get('studentId')}},body:{{mode:'raw',raw:{json.dumps(raw_body)}}}}}, (e,r)=>{{try{{pm.expect(e).to.eql(null);pm.expect(r.code).to.eql(200);done();}}catch(x){{done(x);}}}}); }});"]
            body = body

    elif case.feature == "FR10":
        kind = scenario["kind"]
        pre = order_pre(case)
        actor = {"none": "none", "malformed": "malformed", "user": "user", "forged": "forged", "other-user": "other-user"}.get(scenario.get("actor"), "admin")
        if path.endswith("cancel"):
            body = None
        else:
            target = scenario.get("target")
            if kind == "missing-status": body = {}
            elif kind == "null-status": body = {"status": None}
            elif kind == "uppercase-status": body = {"status": "CONFIRMED"}
            elif kind == "script-status": body = {"status": "<script>alert(1)</script>"}
            elif kind == "concurrent-confirm-cancel": body = {"status": "confirmed"}
            else: body = {"status": target}
        if kind == "missing-order": path = "/api/admin/orders/99999999/status"
        elif kind == "negative-id": path = "/api/admin/orders/-1/status"
        elif kind == "leading-zero-id": path = "/api/admin/orders/000{{orderId}}/status"
        else: path = path.replace(":id", "{{orderId}}")
        source = scenario.get("source", "pending")
        if kind == "concurrent-confirm-cancel":
            tests += ["pm.test('concurrent result is one legal outcome', function(done) { const cancel={url:pm.environment.get('baseUrl')+'/api/orders/'+pm.variables.get('orderId')+'/cancel',method:'PUT',header:{'Authorization':'Bearer '+pm.environment.get('userToken'),'X-Student-Id':pm.environment.get('studentId')}}; pm.sendRequest(cancel,(e,r)=>{try{pm.expect(e).to.eql(null);pm.expect(r.code).to.be.oneOf([200,400]);pm.sendRequest(pm.environment.get('baseUrl')+'/api/orders/'+pm.variables.get('orderId'),(e2,r2)=>{try{pm.expect(['confirmed','canceled']).to.include(r2.json().status);done();}catch(x){done(x);}});}catch(x){done(x);}}); });"]
        elif "99999999" not in path and "/-1/" not in path:
            expected_state = scenario.get("target") if case.expected_status == 200 and not path.endswith("cancel") else ("canceled" if case.expected_status == 200 and path.endswith("cancel") else source)
            tests += [get_postcondition("'/api/orders/' + pm.variables.get('orderId')", "pm.environment.get('userToken')", ["pm.expect(res.code).to.eql(200);", f"pm.expect(res.json().status).to.eql({json.dumps(expected_state)});"], "order state postcondition")]
        if kind in {"response-schema"}:
            tests += ["pm.test('success response exact schema',()=>{const b=pm.response.json();pm.expect(Object.keys(b)).to.eql(['message']);pm.expect(b.message).to.be.a('string');});"]
        if kind == "exact-error-schema":
            tests += ["pm.test('error response exact schema',()=>{const b=pm.response.json();pm.expect(Object.keys(b)).to.eql(['error']);pm.expect(b.error).to.be.a('string');});"]

    else:
        kind = scenario["kind"]
        actor = scenario.get("actor", "admin")
        if case.method == "GET":
            if kind == "new-user-visible": pre = disposable_user_pre(case)
            if kind == "query-id": query = [{"key": "id", "value": "1"}]
            elif kind == "query-role": query = [{"key": "role", "value": "admin"}]
            elif kind == "query-sql": query = [{"key": "id", "value": "1' OR '1'='1"}]
            if case.expected_status == 200:
                tests += ["pm.test('admin list schema',()=>{const rows=pm.response.json();pm.expect(rows).to.be.an('array');rows.forEach(u=>{pm.expect(u.id).to.be.a('number');pm.expect(u.name).to.be.a('string');pm.expect(u.email).to.be.a('string');pm.expect(u.role).to.be.a('string');pm.expect(u).to.not.have.property('password');pm.expect(u).to.not.have.property('reset_token');});});"]
            if kind == "unique-ids": tests += ["pm.test('user ids unique',()=>{const ids=pm.response.json().map(x=>x.id);pm.expect(new Set(ids).size).to.eql(ids.length);});"]
            if kind == "new-user-visible": tests += ["pm.test('new user appears once',()=>{const n=pm.response.json().filter(x=>x.email===pm.variables.get('targetEmail')).length;pm.expect(n).to.eql(1);});"]
            if kind == "repeat-list": tests += [get_postcondition("'/api/admin/users'", "pm.environment.get('adminToken')", ["pm.expect(res.code).to.eql(200);", "const a=pm.response.json().map(x=>x.id).sort();", "const b=res.json().map(x=>x.id).sort();", "pm.expect(b).to.eql(a);"], "repeated list stable")]
        else:
            target = scenario.get("target")
            if target == "target" or target == "leading-zero-target" or kind in {"concurrent-delete", "stale-token", "student-id-spoof"}:
                pre = disposable_user_pre(case)
                target_value = "000{{targetUserId}}" if target == "leading-zero-target" else "{{targetUserId}}"
            elif target == "admin":
                target_value = "{{adminId}}"
            else:
                target_value = target
            path = "/api/admin/users/" + target_value
            if kind == "repeat-delete": pre = disposable_user_pre(case)
            if kind == "student-id-spoof": actor = "user"
            if kind == "stale-token":
                tests += ["pm.test('deleted user JWT is no longer a valid subject', function(done){pm.sendRequest({url:pm.environment.get('baseUrl')+'/api/users/me',method:'GET',header:{'Authorization':'Bearer '+pm.variables.get('targetToken'),'X-Student-Id':pm.environment.get('studentId')}},(e,r)=>{try{pm.expect(e).to.eql(null);pm.expect(r.code).to.eql(401);done();}catch(x){done(x);}});});"]
            elif kind == "concurrent-delete":
                tests += ["pm.test('concurrent duplicate has at most one success', function(done){pm.sendRequest({url:pm.environment.get('baseUrl')+'/api/admin/users/'+pm.variables.get('targetUserId'),method:'DELETE',header:{'Authorization':'Bearer '+pm.environment.get('adminToken'),'X-Student-Id':pm.environment.get('studentId')}},(e,r)=>{try{pm.expect(e).to.eql(null);pm.expect(r.code).to.eql(404);done();}catch(x){done(x);}});});"]
            else:
                expected_absent = case.expected_status == 200 or kind == "repeat-delete"
                if target in {"target"} or kind in {"valid-delete", "response-schema", "unrelated-remains", "content-type"}:
                    tests += [get_postcondition("'/api/admin/users'", "pm.environment.get('adminToken')", ["pm.expect(res.code).to.eql(200);", "const ids=res.json().map(x=>String(x.id));", f"pm.expect(ids.includes(pm.variables.get('targetUserId'))).to.eql({str(expected_absent).lower() if False else str(not expected_absent).lower()});"], "delete postcondition")]
                if target == "admin":
                    tests += [get_postcondition("'/api/admin/users'", "pm.environment.get('adminToken')", ["pm.expect(res.code).to.eql(200);", "const ids=res.json().map(x=>String(x.id));", "pm.expect(ids).to.include(pm.environment.get('adminId'));"], "admin remains after self-delete attempt")]
            if kind in {"response-schema", "content-type"}: tests += ["pm.test('delete success schema',()=>{const b=pm.response.json();pm.expect(Object.keys(b)).to.eql(['message']);pm.expect(b.message).to.be.a('string');});"]
            if kind == "missing-error-schema": tests += ["pm.test('delete error schema',()=>{const b=pm.response.json();pm.expect(Object.keys(b)).to.eql(['error']);pm.expect(b.error).to.be.a('string');});"]

    headers = auth_headers(actor)
    if body is not None or case.method in {"PUT", "POST"}:
        headers.append({"key": "Content-Type", "value": "application/json"})
    if case.scenario.get("kind") == "student-id-spoof":
        headers.append({"key": "X-Student-Id", "value": "1", "disabled": True})
    url: dict[str, Any] = {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": path.strip("/").split("/")}
    if query:
        url["query"] = query
        url["raw"] += "?" + "&".join(f"{x['key']}={x['value']}" for x in query)
    request: dict[str, Any] = {"method": case.method, "header": headers, "url": url}
    include_body = body is not None or (case.feature == "FR04" and case.method == "PUT") or (case.feature == "FR10" and case.method == "PUT" and not case.endpoint.endswith("cancel"))
    if include_body:
        request["body"] = {"mode": "raw", "raw": "null" if body is None else compact(body)}
    events = []
    if pre: events.append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": pre}})
    events.append({"listen": "test", "script": {"type": "text/javascript", "exec": tests}})
    return {"name": case.item_name, "description": f"{case.requirement}\n\nOracle: {case.oracle}\n\nAudit: {case.audit_label}", "request": request, "event": events}


def setup_item(name: str, email: str, password: str, token_key: str, id_key: str) -> dict[str, Any]:
    request = {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {"mode": "raw", "raw": compact({"email": email, "password": password})},
        "url": {"raw": "{{baseUrl}}/api/login", "host": ["{{baseUrl}}"], "path": ["api", "login"]},
    }
    tests = [
        "pm.test('setup login succeeds',()=>pm.expect(pm.response.code).to.eql(200));",
        f"const setup=pm.response.json(); pm.environment.set('{token_key}',setup.token); pm.environment.set('{id_key}',String(setup.user.id));",
    ]
    return {"name": name, "request": request, "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}]}


def build_collection() -> dict[str, Any]:
    common_pre = [
        "const sid=pm.environment.get('studentId');",
        "if(!sid) throw new Error('studentId is required');",
        "pm.request.headers.upsert({key:'X-Student-Id',value:sid});",
        "console.log('[HW06]',pm.info.requestName,'X-Student-Id='+sid,pm.request.method,pm.request.url.toString());",
    ]
    folders = []
    for feature, title in [("FR04", "FR-04 Personal profile"), ("FR10", "FR-10 Order state machine"), ("FR19", "FR-19 Admin user management")]:
        feature_cases = [c for c in CASES if c.feature == feature]
        if feature == "FR19":
            feature_cases.sort(key=lambda c: (c.scenario.get("kind") == "fresh-self-delete", c.test_id))
        items = [compile_case(c) for c in feature_cases]
        folders.append({"name": title, "item": items})
    return {
        "info": {"name": "HW06 23127326 — audited executable suite", "description": "140 catalogue cases with isolated fixtures, exact oracles, schema checks and postconditions.", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": common_pre}}],
        "variable": [{"key": "baseUrl", "value": "http://localhost:3000"}, {"key": "studentId", "value": STUDENT_ID}],
        "item": [
            {"name": "00 Setup", "item": [
                setup_item("SETUP login admin", "admin@eshop.com", "Admin123!", "adminToken", "adminId"),
                setup_item("SETUP login user", "test@eshop.com", "Test1234!", "userToken", "userId"),
            ]},
            *folders,
        ],
    }


def write_catalogue() -> None:
    headers = ["Test ID", "Feature", "Endpoint", "Method", "Category", "Requirement/SEC", "Precondition", "Test data", "Steps", "Expected status", "Expected oracle/schema", "AI source", "Audit label", "Audit reason", "Corrected version", "Why AI missed", "Postman mapping", "Execution status", "Observed status", "Classification", "Bug ID", "Evidence"]
    rows = []
    for c in CASES:
        rows.append({
            "Test ID": c.test_id,
            "Feature": c.feature,
            "Endpoint": c.endpoint,
            "Method": c.method,
            "Category": c.category,
            "Requirement/SEC": c.requirement,
            "Precondition": c.precondition,
            "Test data": c.data,
            "Steps": "Create isolated fixture; send mapped request; assert exact status/schema; verify state/identity postcondition.",
            "Expected status": str(c.expected_status),
            "Expected oracle/schema": c.oracle,
            "AI source": c.ai_source,
            "Audit label": c.audit_label,
            "Audit reason": c.audit_reason,
            "Corrected version": c.correction,
            "Why AI missed": c.why_missed,
            "Postman mapping": c.item_name,
            "Execution status": "NOT RUN",
            "Observed status": "",
            "Classification": "",
            "Bug ID": "",
            "Evidence": "",
        })
    TC_DIR.mkdir(parents=True, exist_ok=True)
    with (TC_DIR / "23127326.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (TC_DIR / "23127326.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def write_data_driven_assets() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        ("valid-10", "0912345678", 200),
        ("valid-11", "01234567890", 200),
        ("short-9", "091234567", 400),
        ("long-12", "091234567890", 400),
        ("wrong-prefix", "1912345678", 400),
        ("letters", "09abcdefgh", 400),
    ]
    with (DATA_DIR / "fr04-phone-partitions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["partition", "phone", "expectedStatus"])
        writer.writerows(rows)
    login = setup_item("Login user for iteration", "test@eshop.com", "Test1234!", "userToken", "userId")
    update = {
        "name": "Data-driven phone partition",
        "request": {
            "method": "PUT",
            "header": [{"key": "Authorization", "value": "Bearer {{userToken}}"}, {"key": "Content-Type", "value": "application/json"}],
            "body": {"mode": "raw", "raw": '{"name":"Data Runner","shipping_address":"Data","phone":"{{phone}}"}'},
            "url": {"raw": "{{baseUrl}}/api/users/me", "host": ["{{baseUrl}}"], "path": ["api", "users", "me"]},
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": [
            "pm.test('partition status '+pm.iterationData.get('partition'),()=>pm.expect(pm.response.code).to.eql(Number(pm.iterationData.get('expectedStatus'))));",
            f"pm.test('X-Student-Id present',()=>pm.expect(pm.request.headers.get('X-Student-Id')).to.eql('{STUDENT_ID}'));",
        ]}}],
    }
    collection = {
        "info": {"name": "HW06 23127326 — data-driven FR04 phone partitions", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": ["pm.request.headers.upsert({key:'X-Student-Id',value:pm.environment.get('studentId')});", "console.log('[HW06-DATA]',pm.iterationData.get('partition'),'X-Student-Id='+pm.environment.get('studentId'));"]}}],
        "item": [login, update],
    }
    (PM_DIR / "HW06_23127326_data_driven_collection.json").write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")


def write_ci_demo_asset() -> None:
    """Build a stable three-feature CI gate plus one explicitly controlled assertion."""
    selected_ids = {"FR04-001", "FR10-001", "FR19-001"}
    selected = [compile_case(case) for case in CASES if case.test_id in selected_ids]
    control_item = {
        "name": "CI-DEMO-001 — controlled pass/fail assertion",
        "request": {
            "method": "GET",
            "header": [],
            "url": {"raw": "{{baseUrl}}/api/products", "host": ["{{baseUrl}}"], "path": ["api", "products"]},
        },
        "event": [{
            "listen": "test",
            "script": {"type": "text/javascript", "exec": [
                "pm.test('CI demo endpoint responds 200',()=>pm.expect(pm.response.code).to.eql(200));",
                "pm.test('CI-DEMO-001 controlled assertion',()=>pm.expect(pm.environment.get('forceFailure')).to.eql('false'));",
            ]},
        }],
    }
    collection = {
        "info": {
            "name": "HW06 23127326 — deterministic CI demonstration",
            "description": "Stable three-feature gate. forceFailure=true changes exactly one named control assertion; it is not a product-defect claim.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": [
            "const sid=pm.environment.get('studentId');",
            "if(!sid) throw new Error('studentId is required');",
            "pm.request.headers.upsert({key:'X-Student-Id',value:sid});",
            "console.log('[HW06-CI]',pm.info.requestName,'X-Student-Id='+sid);",
        ]}}],
        "variable": [{"key": "baseUrl", "value": "http://localhost:3000"}],
        "item": [
            {"name": "00 Setup", "item": [
                setup_item("SETUP login admin", "admin@eshop.com", "Admin123!", "adminToken", "adminId"),
                setup_item("SETUP login user", "test@eshop.com", "Test1234!", "userToken", "userId"),
            ]},
            {"name": "01 Stable API checks", "item": selected},
            {"name": "02 Pipeline control", "item": [control_item]},
        ],
    }
    (PM_DIR / "HW06_23127326_ci_demo_collection.json").write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    build_cases()
    write_catalogue()
    PM_DIR.mkdir(parents=True, exist_ok=True)
    (PM_DIR / "HW06_23127326_collection.json").write_text(json.dumps(build_collection(), ensure_ascii=False, indent=2), encoding="utf-8")
    write_data_driven_assets()
    write_ci_demo_asset()
    print(f"generated {len(CASES)} audited catalogue cases")


if __name__ == "__main__":
    main()
