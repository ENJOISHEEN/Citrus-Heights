# Daily huddle board — automated run

Inputs each morning (all via the Microsoft 365 connector):
1. SharePoint file `Bridge Stack Ranking_MM.DD.YY.xlsx` in Stack Ranking/October 2026 (data date = the date in the filename).
2. Outlook email from michael.paras@bridgelocations.com, subject `NPS M/D/YYYY` (same data date; arrives the night before the file).

Steps:
1. `sharepoint_search` query "Bridge Stack Ranking_<MM.DD.YY>" → read_resource on the file URI. The result is too large, so the tool saves it to a file; use that path as `dump.txt`. (Only the daily sheets come through; month-to-date sheets are cut off — that is why state.json is kept and advanced one day at a time.)
2. `outlook_email_search` sender Michael Paras, query "NPS <M/D/YYYY>" → read_resource on the message → saved to a file; use as `nps.txt`.
3. `cd tools && python3 board.py update state.json dump.txt nps.txt <YYYY-MM-DD data date>` — refuses if the date is a repeat or skips a day.
4. `python3 build_board.py state.json <publish date> out.html` (publish date = today).
5. Check: div depth 0, rep RGU total vs store RGU (script prints a note if they differ), page loads at 390px/768px without sideways scroll.
6. Publish: trial mode writes `trial/index.html`; live mode writes `index.html`. Commit as Claude <noreply@anthropic.com> and push to main. state.json is committed with it.
7. Re-sync: whenever a full workbook is attached to a chat, run `python3 board.py seed <xlsx> state.json <nps.txt>` to replace the running totals with the exact month-to-date numbers (fixes drift from chargebacks/corrections; also picks up a changed RGU target).
8. Drift (known): the daily sheets carry no RGU targets and no corrections, so `update` leaves targets stale and rep totals can drift by a few RGUs (found 10/14: Sunrise target 720 vs 711, other stores' targets, and Daisy/Albert/Jayme/Kevin off by 1-2). Store totals for Sunrise were exact. The connector cannot read the MTD tabs, so the fix is a re-sync: paste the Store-MTD and Employee-MTD rows (no header, tab-separated) into two files and run `python3 board.py resync state.json store.tsv emp.tsv`, then rebuild. Automated runs should end with a line telling the owner targets/rep totals are unverified until the next re-sync; do this weekly or whenever the plan target changes.
