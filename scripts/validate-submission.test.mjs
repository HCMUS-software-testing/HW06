import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import {
  collectAssertionIds,
  countAuditLabels,
  extractCaseIds,
  findForbiddenEvidence,
  loadNewmanTotals,
  main,
  validateSubmission,
} from './validate-submission.mjs';

const FR_SPECS = {
  '05': { method: 'GET', route: '/api/products' },
  '08': { method: 'POST', route: '/api/checkout' },
  '18': { method: 'GET', route: '/api/admin/orders' },
};

function caseIds(fr, kind, count) {
  return Array.from({ length: count }, (_, index) => `TC-FR${fr}-${kind}-${String(index + 1).padStart(3, '0')}`);
}

function writeFile(root, path, text) {
  const target = join(root, path);
  mkdirSync(join(target, '..'), { recursive: true });
  writeFileSync(target, text);
}

function buildTraceRows({ omitIds = [], routeOverrides = {}, procedureOverrides = {} } = {}) {
  const omitted = new Set(omitIds);
  const rows = [
    '| Case ID | Final intent | Execution class | Procedure | Assertion ID | Latest result source |',
    '| --- | --- | --- | --- | --- | --- |',
  ];

  for (const fr of Object.keys(FR_SPECS)) {
    const route = routeOverrides[fr] ?? FR_SPECS[fr].route;
    for (const id of caseIds(fr, 'AI', 35)) {
      const procedure = procedureOverrides[fr] ?? `${FR_SPECS[fr].method} ${route}`;
      if (!omitted.has(id)) rows.push(`| ${id} | final | NEWMAN | ${procedure} | ${id} | src/newman/member-2/fr-${fr}.json |`);
    }
    for (const id of caseIds(fr, 'HUMAN', 5)) {
      if (!omitted.has(id)) rows.push(`| ${id} | manual | BROWSER-MANUAL | manual procedure | - | NOT-RUN-NO-SUT-HOOK |`);
    }
  }

  return rows.join('\n');
}

function buildCollection({ omitAssertions = [], requestOverrides = {} } = {}) {
  const omitted = new Set(omitAssertions);
  return {
    item: Object.entries(FR_SPECS).map(([fr, expected]) => {
      const request = requestOverrides[fr] ?? expected;
      return {
        name: `FR-${fr}`,
        item: [{
          name: `${request.method} ${request.route}`,
          request: { method: request.method, url: { raw: `{{baseUrl}}${request.route}` } },
          event: [{
            listen: 'test',
            script: { exec: caseIds(fr, 'AI', 35)
              .filter((id) => !omitted.has(id))
              .map((id) => `pm.test('${id} | assertion', () => {});`) },
          }],
        }],
      };
    }),
  };
}

function writeSubmissionFixture(root, options = {}) {
  for (const fr of Object.keys(FR_SPECS)) {
    const rows = [
      ...caseIds(fr, 'AI', 35).map((id) => `| ${id} | VALID | final audit verdict |`),
      ...caseIds(fr, 'HUMAN', 5).map((id) => `| ${id} | human-designed case |`),
    ];
    writeFile(root, `src/test-cases/member-2-fr-${fr}.md`, rows.join('\n'));
  }
  writeFile(root, 'src/test-cases/member-2-traceability.md', buildTraceRows(options));
  writeFile(root, 'src/postman/HW06_API_Testing.postman_collection.json', JSON.stringify(buildCollection(options)));
  writeFile(root, 'src/postman/HW06_Local.postman_environment.json', '{}');
  writeFile(root, 'src/ai-audit/ai_audit_report.md', options.auditMarkdown ?? '# Audit log');
  writeFile(root, 'src/README.md', options.readmeMarkdown ?? '# Submission');
  writeFile(root, 'src/docs/main-report.md', options.mainReportMarkdown ?? '# Main report');
  writeFile(root, 'src/docs/cicd-report.md', '# CI report');
}

function runFixture(options, assertion) {
  const root = mkdtempSync(join(tmpdir(), 'hw06-validator-cli-'));
  const output = [];
  const originalLog = console.log;

  try {
    writeSubmissionFixture(root, options);
    console.log = (message) => output.push(message);
    const exitCode = main({ rootDir: root });
    assertion({ exitCode, output });
  } finally {
    console.log = originalLog;
    rmSync(root, { recursive: true, force: true });
  }
}

test('extractCaseIds returns every case ID so duplicate inventory rows are visible', () => {
  const markdown = [
    '| TC-FR05-AI-001 | generated case |',
    '| TC-FR05-AI-001 | duplicated case |',
    '| TC-FR05-HUMAN-001 | human case |',
  ].join('\n');

  assert.deepEqual(extractCaseIds(markdown), [
    'TC-FR05-AI-001',
    'TC-FR05-AI-001',
    'TC-FR05-HUMAN-001',
  ]);
});

test('countAuditLabels counts authoritative AI audit verdict labels', () => {
  const markdown = [
    '| TC-FR08-AI-001 | VALID | clear oracle |',
    '| TC-FR08-AI-002 | INVALID | stale endpoint |',
    '| TC-FR08-AI-003 | INCOMPLETE | missing fixture |',
  ].join('\n');

  assert.deepEqual(countAuditLabels(markdown), {
    VALID: 1,
    INVALID: 1,
    INCOMPLETE: 1,
  });
});

test('collectAssertionIds finds case IDs used by Postman test assertions', () => {
  const collection = {
    item: [{
      name: 'FR-18',
      item: [{
        name: 'GET /api/admin/orders',
        event: [{
          listen: 'test',
          script: { exec: [
            "pm.test('TC-FR18-AI-001 | admin list succeeds', () => {});",
            "pm.test('TC-FR18-HUMAN-001 | rejects forged role', () => {});",
          ] },
        }],
      }],
    }],
  };

  assert.deepEqual([...collectAssertionIds(collection)], [
    'TC-FR18-AI-001',
    'TC-FR18-HUMAN-001',
  ]);
});

test('loadNewmanTotals aggregates Newman JSON report totals', () => {
  const directory = mkdtempSync(join(tmpdir(), 'hw06-newman-'));
  const first = join(directory, 'fr-05.json');
  const second = join(directory, 'fr-08.json');

  try {
    writeFileSync(first, JSON.stringify({
      run: { stats: { assertions: { total: 3, failed: 1 }, requests: { total: 2, failed: 0 } } },
    }));
    writeFileSync(second, JSON.stringify({
      run: { stats: { assertions: { total: 4, failed: 0 }, requests: { total: 3, failed: 1 } } },
    }));

    assert.deepEqual(loadNewmanTotals([first, second]), {
      reports: 2,
      assertions: { total: 7, executed: 7, passed: 6, failed: 1 },
      requests: { total: 5, executed: 5, passed: 4, failed: 1 },
      executed: 7,
      passed: 6,
      failed: 1,
    });
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('findForbiddenEvidence rejects stale endpoints, all-zero SHAs, JWTs, and false completed claims', () => {
  const violations = findForbiddenEvidence([
    'Legacy endpoint: /api/products/search',
    'Checkout endpoint: /api/orders/checkout',
    'Source SHA: 0000000000000000000000000000000000000000',
    'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature',
    'Newman execution: COMPLETED; Screenshot: MANUAL-EVIDENCE-REQUIRED',
  ].join('\n'));

  assert.deepEqual(violations.map((violation) => violation.code), [
    'STALE_ENDPOINT',
    'STALE_ENDPOINT',
    'ZERO_SHA',
    'JWT',
    'COMPLETED_WITH_MANUAL_EVIDENCE',
  ]);
});

test('validateSubmission reports duplicate case IDs as machine-readable errors', () => {
  const directory = mkdtempSync(join(tmpdir(), 'hw06-validator-'));

  try {
    writeFileSync(join(directory, 'inventory.md'), [
      '| TC-FR05-AI-001 | one |',
      '| TC-FR05-AI-001 | duplicate |',
    ].join('\n'));

    const result = validateSubmission({
      rootDir: directory,
      caseFiles: [{ fr: '05', path: 'inventory.md' }],
      collectionPath: null,
      environmentPath: null,
      auditPath: null,
      traceabilityPath: null,
      reportPaths: [],
      newmanPaths: [],
    });

    assert.ok(result.errors.some((message) => message.includes('duplicate case ID TC-FR05-AI-001')));
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('CLI rejects forbidden JWT and completed manual-evidence claims in the AI audit log', () => {
  runFixture({
    auditMarkdown: 'Status: COMPLETED; Screenshot: MANUAL-EVIDENCE-REQUIRED\nAuthorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature',
  }, ({ exitCode, output }) => {
    assert.equal(exitCode, 1);
    assert.ok(output.some((line) => line.startsWith('ERROR JWT in src/ai-audit/ai_audit_report.md')));
    assert.ok(output.some((line) => line.startsWith('ERROR COMPLETED_WITH_MANUAL_EVIDENCE in src/ai-audit/ai_audit_report.md')));
  });
});

test('CLI requires every authored ID exactly once in traceability', () => {
  runFixture({ omitIds: ['TC-FR08-HUMAN-005'] }, ({ exitCode, output }) => {
    assert.equal(exitCode, 1);
    assert.ok(output.includes('ERROR authored case ID TC-FR08-HUMAN-005 must appear exactly once in traceability; found 0'));
  });
});

test('CLI requires NEWMAN traceability rows to resolve to collection assertions', () => {
  runFixture({ omitAssertions: ['TC-FR18-AI-035'] }, ({ exitCode, output }) => {
    assert.equal(exitCode, 1);
    assert.ok(output.includes('ERROR traceability NEWMAN ID TC-FR18-AI-035 is missing from collection assertions'));
  });
});

test('CLI rejects out-of-scope methods and routes in Postman and NEWMAN traceability', () => {
  runFixture({
    requestOverrides: { '05': { method: 'POST', route: '/api/products/:id' } },
    procedureOverrides: { '05': 'POST /api/products' },
  }, ({ exitCode, output }) => {
    assert.equal(exitCode, 1);
    assert.ok(output.some((line) => line.includes('Postman FR-05 request POST /api/products/:id is outside allowed scope')));
    assert.ok(output.some((line) => line.includes('traceability NEWMAN ID TC-FR05-AI-001 uses method POST /api/products outside FR-05 scope')));
  });
});

test('CLI rejects README and main-report totals that disagree with Newman JSON', () => {
  const root = mkdtempSync(join(tmpdir(), 'hw06-validator-totals-'));
  const output = [];
  const originalLog = console.log;

  try {
    writeSubmissionFixture(root, {
      readmeMarkdown: 'Newman totals: requests=99; executed=99; passed=99; failed=0',
      mainReportMarkdown: 'Newman totals: requests=3; executed=7; passed=6; failed=1',
    });
    writeFile(root, 'src/newman/member-2/fr-05.json', JSON.stringify({
      run: { stats: { assertions: { total: 7, failed: 1 }, requests: { total: 3, failed: 1 } } },
    }));
    console.log = (message) => output.push(message);
    const exitCode = main({ rootDir: root });

    assert.equal(exitCode, 1);
    assert.ok(output.some((line) => line.includes('src/README.md Newman totals')));
    assert.ok(!output.some((line) => line.includes('src/docs/main-report.md Newman totals')));
  } finally {
    console.log = originalLog;
    rmSync(root, { recursive: true, force: true });
  }
});
