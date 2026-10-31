# AI-assisted Booking Funnel Audit — Synthetic Demonstration

> Synthetic sample dataset; this is NOT Amber company data.

**Inquiry leads:** 500  
**Correct unique booked leads:** 300  
**Conversion:** 60.0%  
**Incorrect booking event count:** 311  
**Duplicate-event overcount caught:** 11  

## Channel conversion

| Channel | Inquiries | Booked | Conversion |
|---|---:|---:|---:|
| organic | 142 | 86 | 60.56% |
| referral | 143 | 86 | 60.14% |
| social | 72 | 43 | 59.72% |
| paid | 143 | 85 | 59.44% |

## Verification
The first AI-assisted SQL draft (`COUNT(*)` of booking events) can overstate bookings when events are duplicated. The validated metric is `COUNT(DISTINCT lead_id)`; a separate group-based duplicate check and assertions back it up.
