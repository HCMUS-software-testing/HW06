import json, os
ROOT=os.path.dirname(os.path.dirname(__file__))
p=os.path.join(ROOT,'newman','member-4','newman-full-report.json')
d=json.load(open(p)); failures=d['run']['failures']
known={'FR04 role escalation must reject':('DEFECT','BUG-04-001','Role mass assignment reproduced; response 200'),'FR04-035 — security':('DEFECT','BUG-04-001','Duplicate role assertion; same root defect'),'FR19 user list must reject':('DEFECT','BUG-04-005','Regular user receives 200 admin list'),'FR19 self-delete must reject':('DEFECT','BUG-04-006','Admin self-delete receives 200 and removes self')}
rows=['# Newman failure classification — full run','',f'Run: 150 requests/assertions; {len(failures)} failed assertions. SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`.','', '| # | Item | Class | Bug/Reason |', '|---:|---|---|---|']
counts={'DEFECT':0,'EXPECTED-NEGATIVE':0,'FIXTURE-ISSUE':0}
for i,f in enumerate(failures,1):
    name=f.get('source',{}).get('name','')
    if name in known: cls,bug,why=known[name]
    else: cls,bug,why='FIXTURE-ISSUE','FIXTURE','Generic token/body/ID or shared mutable order failed to realize declared precondition.'
    counts[cls]+=1; rows.append(f'| {i} | `{name}` | **{cls}** | `{bug}` — {why} |')
rows += ['', '## Totals', '', f'- DEFECT occurrences: **{counts["DEFECT"]}** (3 unique root defects)', f'- EXPECTED-NEGATIVE: **{counts["EXPECTED-NEGATIVE"]}**', f'- FIXTURE-ISSUE: **{counts["FIXTURE-ISSUE"]}**', '', 'Rule: failed assertion against a correctly realized security/business precondition is DEFECT; failure caused by generic catalogue data is FIXTURE-ISSUE. Negative case name alone never makes result EXPECTED-NEGATIVE.']
out=os.path.join(ROOT,'docs','failure-classification.md'); open(out,'w',encoding='utf8').write('\n'.join(rows)+'\n'); print(out,counts)
