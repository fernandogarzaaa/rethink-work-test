# Owning the bots (Task 2.4, under 300 words)

The bots are safety-critical software wearing a friendly face, and I would own them that way.

First, fix the prompts. Three rules are actively harmful: "never say you don't know" (causes hallucinated schedules), "false alarms waste staff time" (causes the two dangerous misses), and the facilitator bot's "solve it yourself" (lets a volunteer hold a suicide disclosure alone). I would rewrite these before any new feature work, because no judge can compensate for a bot instructed not to escalate.

Second, make the evaluation continuous, not a one-off. The judge v2 pipeline becomes a nightly job over that day's exchanges, with URGENT flags paging staff and a weekly sample reviewed against clinician labels to track recall. The failure-modes table becomes the living taxonomy: every new miss gets a row, a sorting rule, and a regression test.

Third, version the knowledge base. The prompt contradicts itself on the refund threshold today. Programme facts move into the data model; the bots read them, never hardcode them.

Finally, keep a human in the loop where it matters. The bots handle content and logistics; anything touching self-harm, coercive control, or medical advice routes to staff. Automation earns trust by knowing its limits, and in mental health the cost of a miss is measured in lives, not tickets.

(248 words)
