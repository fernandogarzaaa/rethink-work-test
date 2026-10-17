# Data model (Task 1.3)

Replaces the Airtable + Sheets + Forms + Stripe patchwork with one schema. Derived from the four exports.

## Entities

**Participant**
- id (e.g. RW26-018, primary key)
- full_name, preferred_name, email (unique), country, timezone
- cohort (e.g. 2026 Summer), group_id (FK to Group)
- application_status: Applied | In Facilitation Round | Accepted | Withdrawn | Rejected
- sharing_consent: boolean
- staff_notes: text

**Group**
- id (e.g. Group 84, primary key)
- cohort, facilitator_id (FK to Facilitator)
- meeting_time_utc (the exports assume 18:00 UTC for most groups; store it per group instead of in a prompt)

**Facilitator**
- id, name, email (unique)
- trained: boolean

**Payment**
- id (Stripe id or WISE-xxx for manual, primary key)
- participant_id (FK), amount, currency, fee
- type: Motivational Deposit | Voluntary Contribution
- deposit_amount_due: 200 | 50 (50 for lower-income countries)
- deposit_status: Pending | Received | Refunded | Partially Refunded
- amount_refunded, channel: Stripe | Wise (manual)
- created_utc

**Attendance**
- participant_id (FK), session_week (1-8, 12)
- present: 1 | 0.5 (partial) | 0
- recorded_by (facilitator_id), recorded_at
- Unique constraint on (participant_id, session_week)

**WeeklyReflection**
- participant_id (FK), week_number (1-9)
- responses: JSONB (the GAD-7/PHQ-style items plus session feedback)
- submitted_at
- Unique constraint on (participant_id, week_number)

**WellbeingTracker**
- participant_id (FK), tracker: Week1 | Week12
- completed: boolean, completed_at
- Not in the exports; needed for the refund rule, so it is a first-class entity here rather than an assumption.

## Refund rule as a query

A participant's deposit is refundable when:
- SUM(attendance.present) >= 8 across the 9 sessions, AND
- COUNT(weekly_reflections) = 9, AND
- both wellbeing trackers completed, AND
- deposit_status != Refunded.

The voluntary contribution is never refunded. Refunds go out within two weeks of the week-12 reunion; the Payment row records amount_refunded and channel.

## Notes

- Email is the join key across all four exports today; the model replaces it with participant_id and keeps email as a unique attribute.
- The attendance export's wide format (one column per session week) becomes one row per participant per session, which is what makes the 0.5 partial-attendance rule computable.
- Manual Wise entries are Payments with channel = Wise (manual), same as Stripe rows, so the refund run covers both.
- The bot prompt's knowledge base currently hardcodes "most groups meet at 18:00 UTC" and contradicts itself on the session threshold (8 vs 7). Both values move into Group.meeting_time_utc and a single programme-policy record, so the bots read them instead of guessing.
