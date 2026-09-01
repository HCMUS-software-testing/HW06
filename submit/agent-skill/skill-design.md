# Agent Skill design notes

Student must draw the original diagram manually. The submitted `diagram.png` should show: inputs (API spec, SRS, selected feature), parser/normalizer, four parallel coverage planners (domain/state/security/schema), candidate generator, deduplicator/critic, human-review gate, exporters (Excel/Markdown/Postman), execution engine, defect evidence, and a feedback loop from audit/execution back to prompts/rules.

Diagram acceptance: arrows show data flow; human review is a hard gate; execution and bug evidence are downstream of approval; no AI image/diagram generation is used.

## Required edges for the student-drawn version

1. `API spec + SRS + feature -> Contract normalizer`.
2. `Contract normalizer -> Domain planner / State planner / Security planner / Schema planner`.
3. All four planners `-> Candidate generator -> Deduplicator + critic`.
4. `Deduplicator + critic -> Human review gate`.
5. Rejected/incomplete branch `-> Prompt/rule refinement -> planners`.
6. Approved branch `-> CSV/XLSX + Postman exporters -> Newman execution -> failure classifier -> bug evidence`.
7. Execution feedback `-> Human review gate`.

Student attestation to complete under the final image: `I designed and drew this diagram myself: __________ (name/date).`
