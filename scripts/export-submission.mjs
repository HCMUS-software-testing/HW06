import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import ExcelJS from 'exceljs';
import { marked } from 'marked';

import { parseTraceabilityRows } from './validate-submission.mjs';

const CASE_ID_PATTERN = /TC-FR(?:05|08|18)-(?:AI|HUMAN)-\d{3}/;
const VERDICTS = new Set(['VALID', 'INVALID', 'INCOMPLETE']);

export function markdownCells(line) {
  const trimmed = String(line).trim();
  if (!trimmed.startsWith('|')) return [];
  const values = trimmed.split('|').map((cell) => cell.trim());
  if (values[0] === '') values.shift();
  if (trimmed.endsWith('|')) values.pop();
  return values;
}

function isSeparator(line) {
  return /^\|\s*:?-{3,}/.test(String(line).trim());
}

export function parseCaseTables(markdown, fr = '') {
  const lines = String(markdown).split('\n');
  const cases = [];
  const seen = new Set();

  for (const line of lines) {
    if (!line.trim().startsWith('|') || isSeparator(line)) continue;
    const cells = markdownCells(line);
    const idCell = cells.find((cell) => CASE_ID_PATTERN.test(cell)) ?? '';
    const id = idCell.match(CASE_ID_PATTERN)?.[0];
    if (!id || seen.has(id)) continue;
    seen.add(id);
    const verdict = cells.find((cell) => VERDICTS.has(cell.toUpperCase()))?.toUpperCase() ?? '';
    const origin = id.includes('-HUMAN-') ? 'HUMAN' : 'AI';
    cases.push({
      id,
      fr: fr || id.slice(5, 7),
      origin,
      verdict,
      intent: cells[1] && cells[1] !== id ? cells[1] : (cells[3] ?? cells[2] ?? ''),
      executionClass: cells.find((cell) => /^(NEWMAN|BROWSER-MANUAL|FAULT-INJECTION|EXCLUDED)$/i.test(cell))?.toUpperCase() ?? '',
      raw: cells,
    });
  }

  return cases;
}

export function buildExecutionSummary({ newmanSummary, traceabilityMarkdown, casesByFr = {}, readmeText = '' }) {
  void readmeText;
  const rows = parseTraceabilityRows(traceabilityMarkdown ?? '');
  const authoredCases = Object.values(casesByFr).flat();
  const authored = authoredCases.length || new Set(rows.map((row) => row.caseId)).size;
  const automated = rows.filter((row) => row.executionClass === 'NEWMAN').length;
  const assertions = newmanSummary?.assertions ?? { total: 0, executed: 0, passed: 0, failed: 0, pending: 0 };
  const requests = newmanSummary?.requests ?? { total: 0, executed: 0, passed: 0, failed: 0, pending: 0 };
  return {
    authored,
    automated,
    assertions,
    requests,
    failures: newmanSummary?.failures ?? assertions.failed ?? 0,
    generatedAt: newmanSummary?.generatedAt ?? '',
    suites: newmanSummary?.suites ?? [],
  };
}

export function renderReportHtml(markdown, { gitSha = '', newmanTimestamp = '', title = 'HW06 report' } = {}) {
  const body = marked.parse(String(markdown), { async: false });
  return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>${escapeHtml(title)}</title>
  <style>
    body { font-family: "Noto Sans", "DejaVu Sans", sans-serif; margin: 32px; color: #111; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 6px 8px; vertical-align: top; }
    code { font-family: ui-monospace, monospace; }
    .stamp { color: #555; font-size: 12px; margin-bottom: 24px; }
  </style>
</head>
<body>
  <p class="stamp">Git SHA: ${escapeHtml(gitSha)} · Newman run: ${escapeHtml(newmanTimestamp)}</p>
  ${body}
</body>
</html>
`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

export function buildWorkbookModel({
  casesByFr,
  traceabilityMarkdown,
  newmanSummary,
  gitSha = '',
  newmanTimestamp = '',
}) {
  const summary = buildExecutionSummary({
    newmanSummary,
    traceabilityMarkdown,
    casesByFr,
  });
  const rows = parseTraceabilityRows(traceabilityMarkdown);
  const allCases = ['05', '08', '18'].flatMap((fr) => casesByFr[fr] ?? []);

  return {
    gitSha,
    newmanTimestamp,
    sheets: [
      {
        name: 'Summary',
        headers: ['Metric', 'Value'],
        rows: [
          ['gitSha', gitSha],
          ['newmanTimestamp', newmanTimestamp],
          ['authored', summary.authored],
          ['automated', summary.automated],
          ['assertions.total', summary.assertions.total],
          ['assertions.executed', summary.assertions.executed],
          ['assertions.passed', summary.assertions.passed],
          ['assertions.failed', summary.assertions.failed],
          ['assertions.pending', summary.assertions.pending],
          ['requests.total', summary.requests.total],
        ],
      },
      ...['05', '08', '18'].map((fr) => ({
        name: `FR-${fr}`,
        headers: ['Case ID', 'Origin', 'Verdict', 'Execution class', 'Intent'],
        rows: (casesByFr[fr] ?? []).map((item) => [
          item.id,
          item.origin,
          item.verdict,
          item.executionClass,
          item.intent,
        ]),
      })),
      {
        name: 'Audit',
        headers: ['Case ID', 'FR', 'Origin', 'Verdict'],
        rows: allCases.map((item) => [item.id, item.fr, item.origin, item.verdict]),
      },
      {
        name: 'Traceability',
        headers: ['Case ID', 'FR', 'Execution class', 'Assertion ID', 'Method', 'Route', 'Result target'],
        rows: rows.map((row) => [
          row.caseId,
          row.fr,
          row.executionClass,
          row.assertionId ?? '',
          row.method ?? '',
          row.route ?? '',
          row.resultTarget,
        ]),
      },
    ],
  };
}

export async function writeWorkbook(model, targetPath) {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = 'HW06 member-2 exporter';
  for (const sheet of model.sheets) {
    const worksheet = workbook.addWorksheet(sheet.name);
    worksheet.views = [{ state: 'frozen', ySplit: 1 }];
    worksheet.addTable({
      name: sheet.name.replace(/[^A-Za-z0-9]/g, '') || 'Table',
      ref: 'A1',
      headerRow: true,
      totalsRow: false,
      columns: sheet.headers.map((header) => ({ name: header, filterButton: true })),
      rows: sheet.rows.length > 0 ? sheet.rows : [sheet.headers.map(() => '')],
    });
    worksheet.columns.forEach((column) => {
      column.width = 28;
    });
  }
  mkdirSync(dirname(targetPath), { recursive: true });
  await workbook.xlsx.writeFile(targetPath);
}

function currentGitSha(rootDir) {
  try {
    return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: rootDir, encoding: 'utf8' }).trim();
  } catch (error) {
    try {
      const head = readFileSync(resolve(rootDir, '.git/HEAD'), 'utf8').trim();
      if (head.startsWith('ref:')) {
        return readFileSync(resolve(rootDir, '.git', head.slice(4).trim()), 'utf8').trim();
      }
      return head;
    } catch {
      return `UNAVAILABLE:${error.message}`;
    }
  }
}

export async function exportSubmission(options = {}) {
  const rootDir = resolve(options.rootDir ?? process.cwd());
  const gitSha = options.gitSha ?? currentGitSha(rootDir);
  const newmanSummary = JSON.parse(readFileSync(resolve(rootDir, 'src/newman/member-2/summary.json'), 'utf8'));
  const newmanTimestamp = newmanSummary.generatedAt ?? '';
  const casesByFr = {
    '05': parseCaseTables(readFileSync(resolve(rootDir, 'src/test-cases/member-2-fr-05.md'), 'utf8'), '05'),
    '08': parseCaseTables(readFileSync(resolve(rootDir, 'src/test-cases/member-2-fr-08.md'), 'utf8'), '08'),
    '18': parseCaseTables(readFileSync(resolve(rootDir, 'src/test-cases/member-2-fr-18.md'), 'utf8'), '18'),
  };
  const traceabilityMarkdown = readFileSync(resolve(rootDir, 'src/test-cases/member-2-traceability.md'), 'utf8');
  const model = buildWorkbookModel({
    casesByFr,
    traceabilityMarkdown,
    newmanSummary,
    gitSha,
    newmanTimestamp,
  });
  const xlsxPath = resolve(rootDir, options.xlsxPath ?? 'src/test-cases/23127075-hw06-test-cases.xlsx');
  await writeWorkbook(model, xlsxPath);

  if (options.writeHtml !== false) {
    const reports = options.reports ?? [
      { source: 'src/docs/main-report.md', title: 'Main report' },
      { source: 'src/docs/ai-critique.md', title: 'AI critique' },
      { source: 'src/docs/cicd-report.md', title: 'CI/CD report' },
      { source: 'src/ai-audit/ai_audit_report.md', title: 'AI audit report' },
    ];
    for (const report of reports) {
      const markdown = readFileSync(resolve(rootDir, report.source), 'utf8');
      const html = renderReportHtml(markdown, { gitSha, newmanTimestamp, title: report.title });
      if (options.htmlDir) {
        const fileName = report.source.split('/').pop().replace(/\.md$/, '.html');
        writeFileSync(resolve(rootDir, options.htmlDir, fileName), html);
      }
    }
  }

  return { xlsxPath, gitSha, newmanTimestamp, summary: buildExecutionSummary({ newmanSummary, traceabilityMarkdown, casesByFr }) };
}

export async function main(options = {}) {
  const result = await exportSubmission(options);
  console.log(`Wrote ${result.xlsxPath}`);
  console.log(`Git SHA ${result.gitSha}`);
  console.log(`Newman ${result.newmanTimestamp}`);
  return 0;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then((code) => {
    process.exitCode = code;
  }).catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}
