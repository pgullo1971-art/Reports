# SuperAgent Weekly Pulse — refresh playbook

The live report is https://claude.ai/artifact/Er6twyU8BNyrVDXjq711AZ. The page stores no data in its HTML.
Everything it shows comes from its artifact database. A scheduled routine refreshes that database
every day at 5:00 PM ET, following the steps below. Anyone can run the same steps by hand.

## Data model

| Doc | What it holds |
| --- | --- |
| `report/current` | `weekOf` (the Monday, `YYYY-MM-DD`), `lastSync` (ISO), `nextSync` (display text), `headline` (3–4 sentences), `highlights` (3–6 short strings), `sources` |
| `accounts/<slug>` | One per account: `name, agent, persona, status, phase, goLive, goLiveLabel, goLiveConfirmed, pilotStart, pilotEnd, summary, updates[{date,text}], nextSteps[], metrics[{label,value}], owner, track, sources[], order, updatedAt` |
| `weeks/<weekOf>` | The archived week: `asOf` (that week's Friday), `headline`, `highlights`, and `accounts` (a map of slug → full account object) |

- `status` is one of `live`, `on-track`, `watch`, `at-risk`, `pre`.
- `persona` is one of `Medical Affairs`, `Market Access`, `Sales`, or a free label such as `New / scoping`.
- Dates are `YYYY-MM-DD`. Use `""` when there is no date.

## What the page computes on its own

You don't write these fields. The page derives them from the data:

- KPIs
- countdowns
- "Launch in N days"
- "Date passed"
- "Slipped Nd" (vs the previous week's archive)
- "N date changes" (from the week history)
- "Date unconfirmed" (when `goLiveConfirmed` is `false` and the date is 21 days out or less)
- "No update N days" (from `updatedAt`)
- "Pilot running"
- the "Changed since last week" list
- the runway

So keep the data factual and current, and the analysis follows.

## Refresh steps

1. **Read the current state.** Read `report/current`, list `accounts`, and list `weeks`. Note each document's `version`.
2. **Research since `lastSync`.** This step is read-only: never send, draft, label or modify anything.
   - **Gmail**: search each account name and its key contacts. Also search meeting-summary senders: `from:do-not-reply@gong.io`, `from:no-reply@otter.ai`, `from:no-reply@zoom.us`, and Staircase.
   - **Google Calendar**: this week and next.
   - **Google Drive**: files modified since `lastSync`.
   - **Ignore** calendar "hypercare ends" placeholders. They were created from old launch dates.
3. **Start a new week if needed.** If the current Monday (ET) is after `report.weekOf`:
   - Make sure `weeks/<old weekOf>` holds the final state from before this refresh.
   - Set `report.weekOf` to the new Monday.
4. **Update each account that has news.**
   - `updates`: this week's items only, as `{date, text}`, at most 5. Drop items older than the report week.
   - Refresh `summary` and `nextSteps`. Never write watch items (leave `watch` empty).
   - Change `goLive` or `status` only on evidence. Set `goLiveConfirmed: false` when the client hasn't confirmed.
   - Add 1–3 `sources` (email subject + date, or file title).
   - Set `updatedAt` to now.
   - Leave accounts with no news untouched, so their staleness signal works.
   - Add a new account as `accounts/<slug>` with the next `order`.
5. **Rewrite the report summary.** Write `report.headline` in Paul's voice: warm, direct, factual, 3–4 sentences, leading with the biggest move. Refresh `highlights`, and set `lastSync` and `nextSync`.
6. **Archive this week.** Mirror the current state into `weeks/<weekOf>`: `asOf` = this week's Friday, the same headline and highlights, and the full accounts map.
7. **Write it in one batch.** Use a single ArtifactData `batch`, pinning every existing document with `if_version`. If a pin fails, re-read that document and redo only that write.
8. **Report back** in 3–5 lines: what changed, and anything that looked uncertain.

## Excluded accounts

- **Praxis Medicines** removed SuperAgents from its portfolio on Oct 1, 2026, and was taken out of the report. Don't re-add it.

## Guardrails

- Only write facts found in sources. Mark anything uncertain with "unconfirmed" in the text.
- Don't invent metrics.
- Never remove an account unless the sources show the engagement ended. In that case, mention it in the headline.
