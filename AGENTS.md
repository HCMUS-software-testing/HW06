# Repository Guidelines

## Project Structure & Module Organization

This repository is an HW06 API-testing submission for the EShop SUT, not a standalone application. Keep deliverables organized as follows:

- `src/test-cases/`: AI-generated, audited, and human-extended cases for FR-05, FR-08, and FR-18.
- `src/postman/`: Postman collection and local environment; generated run data belongs in its `data/` directory.
- `src/docs/`: Main report, CI/CD report, AI critique, prompt sequence, and commit-log evidence.
- `src/bug-reports/`: Reproducible defect reports and issue references.
- `src/ai-audit/`: AI audit log and review evidence.
- `src/agent-skill/`: Mermaid diagram, pseudocode, and demo notes for the AI test generator.
- `req/`, `docs/`, and `ai-reasoning/`: assignment requirements, planning/team documents, and supporting research.

## Build, Test, and Development Commands

There is no application build configured in this repository. Run the EShop backend at `http://localhost:3000`, then execute the committed Postman collection with Newman when available:

```bash
newman run src/postman/HW06_API_Testing.postman_collection.json \
  -e src/postman/HW06_Local.postman_environment.json
```

Use the collection’s environment variables and preserve the required `X-Student-Id` header. Record meaningful execution results in the relevant report under `src/docs/` or `src/newman/`.

## Coding Style & Naming Conventions

Use Markdown headings, short paragraphs, and tables that match the surrounding report style. Name files in lowercase kebab-case where practical; retain the existing `member-2-fr-XX.md` and `HW06_*.json` patterns. Keep Postman request names aligned with the endpoint and functional requirement. Use two-space indentation in JSON and valid Mermaid syntax in diagrams.

## Testing Guidelines

Organize cases by functional requirement and distinguish AI-generated, audited, and human-written cases. Each case should state preconditions, request data, expected status/body behavior, and audit rationale. Cover positive, negative, boundary, authorization, and security scenarios. Validate JSON after editing collection or environment files, and rerun Newman after request or script changes.

## Commit & Pull Request Guidelines

Follow the history’s Conventional Commit style with the member scope, for example `test(member-2): complete FR-08 cases` or `docs(member-2): update main report`. Keep commits focused. Pull requests should summarize changed deliverables, identify the FRs affected, include test execution evidence or explain why it is unavailable, and link any bug reports or issues.

## Security & Configuration Tips

Do not commit real tokens, credentials, or private service URLs. Use the local Postman environment and replace placeholder secrets locally. Review exported JSON for accidentally embedded authorization values before sharing changes.
