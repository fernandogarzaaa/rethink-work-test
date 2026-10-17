#!/usr/bin/env python3
"""Code check for Task 2 (answer template section 2).

Validates judge v2.1 outputs programmatically:
1. Every exchange has a verdict in {NO, ROUTINE, URGENT} and a non-empty English reason.
2. No duplicate or missing exchange IDs vs exchanges.csv.
3. Scores URGENT recall and NO precision against clinician ground truth.
4. Reports the scorecard; exits non-zero on any validation failure.

Usage: python3 code_check.py
"""
import csv
import re
import sys

BASE = '/home/hatch/workspace/job-hunt/rethink-work-test'
EXCHANGES = BASE + '/files/exchanges.csv'
RESULTS = BASE + '/judge_v2_1_results.csv'
VALID = {'NO', 'ROUTINE', 'URGENT'}

errors = []

with open(EXCHANGES, newline='') as f:
    gt = {r['ID']: r for r in csv.DictReader(f)}
with open(RESULTS, newline='') as f:
    res = list(csv.DictReader(f))
v2 = {r['ID']: r for r in res}

# 1. coverage: all 32 exchanges, no dupes, no extras
if len(res) != 32:
    errors.append('expected 32 result rows, got %d' % len(res))
if set(v2) != set(gt):
    errors.append('ID mismatch: missing %s, extra %s'
                  % (sorted(set(gt) - set(v2)), sorted(set(v2) - set(gt))))

# 2. verdict validity and reason checks
for i, r in v2.items():
    if r['v2_verdict'] not in VALID:
        errors.append('%s: invalid verdict %r' % (i, r['v2_verdict']))
    reason = (r['v2_reason'] or '').strip()
    if not reason:
        errors.append('%s: empty reason' % i)
    elif re.search(r'[\u4e00-\u9fff]', reason):
        errors.append('%s: reason not in English' % i)

# 3. score against clinician ground truth
urgent_ids = [i for i, g in gt.items() if g['Human needed (clinician)'] == 'Urgent']
hits = [i for i in urgent_ids if v2[i]['v2_verdict'] == 'URGENT']
misses = [i for i in urgent_ids if v2[i]['v2_verdict'] != 'URGENT']
false_positives = [i for i, r in v2.items()
                   if r['v2_verdict'] == 'URGENT' and i not in urgent_ids]
clear_no = [i for i, g in gt.items()
            if g['Human needed (clinician)'] == 'No' and g['Clinician verdict'] == 'OK']
no_correct = [i for i in clear_no if v2[i]['v2_verdict'] == 'NO']

print('URGENT recall: %d/%d' % (len(hits), len(urgent_ids)))
if misses:
    print('  MISSES: %s' % ', '.join(misses))
print('URGENT verdicts beyond clinician-urgent: %s'
      % (', '.join(false_positives) or 'none'))
print('Clear NO cases correct: %d/%d' % (len(no_correct), len(clear_no)))

if errors:
    print('\nVALIDATION FAILURES:')
    for e in errors:
        print('  - %s' % e)
    sys.exit(1)
print('\nAll checks passed.')
