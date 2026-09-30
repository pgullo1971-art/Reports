# Reports

## SuperAgent Weekly Pulse (`weekly-pulse/`)

This is a self-updating version of the weekly *SuperAgent Implementation Status Report*.

- **Live page:** https://claude.ai/artifact/Er6twyU8BNyrVDXjq711AZ
- **`index.html`:** the page source. It reads everything from the artifact's shared database.
- **`UPDATE_PLAYBOOK.md`:** how the database is refreshed. A scheduled routine runs it Mon/Wed/Fri at 7:48 AM ET using Gmail, Calendar and Drive.
- **`seed/`:** `build_seed.py` builds the initial documents: the week of Sep 28, 2026, plus archives of the Sep 7, 14 and 21 reports.

### What the page does on its own

- **KPIs and countdowns** are computed from go-live dates, relative to today.
- **Needs attention** flags come from the data: date slips vs last week, repeat slips across weeks, unconfirmed dates close to launch, passed dates, launch week, watch/at-risk status, and accounts with no update in 9+ days.
- **Changed since last week** is an automatic diff against the prior week's archive.
- **The go-live runway** shows today, pilot windows, and last week's date wherever a date moved.
- **The week picker** replays any archived week, with its flags computed as of that week.
- **Ask Claude** has presets: draft the weekly email, top risks, a 3-bullet exec summary, and what we need from clients. It also takes free-form questions.
- **Copy plain-text summary** builds the summary from the data without using Claude.
