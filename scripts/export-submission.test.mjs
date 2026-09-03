import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import {
  parseCaseTables,
  buildExecutionSummary,
  renderReportHtml,
  buildWorkbookModel,
} from './export-submission.mjs';

const CASE_MD = `# FR-05

| Case ID | Verdict | Reason | Final intent | Class |
| --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | VALID | schema ok | list products | NEWMAN |
| TC-FR05-AI-002 | INVALID | duplicate | excluded | EXCLUDED |

| Case ID | Intent | Class | Why human |
| --- | --- | --- | --- |
| TC-FR05-HUMAN-001 | xss browser | BROWSER-MANUAL | DOM sink |
`;

const TRACE_MD = `# Trace

| Case ID | Final intent | Execution class | Postman | Assertion ID | Latest result source |
| --- | --- | --- | --- | --- | --- |
| TC-FR05-AI-001 | list | NEWMAN | GET /api/products | TC-FR05-AI-001 | src/newman/member-2/fr-05.json |
| TC-FR05-AI-002 | dup | EXCLUDED | Excluded | — | NOT-RUN-DUPLICATE |
| TC-FR05-HUMAN-001 | xss | BROWSER-MANUAL | Browser | — | MANUAL |
`;

const NEWMAN_SUMMARY = {
  generatedAt: '2026-09-03T02:43:08.840Z',
  suites: [
    {
      id: 'fr-05',
      assertions: { total: 1, executed: 1, passed: 1, failed: 0, pending: 0 },
      requests: { total: 2, executed: 2, passed: 2, failed: 0, pending: 0 },
      failures: 0,
    },
  ],
  assertions: { total: 1, executed: 1, passed: 1, failed: 0, pending: 0 },
  requests: { total: 2, executed: 2, passed: 2, failed: 0, pending: 0 },
  failures: 0,
  errors: 0,
  ok: true,
};

test('parseCaseTables reads audit and human rows', () => {
  const cases = parseCaseTables(CASE_MD, '05');
  assert.equal(cases.length, 3);
  assert.equal(cases[0].id, 'TC-FR05-AI-001');
  assert.equal(cases[0].verdict, 'VALID');
  assert.equal(cases[2].id, 'TC-FR05-HUMAN-001');
  assert.equal(cases[2].origin, 'HUMAN');
});

test('buildExecutionSummary uses Newman totals instead of README text', () => {
  const summary = buildExecutionSummary({
    newmanSummary: NEWMAN_SUMMARY,
    traceabilityMarkdown: TRACE_MD,
    casesByFr: { '05': parseCaseTables(CASE_MD, '05') },
    readmeText: '| Số test cases PASS | 999 |\n| authored | 0 |',
  });
  assert.equal(summary.assertions.total, 1);
  assert.equal(summary.assertions.passed, 1);
  assert.equal(summary.authored, 3);
  assert.equal(summary.automated, 1);
  assert.notEqual(summary.assertions.passed, 999);
});

test('renderReportHtml stamps git SHA and Newman timestamp', () => {
  const html = renderReportHtml('# Hello\n\nBody', {
    gitSha: 'abc123def',
    newmanTimestamp: '2026-09-03T02:43:08.840Z',
    title: 'Main report',
  });
  assert.match(html, /<h1>Hello<\/h1>/);
  assert.match(html, /abc123def/);
  assert.match(html, /2026-09-03T02:43:08.840Z/);
  assert.match(html, /charset=.utf-8/i);
});

test('workbook model contains required sheets and Newman-derived totals', () => {
  const model = buildWorkbookModel({
    casesByFr: {
      '05': parseCaseTables(CASE_MD, '05'),
      '08': [],
      '18': [],
    },
    traceabilityMarkdown: TRACE_MD,
    newmanSummary: NEWMAN_SUMMARY,
    gitSha: 'abc123def',
    newmanTimestamp: NEWMAN_SUMMARY.generatedAt,
  });
  assert.deepEqual(
    model.sheets.map((sheet) => sheet.name),
    ['Summary', 'FR-05', 'FR-08', 'FR-18', 'Audit', 'Traceability'],
  );
  const summarySheet = model.sheets[0];
  const passedRow = summarySheet.rows.find((row) => row[0] === 'assertions.passed');
  assert.deepEqual(passedRow, ['assertions.passed', 1]);
  assert.equal(model.sheets[1].rows.length, 3);
});

test('ExcelJS can materialize the workbook model', async () => {
  const { writeWorkbook } = await import('./export-submission.mjs');
  const dir = mkdtempSync(join(tmpdir(), 'hw06-export-'));
  const target = join(dir, 'cases.xlsx');
  const model = buildWorkbookModel({
    casesByFr: { '05': parseCaseTables(CASE_MD, '05'), '08': [], '18': [] },
    traceabilityMarkdown: TRACE_MD,
    newmanSummary: NEWMAN_SUMMARY,
    gitSha: 'abc123def',
    newmanTimestamp: NEWMAN_SUMMARY.generatedAt,
  });
  await writeWorkbook(model, target);
  const { default: ExcelJS } = await import('exceljs');
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(target);
  assert.deepEqual(workbook.worksheets.map((sheet) => sheet.name), [
    'Summary',
    'FR-05',
    'FR-08',
    'FR-18',
    'Audit',
    'Traceability',
  ]);
});
