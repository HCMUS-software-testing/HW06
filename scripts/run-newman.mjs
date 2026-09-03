import { existsSync } from 'node:fs';
import {
  mkdir,
  mkdtemp,
  readFile,
  rename,
  rm,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import newman from 'newman';

const JWT_PATTERN = /eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g;
const BEARER_PATTERN = /Bearer\s+[A-Za-z0-9._~+/=-]+/gi;
const AUTHORIZATION_TEXT_PATTERN = /Authorization\s*:\s*[^\r\n<]+/gi;
const SENSITIVE_NAME = '(?:password|adminPassword|userPassword|token|accessToken|adminToken|userToken|adminEmail|userEmail)';
const JSON_SECRET_PATTERN = new RegExp(`((?:["'])${SENSITIVE_NAME}(?:["'])\\s*:\\s*(?:["']))[^"'\\r\\n]*((?:["']))`, 'gi');
const HTML_SECRET_PATTERN = new RegExp(`((?:&quot;|&#34;)${SENSITIVE_NAME}(?:&quot;|&#34;)\\s*:\\s*(?:&quot;|&#34;)).*?((?:&quot;|&#34;))`, 'gi');
const PLAIN_SECRET_PATTERN = new RegExp(`(\\b${SENSITIVE_NAME}\\s*[=:]\\s*)[^\\s&<]+`, 'gi');
const SENSITIVE_KEY_PATTERN = /^(?:authorization|proxy-authorization|token|accessToken|adminToken|userToken|password|adminPassword|userPassword|adminEmail|userEmail)$/i;

function redactText(value) {
  return String(value)
    .replace(HTML_SECRET_PATTERN, '$1[REDACTED]$2')
    .replace(JSON_SECRET_PATTERN, '$1[REDACTED]$2')
    .replace(PLAIN_SECRET_PATTERN, '$1[REDACTED]')
    .replace(AUTHORIZATION_TEXT_PATTERN, 'Authorization: [REDACTED]')
    .replace(BEARER_PATTERN, 'Bearer [REDACTED]')
    .replace(JWT_PATTERN, '[REDACTED]');
}

function redactValue(value, seen) {
  if (typeof value === 'string') return redactText(value);
  if (value === null || typeof value !== 'object') return value;
  if (seen.has(value)) return '[REDACTED:CIRCULAR]';
  seen.add(value);

  if (Array.isArray(value)) {
    const result = value.map((entry) => redactValue(entry, seen));
    seen.delete(value);
    return result;
  }

  const sensitiveVariable = typeof value.key === 'string' && SENSITIVE_KEY_PATTERN.test(value.key);
  const result = {};
  for (const [key, entry] of Object.entries(value)) {
    if (SENSITIVE_KEY_PATTERN.test(key)
      || (sensitiveVariable && /^(?:value|current|initial)$/i.test(key))) {
      result[key] = '[REDACTED]';
    } else {
      result[key] = redactValue(entry, seen);
    }
  }
  seen.delete(value);
  return result;
}

export function redactReport(report) {
  return redactValue(report, new WeakSet());
}

export function serializeReport(report) {
  return `${JSON.stringify(redactReport(report))}\n`;
}


export function buildRuns(options = {}) {
  const rootDir = resolve(options.rootDir ?? process.cwd());
  const outputDir = resolve(options.outputDir ?? join(rootDir, 'src/newman/member-2'));
  const collection = join(rootDir, 'src/postman/HW06_API_Testing.postman_collection.json');
  const environment = join(rootDir, 'src/postman/HW06_Local.postman_environment.json');
  const definitions = [
    ['fr-05', 'FR-05 - Product Search', 'fr-05-search.json'],
    ['fr-08', 'FR-08 - Checkout', 'fr-08-checkout.json'],
    ['fr-18', 'FR-18 - Admin Orders', 'fr-18-admin.json'],
  ];

  return definitions.map(([id, folder, dataFile]) => ({
    id,
    folder,
    collection,
    environment,
    data: join(rootDir, 'src/postman/data', dataFile),
    outputBase: join(outputDir, id),
  }));
}

function countStats(stats = {}) {
  const total = Number(stats.total ?? 0);
  const failed = Number(stats.failed ?? 0);
  const pending = Math.min(total, Number(stats.pending ?? 0) + Number(stats.skipped ?? 0));
  const executed = Math.max(0, total - pending);
  const passed = Math.max(0, executed - failed);
  return { total, executed, passed, failed, pending };
}

function addStats(target, source) {
  for (const key of ['total', 'executed', 'passed', 'failed', 'pending']) {
    target[key] += source[key];
  }
}

export function summarizeRuns(results) {
  const aggregate = {
    generatedAt: new Date().toISOString(),
    suites: [],
    assertions: { total: 0, executed: 0, passed: 0, failed: 0, pending: 0 },
    requests: { total: 0, executed: 0, passed: 0, failed: 0, pending: 0 },
    failures: 0,
    errors: 0,
    ok: true,
  };

  for (const result of results) {
    const run = result.summary?.run ?? {};
    const assertions = countStats(run.stats?.assertions);
    const requests = countStats(run.stats?.requests);
    const failures = Array.isArray(run.failures) ? run.failures.length : 0;
    const error = result.error ? redactText(result.error.message ?? result.error) : null;
    addStats(aggregate.assertions, assertions);
    addStats(aggregate.requests, requests);
    aggregate.failures += failures;
    if (error) aggregate.errors += 1;
    aggregate.suites.push({
      id: result.id,
      assertions,
      requests,
      failures,
      error,
      outputs: result.outputs,
    });
  }

  aggregate.ok = aggregate.assertions.failed === 0
    && aggregate.requests.failed === 0
    && aggregate.failures === 0
    && aggregate.errors === 0;
  return aggregate;
}

async function atomicWrite(path, contents) {
  await mkdir(dirname(path), { recursive: true });
  const temporary = `${path}.${process.pid}.${Math.random().toString(16).slice(2)}.tmp`;
  await writeFile(temporary, contents, 'utf8');
  await rename(temporary, path);
}

async function readOr(path, fallback) {
  if (!existsSync(path)) return fallback;
  return readFile(path, 'utf8');
}

function runNewman(newmanRun, options) {
  return new Promise((resolveRun) => {
    let settled = false;
    const finish = (error, summary) => {
      if (settled) return;
      settled = true;
      resolveRun({ error, summary });
    };

    try {
      newmanRun(options, finish);
    } catch (error) {
      finish(error, null);
    }
  });
}

async function captureCliOutput(run) {
  const output = [];
  const capture = (stream) => {
    const original = stream.write;
    stream.write = function captureWrite(chunk, encoding, callback) {
      output.push(Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk));
      if (typeof encoding === 'function') encoding();
      if (typeof callback === 'function') callback();
      return true;
    };
    return () => { stream.write = original; };
  };
  const restoreStdout = capture(process.stdout);
  const restoreStderr = capture(process.stderr);

  try {
    return { result: await run(), output: output.join('') };
  } finally {
    restoreStdout();
    restoreStderr();
  }
}

async function persistRun(run, rawPaths, result) {
  const fallbackReport = JSON.stringify(result.summary ?? {
    error: result.error ? { message: result.error.message } : null,
    run: { stats: {}, failures: [] },
  });
  const rawJson = await readOr(rawPaths.json, fallbackReport);
  let parsedJson;
  try {
    parsedJson = JSON.parse(rawJson);
  } catch {
    parsedJson = { raw: rawJson };
  }
  const rawHtml = await readOr(
    rawPaths.html,
    '<html><body><pre>HTML reporter output was not produced.</pre></body></html>',
  );
  const rawCli = await readOr(rawPaths.txt, '');
  const outputs = {
    json: `${run.outputBase}.json`,
    html: `${run.outputBase}.html`,
    txt: `${run.outputBase}.txt`,
  };

  await atomicWrite(outputs.json, serializeReport(parsedJson));
  await atomicWrite(outputs.html, redactText(rawHtml));
  await atomicWrite(outputs.txt, redactText(rawCli));
  return outputs;
}

export async function runSuites(options = {}) {
  const newmanRun = options.newmanRun ?? newman.run.bind(newman);
  const runs = options.runs ?? buildRuns(options);
  const outputDir = resolve(options.outputDir ?? join(options.rootDir ?? process.cwd(), 'src/newman/member-2'));
  const temporaryDir = await mkdtemp(join(tmpdir(), 'hw06-newman-'));
  const results = [];

  try {
    for (const run of runs) {
      const rawPaths = {
        json: join(temporaryDir, `${run.id}.json`),
        html: join(temporaryDir, `${run.id}.html`),
        txt: join(temporaryDir, `${run.id}.txt`),
      };
      const captured = await captureCliOutput(() => runNewman(newmanRun, {
        collection: run.collection,
        environment: run.environment,
        iterationData: run.data,
        folder: [run.folder],
        reporters: ['cli', 'json', 'htmlextra'],
        reporter: {
          json: { export: rawPaths.json },
          htmlextra: { export: rawPaths.html },
        },
        color: 'off',
      }));
      const result = captured.result;
      await writeFile(rawPaths.txt, captured.output, 'utf8');
      const outputs = await persistRun(run, rawPaths, result);
      results.push({ id: run.id, ...result, outputs });
    }

    const summary = summarizeRuns(results);
    await atomicWrite(join(outputDir, 'summary.json'), `${JSON.stringify(redactReport(summary), null, 2)}\n`);
    return summary;
  } finally {
    await rm(temporaryDir, { recursive: true, force: true });
  }
}

async function main() {
  const summary = await runSuites();
  process.exitCode = summary.ok ? 0 : 1;
}

const entryPath = process.argv[1] ? resolve(process.argv[1]) : null;
if (entryPath === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(redactText(error.stack ?? error.message ?? error));
    process.exitCode = 1;
  });
}
