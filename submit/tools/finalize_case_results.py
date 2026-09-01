"""Merge the recorded Newman run into the catalogue workbook/CSV."""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(ROOT, "test-cases", "member-4.csv")
json_path = os.path.join(ROOT, "newman", "member-4", "newman-full-report.json")

evidence = {
    "FR04-035": ("BUG-04-001", "../evidence/BUG-04-001.png"),
    "FR19-004": ("BUG-04-005", "../evidence/BUG-04-005.png"),
    "FR19-027": ("BUG-04-006", "../evidence/BUG-04-006.png"),
}

with open(json_path, encoding="utf-8") as f:
    report = json.load(f)
observed = {}
for execution in report["run"]["executions"]:
    name = execution["item"]["name"]
    if not name.startswith(("FR04-", "FR10-", "FR19-")):
        continue
    tid = name.split(" — ", 1)[0]
    code = execution.get("response", {}).get("code", "n/a")
    failed = any(a.get("error") for a in execution.get("assertions", []))
    observed[tid] = (code, "FAIL" if failed else "PASS", name)

with open(csv_path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
for row in rows:
    tid = row["Test ID"]
    code, outcome, item = observed.get(tid, ("n/a", "NOT RUN", "not found in Newman report"))
    row["Postman mapping"] = item
    row["Actual result"] = f"HTTP {code}; {outcome}"
    if tid in evidence:
        row["Bug ID"], row["Evidence"] = evidence[tid]
    elif outcome == "FAIL":
        row["Evidence"] = "../newman/member-4/newman-full-report.html"
    else:
        row["Evidence"] = "../newman/member-4/newman-full-report.html"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader(); writer.writerows(rows)
json_out = os.path.join(ROOT, "test-cases", "member-4.json")
with open(json_out, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print(f"updated {len(rows)} rows; mapped {len(observed)} Newman items")
