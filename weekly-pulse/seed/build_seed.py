"""Builds the seed documents for the SuperAgent Weekly Pulse database.
Writes one JSON file per document: accounts/<id>.json, weeks/<weekOf>.json, report/current.json.
"""
import json, os, copy

NOW = "2026-09-30T01:51:17Z"
SRC_GMAIL = "Gmail"

accounts = {
 "biogen": dict(order=1, name="Biogen", agent="Project Callisto", persona="Medical Affairs", status="on-track",
   phase="Launch prep", goLive="2026-10-21", goLiveLabel="Oct 21 (access)", goLiveConfirmed=True, owner="Paul Gullo",
   summary="Users get Callisto access on Wednesday, October 21. The AI Foundations training moved up to Friday, October 16, with a launch meeting on October 23 and role-based training the week after.",
   updates=[
     {"date":"2026-09-25","text":"Rahcyne confirmed the ACTO training is the mandatory one; Biogen's other trainings are supplemental. Launch meeting requested for 10/23."},
     {"date":"2026-09-28","text":"Scope set as Callisto Basics (pre-call planning, knowledge retrieval, medical insights, PACE); write-back moves to the Advanced iteration. MSL, MD and FD audiences get two one-hour sessions each."},
     {"date":"2026-09-29","text":"AI Foundations training set for Oct 16, two live 60-minute sessions (10:00 and 2:00 ET), titled “AI Basics for Breakthroughs in Medical Affairs.”"},
     {"date":"2026-09-29","text":"Branded User Guide received from Rahcyne; Field Director training deck built."}],
   nextSteps=["Run-of-show session with Rahcyne (Sep 30)","Draft training content (Oct 1) and review with Nicole (Oct 2)","Callisto weekly sync (Oct 2)"],
   watch="Bilal still owes Biogen accounts and email addresses for the ACTO team, and has to approve the proposal not to record the live sessions. ACTO still needs SharePoint access to upload decks.",
   metrics=[], sources=["Callisto training and launch planning recap (Sep 28)","AI Foundations Training sync with Rahcyne (Sep 29)"]),
 "ipsen": dict(order=2, name="Ipsen", agent="SuperAgent (knowledge retrieval)", persona="Medical Affairs", status="pre",
   phase="Discovery & content", goLive="", goLiveLabel="TBD", owner="Matt Dugan",
   summary="Phase 1 remains knowledge retrieval. The SuperAgent content discovery session with Denise Bentley and Spencer Hess runs Wednesday, September 30.",
   updates=[{"date":"2026-09-30","text":"Content discovery session scheduled for 2:30 PM with Denise Bentley, Spencer Hess and Matt."},
            {"date":"2026-09-24","text":"Matt Dugan took the lead on Ipsen and owns ongoing updates."}],
   nextSteps=["Capture outcomes from the Sep 30 discovery session","Bi-weekly touchpoint (Tue, Oct 6)"],
   watch="", metrics=[], sources=["Google Calendar"]),
 "regeneron": dict(order=3, name="Regeneron", agent="REX (REgeneron access eXpert)", persona="Market Access", status="on-track",
   phase="Launch prep", goLive="2026-10-05", goLiveLabel="", goLiveConfirmed=True, owner="Paul Gullo",
   pilotStart="2026-09-08", pilotEnd="2026-09-18",
   summary="Go-live holds at Monday, October 5, with an automatic deployment to all current users that week. The pilot group voted to name the agent REX, and Betty announced it to about 27 people on Commercial Training.",
   updates=[
     {"date":"2026-09-29","text":"Agent officially named REX. Brand-team emails with the REX User Guide and Prompting Guide go out Oct 2 and Oct 9."},
     {"date":"2026-09-29","text":"Success measures agreed: adoption, time back, accuracy and sentiment (eNPS). Surveys run after use rather than as a pre-launch baseline, 2–3 questions, with pulses at +2 and +6 weeks."},
     {"date":"2026-09-28","text":"Betty sent a cross-analysis of Market Access assets REX can't pull from yet; new folders being added for field compliance, PSS resources and Dupixent."}],
   nextSteps=["Finish review of the MA asset cross-analysis","Stand up new CMS folders before Oct 5","Deploy to all users week of Oct 5"],
   watch="One pilot user expected payer-policy content, which REX doesn't cover. Set that expectation at rollout; Policy Reporter API raised as a future option. Our success-measures deck still shows Oct 15 and needs correcting.",
   metrics=[{"label":"Pilot reps","value":"12"},{"label":"Pilot questions","value":"209"},{"label":"Routing accuracy","value":"99.3%"},{"label":"Pilot survey avg","value":"4.33/5"}],
   sources=["Introducing REX (Sep 29)","Zoom summary: Defining Success Metrics (Sep 29)"]),
 "corcept": dict(order=4, name="Corcept Therapeutics", agent="Harvi", persona="Sales", status="watch",
   phase="Pilot / UAT", goLive="2026-10-08", goLiveLabel="", goLiveConfirmed=False, owner="Paul Gullo",
   pilotStart="2026-09-28", pilotEnd="2026-10-02",
   summary="The one-week pilot launched to 11 Corcept users on September 28. A new summary-recall feature ships October 7 and isn't retroactive, so Matt proposed a readiness review on October 15 and a go-live based on that review. Jordan hasn't replied yet.",
   updates=[
     {"date":"2026-09-28","text":"Jordan launched the pilot to 11 users; all confirmed with access. Loreli added Sep 29."},
     {"date":"2026-09-28","text":"Four success measures agreed: adoption, time back, coaching quality and user confidence. Coaching quality is the priority, judged by VP Sales Tom Burke and the ASDs. Readouts at 2 weeks, 30 and 60 days."},
     {"date":"2026-09-29","text":"Matt proposed a revised plan: time survey Oct 2, rubric approved Oct 8, summary workflow validated by Oct 13, joint readiness review Oct 15."},
     {"date":"2026-09-29","text":"Jordan asked for a Harvi quick-start guide."}],
   nextSteps=["Get Jordan's answer on the revised date plan","Approve survey wording (Oct 1)","Corcept to confirm licensed NTM and RM counts (Oct 2)","Adapt the Harvi quick-start guide"],
   watch="Go-live will likely move to late October if Corcept accepts Matt's plan. FCR use is still limited to Jordan, Katie and Liz.",
   metrics=[{"label":"Pilot users","value":"11"},{"label":"Success measures","value":"4"}],
   sources=["ACTO Harvi – FCR Date Alignment (Sep 29)","Corcept / Harvi – Success Metrics Alignment (Sep 28)"]),
 "praxis": dict(order=5, name="Praxis Medicines", agent="Prax (Voice FCR)", persona="Sales", status="on-track",
   phase="Build", goLive="2026-10-12", goLiveLabel="Week of Oct 12", goLiveConfirmed=False, owner="Paul Gullo",
   pilotStart="2026-10-05", pilotEnd="2026-10-09",
   summary="Targeting the week of October 12, still awaiting confirmation. We proposed a pilot the week of October 5 and haven't heard back. FCRs are being rebranded as coaching touchpoints, and touchpoints now run daily at 11 AM.",
   updates=[
     {"date":"2026-09-24","text":"User cleanup under way; SCORM duplicate-registration hotfix coming. Julie preparing an executive pre-read and demo for the second week of October."},
     {"date":"2026-09-25","text":"Pilot proposed for the week of Oct 5; no reply yet."},
     {"date":"2026-09-28","text":"Julie shared the Praxis/ACTO project tracker; daily 11 AM touchpoints started."}],
   nextSteps=["Get Michael, Christena and Kevin to confirm the pilot group and dates","Confirm the week-of-Oct-12 go-live"],
   watch="", metrics=[], sources=["Praxis SuperAgent: Go-Live Timing and Pilot (Sep 25)","Otter: Praxis + ACTO Touchpoint (Sep 24)"]),
 "philips": dict(order=6, name="Philips Respironics", agent="LAICA", persona="Sales", status="live",
   phase="Live — optimize", goLive="", goLiveLabel="Live", track="Relaunch content refresh", owner="Ali Rizvi",
   summary="Live. LAICA wasn't surfacing the Ramp Plus Discussion Paper; Matt moved reference assets between skills and Dave Glowark confirmed the fix on September 29. Marketing and training are now working together on relaunch content.",
   updates=[{"date":"2026-09-29","text":"Ramp Plus Discussion Paper retrieval fixed and confirmed by Dave Glowark."},
            {"date":"2026-09-28","text":"Marketers and training team collaborating on relaunch content."}],
   nextSteps=["Weekly touchpoint (Thu, Oct 1)","Reconfigure the agent as new relaunch content lands"],
   watch="Cumulative feedback since launch is 62% negative (73 of 118 rated), mostly unanswered questions. Content refresh should bring it down; Kumar suggested a Salesforce CRM connector to keep content current.",
   metrics=[{"label":"Avg DAU (Sep 16–22)","value":"1.2"},{"label":"Sessions","value":"7"},{"label":"Avg response","value":"12.6s"}],
   sources=["LAICA will not produce the Ramp Plus Discussion Paper (Sep 28–29)"]),
 "azurity": dict(order=7, name="Azurity (Currax)", agent="LAICA", persona="Sales", status="live",
   phase="Live — optimize", goLive="", goLiveLabel="Live", track="Cross-brand expansion scoping", owner="Toni Abraham",
   summary="Live and stable. Currax is moving over to Azurity with new content; cross-brand expansion scoping continues, roughly 60–65 days to launch with Contrave as the first content focus.",
   updates=[{"date":"2026-09-28","text":"Confirmed Currax will move over to Azurity with new content."}],
   nextSteps=["Paul / Toni SuperAgents sync (Thu, Oct 1)","Set up the connector call Kumar offered"],
   watch="", metrics=[], sources=["Weekly report reply thread (Sep 28)"]),
 "mineralys": dict(order=8, name="Mineralys", agent="SuperAgents (TBD)", persona="New / scoping", status="pre",
   phase="Platform onboarding", goLive="", goLiveLabel="TBD", owner="Paul Gullo",
   summary="New account. Paul and Ryan met Katie Potteiger and Michael Hayes on September 23 to collect job descriptions as inputs for their SuperAgents, and Paul has admin access to the Mineralys ACTO instance.",
   updates=[{"date":"2026-09-23","text":"Kickoff on SuperAgent inputs (job descriptions)."},{"date":"2026-09-24","text":"Admin access granted to the Mineralys ACTO instance."}],
   nextSteps=["Review SuperAgent functionality with ~8 Mineralys stakeholders (Thu, Oct 1)"],
   watch="", metrics=[], sources=["JDs for Acto Superagent (Sep 23)","Google Calendar"]),
}
for a in accounts.values(): a["updatedAt"] = NOW

def lite(a, **over):
    keep = {k: a[k] for k in ("name","agent","persona","status","phase","goLive","goLiveLabel","goLiveConfirmed","order","summary") if k in a}
    keep.update(over); return keep

A = accounts
weeks = {
 "2026-09-07": {"asOf":"2026-09-11","headline":"Biogen's September 8 go-live did not happen after a Salesforce patch issue on Biogen's side; the new target is the week of September 28. Corcept confirmed October 1, Praxis's pilot is underway, and Regeneron's pilot is live.","accounts":{
   "biogen": lite(A["biogen"], status="at-risk", phase="Build", goLive="2026-09-28", goLiveLabel="Week of Sep 28", summary="Sept 8 go-live missed after a Salesforce Winter '26 patch issue affecting iPad/Veeva login."),
   "ipsen": lite(A["ipsen"], phase="Platform onboarding", summary="Targeting Q4; overview call Sept 16."),
   "regeneron": lite(A["regeneron"], agent="SuperAgent Implementation", goLive="2026-09-21", phase="Pilot / UAT", summary="Pilot live, closing content gaps."),
   "corcept": lite(A["corcept"], status="on-track", goLive="2026-10-01", goLiveConfirmed=True, phase="Pilot / UAT", summary="Go-live confirmed for October 1, off September 16."),
   "praxis": lite(A["praxis"], goLive="2026-09-23", goLiveLabel="", phase="Pilot / UAT", summary="Pilot underway Sept 9–18, FCR testing live."),
   "philips": lite(A["philips"], summary="Live and stable."),
   "azurity": lite(A["azurity"], summary="Live and stable.")}},
 "2026-09-14": {"asOf":"2026-09-18","headline":"Biogen asked that its medical team complete AI-literacy training before Callisto goes live. Regeneron's pilot finished with 99.3% routing accuracy, Corcept holds October 1, and Praxis targets October 12.","accounts":{
   "biogen": lite(A["biogen"], goLive="", goLiveLabel="Late October", phase="Build", summary="AI-literacy training underway with Mark and team ahead of go-live."),
   "ipsen": lite(A["ipsen"], phase="Discovery & content", summary="Phase 1 scope agreed: knowledge retrieval, 3 TAs."),
   "regeneron": lite(A["regeneron"], agent="SuperAgent Implementation", goLive="2026-09-28", goLiveLabel="~Sep 28", phase="Pilot / UAT", summary="Pilot complete with 99.3% routing accuracy."),
   "corcept": lite(A["corcept"], status="on-track", goLive="2026-10-01", goLiveConfirmed=True, phase="Pilot / UAT", summary="UAT fixes continuing, no serious blockers."),
   "praxis": lite(A["praxis"], goLive="2026-10-12", goLiveLabel="Oct 12", phase="Build", summary="Slight contract-side delay; MVP build continues."),
   "philips": lite(A["philips"], summary="Live and stable; new content workflow agreed."),
   "azurity": lite(A["azurity"], summary="Live and stable; cross-brand expansion kicked off.")}},
 "2026-09-21": {"asOf":"2026-09-25","headline":"Biogen has a firm October 21 go-live. Regeneron moved one week to October 5 to finish its content audit, Corcept starts a one-week pilot September 28 ahead of an expected October 8 go-live, and Praxis targets the week of October 12.","accounts":{
   "biogen": lite(A["biogen"], goLiveLabel="Oct 21 (firm)", summary="Firm go-live October 21, with AI foundation training the week of Oct 19, then persona training."),
   "ipsen": lite(A["ipsen"], summary="Preparing CMS content for the knowledge base; Matt Dugan leading."),
   "regeneron": lite(A["regeneron"], agent="SuperAgent Implementation", summary="Moved one week to October 5 to finish content audit and testing."),
   "corcept": lite(A["corcept"], status="on-track", goLiveLabel="~Oct 8", goLiveConfirmed=True, summary="One-week pilot starts September 28; go-live expected ~October 8."),
   "praxis": lite(A["praxis"], summary="FCRs working; very strong client feedback. Awaiting go-live confirmation."),
   "philips": lite(A["philips"], summary="Live; team aligned on next steps for new content."),
   "azurity": lite(A["azurity"], summary="Live and stable; cross-brand scoping in progress.")}},
}
for wk, w in weeks.items():
    for k, a in w["accounts"].items():
        a.setdefault("pilotStart", ""); a.setdefault("pilotEnd", "")
    w["accounts"]["corcept"].update(pilotStart="2026-09-28", pilotEnd="2026-10-02") if wk=="2026-09-21" else None

headline = ("Regeneron holds its Monday, October 5 go-live, with the agent now named REX and launch emails going to the field. "
  "Corcept's pilot is running with 11 users, but a summary-recall feature shipping October 7 has Matt proposing a later go-live, and Jordan hasn't replied yet. "
  "Biogen's AI Foundations training moved up to October 16 ahead of October 21 access, Praxis still needs to confirm its pilot group and launch week, and Mineralys joins the portfolio.")
highlights = [
  "Regeneron: REX name announced; success measures agreed (adoption, time back, accuracy, eNPS)",
  "Corcept: pilot live with 11 users; go-live of Oct 8 now in question",
  "Biogen: AI Foundations training Oct 16, launch meeting Oct 23",
  "Philips: Ramp Plus retrieval fix confirmed by the client",
  "New account: Mineralys, functionality review Oct 1",
]
report = {"weekOf":"2026-09-28","lastSync":NOW,"nextSync":"Wed, Sep 30 · 7:48 AM ET","headline":headline,"highlights":highlights,
          "sources":"Gmail, Google Calendar, Google Drive, Zoom/Gong/Otter summaries"}
# current week's archive entry mirrors the live state
weeks["2026-09-28"] = {"asOf":"2026-10-02","headline":headline,"highlights":highlights,
    "accounts":{k: copy.deepcopy(v) for k,v in accounts.items()}}

def dump(coll, doc, data):
    os.makedirs(coll, exist_ok=True)
    with open(f"{coll}/{doc}.json","w") as f: json.dump(data, f, indent=1, ensure_ascii=False)
for k,v in accounts.items(): dump("accounts", k, v)
for k,v in weeks.items(): dump("weeks", k, v)
dump("report", "current", report)
print("ok", len(accounts), len(weeks))
