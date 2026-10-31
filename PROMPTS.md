# Prompt and verification log

## Business task
Calculate the percentage of unique student-housing inquiry leads who book and compare acquisition channels. Use a synthetic event dataset; preserve the difference between entity grain (`lead_id`) and event grain (multiple records per lead).

## AI-assisted draft SQL to audit

```sql
SELECT COUNT(*) AS booked FROM events WHERE event_type = 'booking';
```

**Problem:** This counts every booking event, including duplicate event replays. It is not an accurate count of unique booked leads.

## Revised validated SQL

```sql
SELECT COUNT(DISTINCT lead_id) AS booked_leads
FROM events
WHERE event_type = 'booking';
```

## Validation method

1. Verify that `COUNT(DISTINCT lead_id)` never exceeds distinct inquiry leads.
2. Group booking events by lead ID and identify repeated booking events.
3. Compare independent Python row counts to SQLite event counts.
4. Reject negative weekly values.
5. Disclose that all records are synthetic and all conversion figures are examples, not company facts.

## Disclosure
The flawed SQL above is intentionally kept as a **demonstrable AI query failure mode** for a data verification example. It is not evidence that an actual AI tool unexpectedly made this mistake during a pre-existing project. The project and this log were drafted with ChatGPT assistance for this application exercise.
