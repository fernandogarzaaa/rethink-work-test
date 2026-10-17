#!/usr/bin/env python3
"""Run judge v2 over the 32 exchanges and write results to judge_v2_results.csv.

Calls Nebius Token Factory directly (custom.nebius credential via authd surrogate).
Model: deepseek-ai/DeepSeek-V4-Flash-0731. (v1 used Claude Sonnet 5.5 via a key
that is now 401ing; the v2 evaluation tests prompt design, not model parity.)
"""
import csv
import json
import sys
import time
import urllib.request

sys.path.insert(0, '/opt/muse/skills/custom-connector-setup/bin')
from dynamic_credentials import add_surrogate_to_request, read_json_response

PROMPT_PATH = '/home/hatch/workspace/job-hunt/rethink-work-test/judge_v2.txt'
CSV_PATH = '/home/hatch/workspace/job-hunt/rethink-work-test/files/exchanges.csv'
OUT_PATH = '/home/hatch/workspace/job-hunt/rethink-work-test/judge_v2_results.csv'
MODEL = 'deepseek-ai/DeepSeek-V4-Flash-0731'
HOST = 'api.tokenfactory.nebius.com'
URL = 'https://%s/v1/chat/completions' % HOST


def judge(prompt_template, user_message, bot_reply):
    prompt = prompt_template.replace('{user_message}', user_message or '').replace(
        '{bot_reply}', bot_reply or '')
    body = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 300,
        'temperature': 0,
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST')
    add_surrogate_to_request(req, 'custom.nebius', allowed_hosts=[HOST])
    resp = urllib.request.urlopen(req, timeout=180)
    data = read_json_response(resp)
    text = data['choices'][0]['message']['content'].strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    return json.loads(text)


def main():
    with open(PROMPT_PATH) as f:
        template = f.read()
    with open(CSV_PATH, newline='') as f:
        rows = list(csv.DictReader(f))

    print('model %s, %d exchanges' % (MODEL, len(rows)), flush=True)
    results = []
    for r in rows:
        try:
            out = judge(template, r['User message'], r['Bot reply'])
            verdict = out.get('verdict', 'ERROR')
            reason = out.get('reason', '')
        except Exception as e:
            verdict, reason = 'ERROR', 'parse/model failure: %s' % str(e)[:200]
        results.append({'ID': r['ID'], 'v2_verdict': verdict,
                        'v2_reason': reason})
        print('%s -> %s' % (r['ID'], verdict), flush=True)
        time.sleep(2)

    with open(OUT_PATH, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['ID', 'v2_verdict', 'v2_reason'])
        w.writeheader()
        w.writerows(results)
    print('wrote %s' % OUT_PATH)


if __name__ == '__main__':
    main()
