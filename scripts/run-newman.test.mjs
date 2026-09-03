import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import postmanCollection from 'postman-collection';

import {
  buildRuns,
  redactReport,
  runSuites,
  summarizeRuns,
} from './run-newman.mjs';

const JWT = ['eyJhbGciOiJIUzI1NiJ9', 'eyJzdWIiOiIxIn0', 'signature'].join('.');
const { Collection } = postmanCollection;

test('selected collection requests retain executable URLs after Postman SDK parsing', () => {
  const source = JSON.parse(readFileSync('src/postman/HW06_API_Testing.postman_collection.json', 'utf8'));
  const collection = new Collection(source);

  for (const folderName of [
    'FR-05 - Product Search',
    'FR-08 - Checkout',
    'FR-18 - Admin Orders',
  ]) {
    const folder = collection.items.all().find((item) => item.name === folderName);
    assert.ok(folder, `${folderName} should exist`);
    folder.items.each((item) => {
      assert.notEqual(item.request.url.toString(), '', `${folderName} / ${item.name} should have a URL`);
    });
  }
});

test('the simultaneous checkout final request uses the prepared user A token', () => {
  const collection = JSON.parse(readFileSync('src/postman/HW06_API_Testing.postman_collection.json', 'utf8'));
  const checkoutData = JSON.parse(readFileSync('src/postman/data/fr-08-checkout.json', 'utf8'));
  const checkoutFolder = collection.item.find((item) => item.name === 'FR-08 - Checkout');
  const finalRequest = checkoutFolder.item.find((item) => item.name === 'TC-FR08-HUMAN-008 - simultaneous checkout');
  const finalAuthorization = finalRequest.request.header
    .find((header) => header.key.toLowerCase() === 'authorization');
  const row = checkoutData.find((entry) => entry.caseId === 'TC-FR08-HUMAN-008');

  assert.equal(row.authMode, 'user');
  assert.equal(finalAuthorization?.value, 'Bearer {{caseUserTokenA}}');
});

test('controller exclusion leaves exactly 91 executable IDs and no unsupported cart workflows', () => {
  const collection = JSON.parse(readFileSync('src/postman/HW06_API_Testing.postman_collection.json', 'utf8'));
  const checkoutData = JSON.parse(readFileSync('src/postman/data/fr-08-checkout.json', 'utf8'));
  const traceability = readFileSync('src/test-cases/member-2-traceability.md', 'utf8');
  const checkoutFolder = collection.item.find((item) => item.name === 'FR-08 - Checkout');
  const removedIds = ['TC-FR08-HUMAN-005', 'TC-FR08-HUMAN-006', 'TC-FR08-HUMAN-009'];
  const assertionIds = [];
  const walk = (items) => items.forEach((item) => {
    if (item.item) walk(item.item);
    for (const event of item.event ?? []) {
      if (event.listen !== 'test') continue;
      for (const line of event.script?.exec ?? []) {
        assertionIds.push(...String(line).match(/TC-FR(?:05|08|18)-(?:AI|HUMAN)-\d{3}/g) ?? []);
      }
    }
  });
  walk(collection.item);

  assert.equal(assertionIds.length, 91);
  assert.deepEqual(Object.fromEntries(['05', '08', '18'].map((fr) => [
    fr,
    assertionIds.filter((id) => id.slice(5, 7) === fr).length,
  ])), { '05': 32, '08': 24, '18': 35 });
  for (const id of removedIds) {
    assert.equal(checkoutData.some((row) => row.caseId === id), false);
    assert.equal(checkoutFolder.item.some((item) => item.name.startsWith(id)), false);
    assert.match(traceability, new RegExp('\\| ' + id + ' \\|.*?\\| EXCLUDED \\|.*?\\| — \\| .*NOT-RUN-NO-SUT-HOOK'));
  }
  assert.doesNotMatch(JSON.stringify(collection), /DELETE', '\/api\/cart\//);
});

test('buildRuns pairs each selected FR folder with its deterministic data partition', () => {
  const runs = buildRuns({ rootDir: '/repo', outputDir: '/evidence' });

  assert.deepEqual(runs.map(({ id, folder, data, outputBase }) => ({
    id,
    folder,
    data,
    outputBase,
  })), [
    {
      id: 'fr-05',
      folder: 'FR-05 - Product Search',
      data: '/repo/src/postman/data/fr-05-search.json',
      outputBase: '/evidence/fr-05',
    },
    {
      id: 'fr-08',
      folder: 'FR-08 - Checkout',
      data: '/repo/src/postman/data/fr-08-checkout.json',
      outputBase: '/evidence/fr-08',
    },
    {
      id: 'fr-18',
      folder: 'FR-18 - Admin Orders',
      data: '/repo/src/postman/data/fr-18-admin.json',
      outputBase: '/evidence/fr-18',
    },
  ]);

  for (const run of runs) {
    assert.equal(run.collection, '/repo/src/postman/HW06_API_Testing.postman_collection.json');
    assert.equal(run.environment, '/repo/src/postman/HW06_Local.postman_environment.json');
  }
});

test('summarizeRuns excludes pending and skipped assertions from pass totals', () => {
  const summary = summarizeRuns([
    {
      id: 'fr-05',
      summary: {
        run: {
          stats: {
            assertions: { total: 6, failed: 1, pending: 1, skipped: 1 },
            requests: { total: 4, failed: 0, pending: 1 },
          },
          failures: [{ error: { message: 'oracle mismatch' } }],
        },
      },
    },
    {
      id: 'fr-08',
      summary: {
        run: {
          stats: {
            assertions: { total: 4, failed: 1 },
            requests: { total: 3, failed: 1 },
          },
          failures: [{ error: { message: 'request failed' } }],
        },
      },
    },
  ]);

  assert.deepEqual(summary.assertions, {
    total: 10,
    executed: 8,
    passed: 6,
    failed: 2,
    pending: 2,
  });
  assert.deepEqual(summary.requests, {
    total: 7,
    executed: 6,
    passed: 5,
    failed: 1,
    pending: 1,
  });
  assert.equal(summary.failures, 2);
  assert.equal(summary.ok, false);
});

test('redactReport removes authorization values, token fields, and JWT-shaped strings without mutating input', () => {
  const source = {
    request: {
      headers: [{ key: 'Authorization', value: `Bearer ${JWT}` }],
      description: `captured ${JWT}`,
      body: {
        raw: '{"userEmail":"owner@example.test","password":"NotForReports!"}',
      },
    },
    environment: {
      values: [
        { key: 'userToken', value: JWT },
        { key: 'studentId', value: '23127075' },
      ],
    },
    response: `Authorization: Bearer ${JWT}`,
    html: '&quot;adminEmail&quot;:&quot;admin@example.test&quot;,&quot;adminPassword&quot;:&quot;AlsoNotForReports!&quot;',
  };

  const redacted = redactReport(source);
  const serialized = JSON.stringify(redacted);

  assert.match(serialized, /\[REDACTED\]/);
  assert.doesNotMatch(serialized, /Authorization:\s*Bearer/i);
  assert.doesNotMatch(serialized, /eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
  assert.doesNotMatch(serialized, /owner@example\.test|admin@example\.test/);
  assert.doesNotMatch(serialized, /NotForReports|AlsoNotForReports/);
  assert.match(serialized, /23127075/);
  assert.equal(source.environment.values[0].value, JWT);
});

test('runSuites atomically preserves redacted evidence and returns a failing summary after Newman assertion failures', async () => {
  const root = mkdtempSync(join(tmpdir(), 'hw06-runner-'));
  const outputDir = join(root, 'evidence');
  const invoked = [];

  const fakeNewmanRun = (options, callback) => {
    invoked.push(options);
    const id = options.folder[0].slice(0, 5).toLowerCase().replace('fr-', 'fr-');
    const failed = id === 'fr-08' ? 1 : 0;
    const summary = {
      environment: {
        values: [{ key: 'adminToken', value: JWT }],
      },
      run: {
        stats: {
          assertions: { total: 2, failed },
          requests: { total: 1, failed: 0 },
        },
        failures: failed ? [{ error: { message: `Bearer ${JWT}` } }] : [],
      },
    };
    process.stdout.write(`CLI ${options.folder[0]} request assertion Authorization: Bearer ${JWT}\n`);
    process.stderr.write(`CLI ${options.folder[0]} stderr Authorization: Bearer ${JWT}\n`);
    writeFileSync(options.reporter.json.export, JSON.stringify(summary));
    writeFileSync(options.reporter.htmlextra.export, `<html>Authorization: Bearer ${JWT}</html>`);
    queueMicrotask(() => callback(null, summary));
    return { on() { return this; } };
  };

  try {
    const result = await runSuites({
      rootDir: root,
      outputDir,
      newmanRun: fakeNewmanRun,
    });

    assert.equal(invoked.length, 3);
    assert.deepEqual(invoked[0].reporters, ['cli', 'json', 'htmlextra']);
    assert.equal(result.ok, false);
    assert.equal(result.assertions.failed, 1);

    for (const id of ['fr-05', 'fr-08', 'fr-18']) {
      for (const extension of ['json', 'html', 'txt']) {
        const path = join(outputDir, `${id}.${extension}`);
        assert.equal(existsSync(path), true, `${path} should survive a failed run`);
        const evidence = readFileSync(path, 'utf8');
        assert.doesNotMatch(evidence, /Authorization:\s*Bearer/i);
        assert.doesNotMatch(evidence, /eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
        if (extension === 'txt') {
          assert.match(evidence, new RegExp(`CLI FR-${id.slice(3)} - .*request assertion`));
          assert.match(evidence, /CLI .* stderr Authorization: \[REDACTED\]/);
        }
      }
    }

    const persistedSummary = JSON.parse(readFileSync(join(outputDir, 'summary.json'), 'utf8'));
    assert.equal(persistedSummary.ok, false);
    assert.equal(persistedSummary.assertions.failed, 1);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
