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
    assertions: { total: 0, failed: 0 },
    requests: { total: 0, failed: 0 },
  };

  for (const path of paths) {
    const report = JSON.parse(readFileSync(path, 'utf8'));
    const stats = report.run?.stats ?? {};
    totals.reports += 1;
    totals.assertions.total += Number(stats.assertions?.total ?? 0);
    totals.assertions.failed += Number(stats.assertions?.failed ?? 0);
    totals.requests.total += Number(stats.requests?.total ?? 0);
    totals.requests.failed += Number(stats.requests?.failed ?? 0);
  }

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

function documentedNewmanTotals(markdown) {
  const assertions = markdown.match(/Newman assertions?\s*[:=-]\s*(\d+)/i);
  const failures = markdown.match(/Newman (?:failures?|failed)\s*[:=-]\s*(\d+)/i);
  if (!assertions || !failures) return null;
  return { assertions: Number(assertions[1]), failures: Number(failures[1]) };
}

function findTraceabilityNewmanIds(markdown) {
  const ids = new Set();
  for (const line of String(markdown).split('\n')) {
    if (!/\|\s*NEWMAN\s*\|/i.test(line)) continue;
    for (const id of extractCaseIds(line)) ids.add(id);
  }
  return ids;
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
  if (collectionPath) {
    const collection = parseJson(resolve(rootDir, collectionPath), 'Postman collection', findings.errors);
    if (collection) {
      assertionIds = collectAssertionIds(collection);
      if (assertionIds.size === 0) addFinding(findings, 'ERROR', 'Postman collection has no case assertion IDs');
      else addFinding(findings, 'OK', `Postman collection registers ${assertionIds.size} case assertion IDs`);
    }
  }
  if (environmentPath) parseJson(resolve(rootDir, environmentPath), 'Postman environment', findings.errors);

  if (auditPath && !existsSync(resolve(rootDir, auditPath))) {
    addFinding(findings, 'ERROR', `audit report is missing: ${auditPath}`);
  }

  if (traceabilityPath) {
    const traceability = safeRead(resolve(rootDir, traceabilityPath), findings.errors);
    if (traceability !== null) {
      const traceabilityIds = new Set(extractCaseIds(traceability));
      const newmanIds = findTraceabilityNewmanIds(traceability);
      for (const id of assertionIds) {
        if (!traceabilityIds.has(id)) addFinding(findings, 'ERROR', `automated assertion ${id} is missing from traceability`);
      }
      for (const id of newmanIds) {
        if (!assertionIds.has(id)) addFinding(findings, 'ERROR', `traceability NEWMAN ID ${id} is missing from collection assertions`);
      }
      if (newmanIds.size === 0) addFinding(findings, 'WARNING', 'traceability has no NEWMAN rows yet');
    }
  }

  const evidenceDirectories = [
    'src/test-cases',
    'src/postman',
    'src/newman',
    'src/docs',
    'src/bug-reports',
  ];
  for (const path of evidenceDirectories.flatMap((directory) => listFiles(resolve(rootDir, directory)))) {
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
      const reportMarkdown = reportPaths
        .map((path) => safeRead(resolve(rootDir, path), findings.errors))
        .filter((text) => text !== null)
        .join('\n');
      const documented = documentedNewmanTotals(reportMarkdown);
      if (documented && (documented.assertions !== totals.assertions.total || documented.failures !== totals.assertions.failed)) {
        addFinding(findings, 'ERROR', `documented Newman totals (${documented.assertions}/${documented.failures}) do not match JSON (${totals.assertions.total}/${totals.assertions.failed})`);
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
