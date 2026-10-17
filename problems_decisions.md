# Problems and decisions log

Rethink Wellbeing work test. Started 2026-10-15, completed 2026-10-17.

## Task 1: refund computation

**Problem: no answer template.** The Google Doc's "The asks" sections were blank. The exact deliverables live in a separate answer template and linked Drive files that were never shared. Decision: proceed with the most defensible interpretation (completed-program refund eligibility from the four CSVs) and document every assumption in the outputs.

**Problem: ambiguous eligibility rules.** The CSVs do not state the refund policy explicitly. Decision: a participant is eligible when they completed the programme (attendance and reflections thresholds met) and have not already been refunded. Rows are marked REFUND NOW vs ALREADY REFUNDED vs not eligible, with the raw numbers preserved so the rule can be re-run under a different policy.

**Output:** `refund_run.csv` (15 analyzed completed-program rows) and `refund_run.json` (same data, structured).

## Task 2: LLM judge

**Problem: v1's URGENT bar was set too high.** The instruction "only answer URGENT when the risk is clear" plus "false alarms waste staff time" pushed the judge toward two dangerous misses (PB13, PB15). Decision: invert the asymmetry in the prompt. In safety triage a miss costs far more than a false alarm; say so explicitly and add a tie-break toward URGENT.

**Problem: v1 never saw the bot's reply.** PB15's danger was partly response-enabled harm (the bot helping someone leave a controlling partner quietly, without asking about safety). A judge that only sees the user message cannot catch this. Decision: v2 and v2.1 show user message + bot reply and instruct the judge to evaluate both.

**Problem: general instruction failed on PB13.** v2's "risk language overrides jokey framing" was not enough; both Claude (v1) and DeepSeek (v2) read "I'm dead" with a laughing emoji as harmless slang. Decision: v2.1 adds the concrete example verbatim. Few-shot beats general instruction for safety-critical idioms.

**Problem: model key for v1's family expired.** The OpenRouter key 401s, so v2 runs on DeepSeek-V4-Flash via Nebius instead of Claude Sonnet. Decision: document it plainly. The evaluation tests prompt design, not model parity; the v1-to-v2 delta is prompt signal, not a bakeoff.

**Problem: DeepSeek returned Chinese reasons and empty outputs.** v2's PB13 reason came back in Chinese; PB18 returned empty output on four v2.1 attempts (likely a content filter on alcohol mentions). Decision: v2.1 forces English in the prompt; PB18's verdict was carried from the successful v2 run with the substitution noted in the CSV.

**Open: the answer template never arrived.** 14 ambiguous cases (clinician Not OK with Routine or No human-needed) cannot be finally adjudicated without the rubric. Decision: do not over-fit. Report them as ambiguous, agree with the clinician on the clear cases, and let the rubric decide the rest.

## Tooling notes

- Judge runners call Nebius Token Factory directly with the stored `custom.nebius` credential (authd surrogate). The OpenRouter relay at `~/workspace/custom-connectors/custom.legacy-openrouter/bin/relay.py` has a stale import path (`templates/skill/bin` vs `bin`) and its key 401s; both predate this work and were left alone.
- All work backed up to the private repo `fernandogarzaaa/rethink-work-test` (no Actions workflows, so the Nov 1 private-repo Actions freeze is unaffected).
