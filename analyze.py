"""Student housing booking funnel audit (synthetic data) with reproducible SQL checks."""
import csv
import json
import random
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
random.seed(20261031)


def make_data():
    rows = []
    cities = ['Pune', 'London', 'Manchester', 'Birmingham']
    channels = ['organic', 'paid', 'referral', 'social']
    for i in range(1, 501):
        lead = f'L{i:04d}'
        city = cities[(i * 7) % len(cities)]
        channel = channels[(i * 13 + i // 7) % len(channels)]
        # Each lead has one inquiry; only some progress to booking.
        booked = i % 5 not in (0, 1)
        rows.append((lead, 'inquiry', city, channel, 0))
        if booked:
            value = 210 + 17 * (i % 13)
            rows.append((lead, 'booking', city, channel, value))
            # Simulate duplicate booking events from an accidental event replay.
            if i % 29 == 0:
                rows.append((lead, 'booking', city, channel, value))
    with (ROOT / 'synthetic_events.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['lead_id', 'event_type', 'city', 'channel', 'weekly_value_gbp'])
        writer.writerows(rows)
    return rows


def main():
    rows = make_data()
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE events (lead_id TEXT, event_type TEXT, city TEXT, channel TEXT, weekly_value_gbp INTEGER)')
    conn.executemany('INSERT INTO events VALUES (?,?,?,?,?)', rows)
    flawed = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='booking'").fetchone()[0]
    corrected = conn.execute("SELECT COUNT(DISTINCT lead_id) FROM events WHERE event_type='booking'").fetchone()[0]
    leads = conn.execute("SELECT COUNT(DISTINCT lead_id) FROM events WHERE event_type='inquiry'").fetchone()[0]
    assert flawed > corrected, 'Demo should contain duplicates to test bad query'
    assert corrected <= leads
    assert len(rows) == conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    assert conn.execute('SELECT COUNT(*) FROM events WHERE weekly_value_gbp < 0').fetchone()[0] == 0
    duplicate_groups = conn.execute('''
      SELECT COUNT(*) FROM (
        SELECT lead_id FROM events WHERE event_type='booking' GROUP BY lead_id HAVING COUNT(*) > 1
      )
    ''').fetchone()[0]
    channel_data = conn.execute('''
      WITH distinct_leads AS (
        SELECT lead_id, MAX(channel) AS channel, MAX(CASE WHEN event_type='booking' THEN 1 ELSE 0 END) AS booked
        FROM events GROUP BY lead_id
      )
      SELECT channel, COUNT(*) AS inquiries, SUM(booked) AS bookings,
             ROUND(100.0 * SUM(booked)/COUNT(*), 2) AS conversion_pct
      FROM distinct_leads GROUP BY channel ORDER BY conversion_pct DESC, channel
    ''').fetchall()
    report = {
      'dataset': 'Synthetic demonstrator; NOT actual Amber operational data',
      'inquiry_leads': leads,
      'flawed_ai_draft_row_count': flawed,
      'correct_distinct_booking_leads': corrected,
      'overcount_if_unvalidated': flawed-corrected,
      'conversion_pct': round(100 * corrected/leads, 2),
      'duplicate_booking_lead_groups': duplicate_groups,
      'by_channel': [dict(channel=c, inquiries=n, bookings=b, conversion_pct=p) for c,n,b,p in channel_data],
      'validation_checks': ['uniqueness of lead in conversion denominator', 'booking count <= inquiries', 'nonnegative value', 'independent Python vs SQLite event row counts']
    }
    (ROOT / 'audit_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (ROOT / 'audit_report.md').write_text(
        '# AI-assisted Booking Funnel Audit — Synthetic Demonstration\n\n'
        '> Synthetic sample dataset; this is NOT Amber company data.\n\n'
        f"**Inquiry leads:** {leads}  \n**Correct unique booked leads:** {corrected}  \n"
        f"**Conversion:** {report['conversion_pct']}%  \n"
        f"**Incorrect booking event count:** {flawed}  \n"
        f"**Duplicate-event overcount caught:** {flawed-corrected}  \n\n"
        '## Channel conversion\n\n| Channel | Inquiries | Booked | Conversion |\n|---|---:|---:|---:|\n'+
        ''.join(f'| {r["channel"]} | {r["inquiries"]} | {r["bookings"]} | {r["conversion_pct"]}% |\n' for r in report['by_channel'])+
        '\n## Verification\nThe first AI-assisted SQL draft (`COUNT(*)` of booking events) can overstate bookings when events are duplicated. '
        'The validated metric is `COUNT(DISTINCT lead_id)`; a separate group-based duplicate check and assertions back it up.\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    conn.close()


if __name__ == '__main__':
    main()
