import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import {
  collectAssertionIds,
  countAuditLabels,
  extractCaseIds,
  findForbiddenEvidence,
  loadNewmanTotals,
  validateSubmission,
} from './validate-submission.mjs';

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
      assertions: { total: 7, failed: 1 },
      requests: { total: 5, failed: 1 },
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
