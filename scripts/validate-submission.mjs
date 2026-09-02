import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const CASE_SPECS = [
  { fr: '05', path: 'src/test-cases/member-2-fr-05.md' },
  { fr: '08', path: 'src/test-cases/member-2-fr-08.md' },
  { fr: '18', path: 'src/test-cases/member-2-fr-18.md' },
];

const CASE_ID_PATTERN = /TC-FR(?:05|08|18)-(?:AI|HUMAN)-\d{3}/g;
const AUDIT_ROW_PATTERN = /^\|(?:\s*\d+\s*\|)?\s*(TC-FR(?:05|08|18)-AI-\d{3})\s*\|\s*(VALID|INVALID|INCOMPLETE)\s*\|/gmi;
const EXECUTION_CLASSES = new Set(['NEWMAN', 'BROWSER-MANUAL', 'FAULT-INJECTION', 'EXCLUDED']);
const FR_SCOPES = {
  '05': [{ method: 'GET', route: '/api/products' }],
  '08': [{ method: 'POST', route: '/api/checkout' }],
  '18': [
    { method: 'GET', route: '/api/admin/orders' },
    { method: 'PUT', route: '/api/admin/orders/:id/status' },
  ],
};

export function extractCaseIds(markdown) {
  return [...String(markdown).matchAll(CASE_ID_PATTERN)].map(([id]) => id);
}

export function countAuditLabels(markdown) {
  const counts = { VALID: 0, INVALID: 0, INCOMPLETE: 0 };

  for (const [, , label] of String(markdown).matchAll(AUDIT_ROW_PATTERN)) {
    counts[label] += 1;
  }

  return counts;
}

export function collectAssertionIds(collection) {
  const ids = new Set();

  const visit = (item) => {
    if (!item || typeof item !== 'object') return;

    for (const event of item.event ?? []) {
      if (event.listen !== 'test') continue;
      for (const line of event.script?.exec ?? []) {
        for (const id of extractCaseIds(line)) ids.add(id);
      }
    }

    for (const child of item.item ?? []) visit(child);
  };

  visit(collection);
  return ids;
}

export function loadNewmanTotals(paths) {
  const totals = {
    reports: 0,
    assertions: { total: 0, executed: 0, passed: 0, failed: 0 },
    requests: { total: 0, executed: 0, passed: 0, failed: 0 },
    executed: 0,
    passed: 0,
    failed: 0,
  };

  for (const path of paths) {
    const report = JSON.parse(readFileSync(path, 'utf8'));
    const stats = report.run?.stats ?? {};
    totals.reports += 1;
    const assertions = Number(stats.assertions?.total ?? 0);
    const failedAssertions = Number(stats.assertions?.failed ?? 0);
    const requests = Number(stats.requests?.total ?? 0);
    const failedRequests = Number(stats.requests?.failed ?? 0);
    totals.assertions.total += assertions;
    totals.assertions.executed += assertions;
    totals.assertions.passed += assertions - failedAssertions;
    totals.assertions.failed += failedAssertions;
    totals.requests.total += requests;
    totals.requests.executed += requests;
    totals.requests.passed += requests - failedRequests;
    totals.requests.failed += failedRequests;
  }

  totals.executed = totals.assertions.executed;
  totals.passed = totals.assertions.passed;
  totals.failed = totals.assertions.failed;

  return totals;
}

export function findForbiddenEvidence(text) {
  const source = String(text);
  const violations = [];

  for (const endpoint of ['/api/products/search', '/api/orders/checkout']) {
    if (source.includes(endpoint)) {
      violations.push({ code: 'STALE_ENDPOINT', detail: endpoint });
    }
  }
  if (/\b0{40}\b/.test(source)) violations.push({ code: 'ZERO_SHA', detail: 'all-zero SHA' });
  if (/\bBearer\s+eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/i.test(source)
    || /["'](?:token|accessToken|adminToken|userToken)["']\s*:\s*["']eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+["']/i.test(source)) {
    violations.push({ code: 'JWT', detail: 'committed JWT-shaped credential' });
  }
  if (/(?:completed|passed|successful|hoàn thành)[^\n]*(?:MANUAL-EVIDENCE-REQUIRED|\[Manual by user\])/i.test(source)) {
    violations.push({ code: 'COMPLETED_WITH_MANUAL_EVIDENCE', detail: 'completed claim paired with manual evidence marker' });
  }

  return violations;
}

function extractAuditVerdicts(markdown) {
  const verdicts = new Map();
  for (const [, id, label] of String(markdown).matchAll(AUDIT_ROW_PATTERN)) {
    const labels = verdicts.get(id) ?? [];
    labels.push(label);
    verdicts.set(id, labels);
  }
  return verdicts;
}

function listFiles(path) {
  if (!existsSync(path)) return [];
  const stat = statSync(path);
  if (stat.isFile()) return [path];
  return readdirSync(path, { withFileTypes: true }).flatMap((entry) => listFiles(resolve(path, entry.name)));
}

function safeRead(path, errors) {
  try {
    return readFileSync(path, 'utf8');
  } catch (error) {
    errors.push(`cannot read ${path}: ${error.message}`);
    return null;
  }
}

function parseJson(path, label, errors) {
  const text = safeRead(path, errors);
  if (text === null) return null;
  try {
    return JSON.parse(text);
  } catch (error) {
    errors.push(`${label} is not valid JSON: ${error.message}`);
    return null;
  }
}

function normalizeRoute(value) {
  const text = typeof value === 'string' ? value : value?.raw;
  if (!text) return null;
  const match = String(text).match(/\/api\/[^\s?#]*/);
  if (!match) return null;
  return match[0]
    .replace(/\{\{[^}]+\}\}/g, ':id')
    .replace(/\/\{[^}]+\}/g, '/:id')
    .replace(/\/+/g, '/');
}

function routeIsAllowed(fr, method, route) {
  return FR_SCOPES[fr]?.some((allowed) => allowed.method === method && allowed.route === route) ?? false;
}

function collectCollectionRequests(collection) {
  const requests = [];

  const visit = (item, inheritedFr = null) => {
    if (!item || typeof item !== 'object') return;
    const fr = String(item.name ?? '').match(/FR[-\s]?(05|08|18)/i)?.[1] ?? inheritedFr;
    if (item.request) {
      requests.push({
        fr,
        method: String(item.request.method ?? '').toUpperCase(),
        route: normalizeRoute(item.request.url),
      });
    }
    for (const child of item.item ?? []) visit(child, fr);
  };

  visit(collection);
  return requests;
}

function parseTraceabilityRows(markdown) {
  const rows = [];

  for (const line of String(markdown).split('\n')) {
    if (!line.trim().startsWith('|') || /^\|\s*:?-{3,}/.test(line)) continue;
    const cells = line.split('|').slice(1, -1).map((cell) => cell.trim());
    const caseId = cells[0]?.match(/^TC-FR(?:05|08|18)-(?:AI|HUMAN)-\d{3}$/)?.[0];
    if (!caseId) continue;
    const executionClass = cells[2]?.toUpperCase();
    const assertionId = cells[4]?.match(CASE_ID_PATTERN)?.[0] ?? null;
    rows.push({
      caseId,
      fr: caseId.slice(5, 7),
      executionClass,
      assertionId,
      method: cells[3]?.match(/\b(GET|POST|PUT)\b/i)?.[1]?.toUpperCase() ?? null,
      route: normalizeRoute(cells[3]),
      resultTarget: cells[5] ?? '',
    });
  }

  return rows;
}

function documentedNewmanTotals(markdown) {
  const lines = String(markdown).split('\n');
  const keyValue = /\b(requests?|executed|passed|failed|failures?)\b\s*[:=]\s*(\d+)/gi;

  for (const line of lines) {
    if (!/newman/i.test(line)) continue;
    const values = {};
    for (const [, key, value] of line.matchAll(keyValue)) {
      const normalized = key.toLowerCase().startsWith('request') ? 'requests'
        : key.toLowerCase().startsWith('fail') ? 'failed'
          : key.toLowerCase();
      values[normalized] = Number(value);
    }
    if (['requests', 'executed', 'passed', 'failed'].every((key) => Number.isInteger(values[key]))) return values;
  }

  for (let index = 0; index < lines.length - 2; index += 1) {
    const header = lines[index].toLowerCase();
    if (!/newman/.test(lines[index - 1] ?? '') || !['requests', 'executed', 'passed', 'failed'].every((key) => header.includes(key))) continue;
    const labels = lines[index].split('|').slice(1, -1).map((cell) => cell.trim().toLowerCase());
    const values = lines[index + 2].split('|').slice(1, -1).map((cell) => Number(cell.trim()));
    const totals = Object.fromEntries(labels.map((label, position) => [label, values[position]]));
    if (['requests', 'executed', 'passed', 'failed'].every((key) => Number.isInteger(totals[key]))) return totals;
  }

  return null;
}

function addFinding(findings, level, message) {
  findings[`${level.toLowerCase()}s`].push(message);
}

export function validateSubmission(options = {}) {
  const rootDir = resolve(options.rootDir ?? process.cwd());
  const findings = { errors: [], warnings: [], oks: [] };
  const caseFiles = options.caseFiles ?? CASE_SPECS;
  const collectionPath = options.collectionPath === undefined
    ? 'src/postman/HW06_API_Testing.postman_collection.json'
    : options.collectionPath;
  const environmentPath = options.environmentPath === undefined
    ? 'src/postman/HW06_Local.postman_environment.json'
    : options.environmentPath;
  const auditPath = options.auditPath === undefined ? 'src/ai-audit/ai_audit_report.md' : options.auditPath;
  const traceabilityPath = options.traceabilityPath === undefined ? 'src/test-cases/member-2-traceability.md' : options.traceabilityPath;
  const reportPaths = options.reportPaths ?? [
    'src/README.md',
    'src/docs/main-report.md',
    'src/docs/cicd-report.md',
  ];
  const newmanPaths = options.newmanPaths ?? listFiles(resolve(rootDir, 'src/newman'))
    .filter((path) => path.endsWith('.json'));

  const allCaseIds = [];
  const caseIdsByFr = new Map();
  const auditVerdicts = new Map();

  for (const spec of caseFiles) {
    const path = resolve(rootDir, spec.path);
    const markdown = safeRead(path, findings.errors);
    if (markdown === null) continue;
    const ids = extractCaseIds(markdown);
    allCaseIds.push(...ids);
    caseIdsByFr.set(spec.fr, ids);

    for (const [id, labels] of extractAuditVerdicts(markdown)) {
      auditVerdicts.set(id, [...(auditVerdicts.get(id) ?? []), ...labels]);
    }
  }

  const occurrences = new Map();
  for (const id of allCaseIds) occurrences.set(id, (occurrences.get(id) ?? 0) + 1);
  for (const [id, count] of occurrences) {
    if (count > 1) addFinding(findings, 'ERROR', `duplicate case ID ${id} appears ${count} times`);
  }

  for (const { fr } of caseFiles) {
    const ids = caseIdsByFr.get(fr) ?? [];
    const aiIds = [...new Set(ids.filter((id) => id.startsWith(`TC-FR${fr}-AI-`)))];
    const humanIds = [...new Set(ids.filter((id) => id.startsWith(`TC-FR${fr}-HUMAN-`)))];
    if (aiIds.length !== 35) addFinding(findings, 'ERROR', `FR-${fr} must contain exactly 35 unique AI IDs; found ${aiIds.length}`);
    else addFinding(findings, 'OK', `FR-${fr} has 35 unique AI IDs`);
    if (humanIds.length < 5) addFinding(findings, 'ERROR', `FR-${fr} must contain at least 5 unique HUMAN IDs; found ${humanIds.length}`);
    else addFinding(findings, 'OK', `FR-${fr} has ${humanIds.length} unique HUMAN IDs`);

    for (const id of aiIds) {
      const labels = auditVerdicts.get(id) ?? [];
      if (labels.length !== 1) addFinding(findings, 'ERROR', `${id} must have one authoritative audit verdict; found ${labels.length}`);
    }
  }

  let assertionIds = new Set();
  let collection = null;
  if (collectionPath) {
    collection = parseJson(resolve(rootDir, collectionPath), 'Postman collection', findings.errors);
    if (collection) {
      assertionIds = collectAssertionIds(collection);
      if (assertionIds.size === 0) addFinding(findings, 'ERROR', 'Postman collection has no case assertion IDs');
      else addFinding(findings, 'OK', `Postman collection registers ${assertionIds.size} case assertion IDs`);
      for (const request of collectCollectionRequests(collection)) {
        if (request.fr && request.route && !routeIsAllowed(request.fr, request.method, request.route)) {
          addFinding(findings, 'ERROR', `Postman FR-${request.fr} request ${request.method} ${request.route} is outside allowed scope`);
        }
      }
    }
  }
  if (environmentPath) parseJson(resolve(rootDir, environmentPath), 'Postman environment', findings.errors);

  if (auditPath && !existsSync(resolve(rootDir, auditPath))) {
    addFinding(findings, 'ERROR', `audit report is missing: ${auditPath}`);
  }

  if (traceabilityPath) {
    const traceability = safeRead(resolve(rootDir, traceabilityPath), findings.errors);
    if (traceability !== null) {
      const rows = parseTraceabilityRows(traceability);
      const authoredIds = new Set(allCaseIds);
      const rowsByCaseId = new Map();
      const rowsByAssertionId = new Map();
      for (const row of rows) {
        rowsByCaseId.set(row.caseId, [...(rowsByCaseId.get(row.caseId) ?? []), row]);
        if (row.assertionId) rowsByAssertionId.set(row.assertionId, [...(rowsByAssertionId.get(row.assertionId) ?? []), row]);
        if (!authoredIds.has(row.caseId)) addFinding(findings, 'ERROR', `traceability contains unknown case ID ${row.caseId}`);
        if (!EXECUTION_CLASSES.has(row.executionClass)) addFinding(findings, 'ERROR', `traceability case ${row.caseId} has invalid execution class ${row.executionClass ?? '(missing)'}`);
      }
      for (const id of authoredIds) {
        const count = rowsByCaseId.get(id)?.length ?? 0;
        if (count !== 1) addFinding(findings, 'ERROR', `authored case ID ${id} must appear exactly once in traceability; found ${count}`);
      }
      for (const id of assertionIds) {
        const mappedRows = rowsByAssertionId.get(id) ?? [];
        if (mappedRows.length !== 1 || mappedRows[0].executionClass !== 'NEWMAN') {
          addFinding(findings, 'ERROR', `automated assertion ${id} must appear exactly once in NEWMAN traceability`);
        }
      }
      const newmanRows = rows.filter((row) => row.executionClass === 'NEWMAN');
      for (const row of newmanRows) {
        if (!row.assertionId || !assertionIds.has(row.assertionId)) {
          addFinding(findings, 'ERROR', `traceability NEWMAN ID ${row.caseId} is missing from collection assertions`);
        }
        if (row.resultTarget !== `src/newman/member-2/fr-${row.fr}.json`) {
          addFinding(findings, 'ERROR', `traceability NEWMAN ID ${row.caseId} must target src/newman/member-2/fr-${row.fr}.json`);
        }
        if (row.route && !routeIsAllowed(row.fr, row.method, row.route)) {
          addFinding(findings, 'ERROR', `traceability NEWMAN ID ${row.caseId} uses method ${row.method ?? '(missing)'} ${row.route} outside FR-${row.fr} scope`);
        }
      }
      if (newmanRows.length === 0) addFinding(findings, 'WARNING', 'traceability has no NEWMAN rows yet');
    }
  }

  const evidencePaths = options.evidencePaths ?? listFiles(resolve(rootDir, 'src'));
  for (const path of evidencePaths) {
    const text = safeRead(path, findings.errors);
    if (text === null) continue;
    for (const violation of findForbiddenEvidence(text)) {
      addFinding(findings, 'ERROR', `${violation.code} in ${relative(rootDir, path)}: ${violation.detail}`);
    }
  }

  if (newmanPaths.length === 0) {
    addFinding(findings, 'WARNING', 'no Newman JSON reports exist yet');
  } else {
    try {
      const totals = loadNewmanTotals(newmanPaths);
      addFinding(findings, 'OK', `loaded ${totals.reports} Newman JSON report(s)`);
      for (const reportPath of reportPaths) {
        const report = safeRead(resolve(rootDir, reportPath), findings.errors);
        if (report === null) continue;
        const documented = documentedNewmanTotals(report);
        if (documented && (documented.requests !== totals.requests.total
          || documented.executed !== totals.executed
          || documented.passed !== totals.passed
          || documented.failed !== totals.failed)) {
          addFinding(findings, 'ERROR', `${reportPath} Newman totals (requests=${documented.requests}; executed=${documented.executed}; passed=${documented.passed}; failed=${documented.failed}) do not match JSON (requests=${totals.requests.total}; executed=${totals.executed}; passed=${totals.passed}; failed=${totals.failed})`);
        }
      }
    } catch (error) {
      addFinding(findings, 'ERROR', `cannot load Newman totals: ${error.message}`);
    }
  }

  return findings;
}

export function main(options = {}) {
  const findings = validateSubmission(options);
  for (const [level, messages] of Object.entries({ ERROR: findings.errors, WARNING: findings.warnings, OK: findings.oks })) {
    for (const message of messages) console.log(`${level} ${message}`);
  }
  return findings.errors.length === 0 ? 0 : 1;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = main();
}
