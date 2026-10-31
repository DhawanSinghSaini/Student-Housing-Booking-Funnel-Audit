# Student Housing Funnel Audit — AI-assisted SQL + Validation

A reproducible **synthetic-data** showcase built as an application sample for Amber's AI Data Analyst Intern role. It demonstrates the business skill of calculating distinct-lead conversion, checking messy data, using AI to accelerate SQL work, and independently validating a tempting but inaccurate metric.

## Business question
How many unique accommodation inquiries turn into bookings, and how does conversion differ by acquisition channel?

## How to run

```bash
python analyze.py
```

Python standard library only; no installation or keys required. The script deterministically generates `synthetic_events.csv`, processes the events in SQLite, produces `audit_report.json` and `audit_report.md`, and validates metrics with assertions.

## AI assistance and a real validation issue

- **AI assistant used:** ChatGPT (GPT-6) to help scaffold the Python/SQLite analysis and produce test ideas in the conversation where this application sample was prepared.
- **Initial AI-assisted query failure mode:** `SELECT COUNT(*) FROM events WHERE event_type='booking'` counts *booking events*, not *unique booked leads*. Duplicate events therefore inflate the metric. The program explicitly executes this flawed approach and compares it with the correct one. This is an **illustrated query error, not a claim about a production bug or a prior conversation**.
- **Human review needed:** Explain in your own words why a distinct entity key is necessary, run the script locally, and verify the results before claiming authorship and publishing.
- **Correction:** `COUNT(DISTINCT lead_id)` and independent duplicate-group checks; assertion that bookings do not exceed inquiry leads.
- **Limitations:** This is synthetic data with no evidence of actual Amber funnel performance, and no real-time AI calls. It is not an official company case study.

## Reusable prompt/workflow

1. Ask ChatGPT to generate a SQL query for inquiry-to-booking conversion, and clarify the entity grain (`lead_id`) and event grain.
2. Inspect the SQL for double-counting with a duplicate-event test case.
3. Validate by distinct-lead group checks and independent assertions.
4. Summarize the result only after it passes tests.


## Files
- `analyze.py`: dataset generation, SQL metrics and validation
- `synthetic_events.csv`: generated synthetic event log
- `audit_report.json`: machine-readable results
- `audit_report.md`: concise stakeholder summary
- `PROMPTS.md`: AI-assisted workflow and repeatable verification approach

## Attribution
AI assistance was used to draft the sample. Do not submit the project as if it were an independently developed, previously deployed system. Review and extend it yourself before publishing.
