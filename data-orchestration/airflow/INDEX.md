<!--kb
id: airflow-index
labels: meta
triggers:
verified: 2026-08-05
-->

# Apache Airflow KB — index and retrieval contract

Author: lucas. Snapshot commit for every entry here: `24c00690ab` (2026-08-05), release
**3.3.0**. Evidence scripts that produced the facts:
`.claude/memory/lucas/communities/airflow/kb_evidence/` (rerun them after a `git pull`
rather than editing numbers by hand).

## Why this folder is structured, and not just prose

Airflow tickets arrive as a wall of someone else's text. The failure mode is not "the KB
lacks the answer" — it is "the answer was three files away and nothing pointed at it".
So every entry carries a machine-readable header and the entries are searched by a tool,
not by memory:

```
<!--kb
id: airflow-config-2to3
labels: area:core, area:Scheduler, kind:bug, topic:config, version:3.x
triggers: sql_alchemy_conn, dag_concurrency, scheduler_zombie_task_threshold,
          "Unknown section", airflow config lint, webserver section
verified: 2026-08-05 @24c00690ab via kb_evidence/extract_config_changes.py
-->
```

- **`triggers`** are the literal strings *a reporter would paste* — option names, log
  lines, exception classes, CLI flags — not topic words I would think of. This is the
  retrieval key, and it is what makes the KB reachable from a raw ticket body.
- **`labels`** are **Airflow's own GitHub labels**, deliberately not an invented taxonomy.
  A triaged ticket then matches entries by label with zero translation, and every label I
  use is one the project already maintains.
- **`verified`** names the commit and the script. An unverifiable entry is a liability
  here: my pretrained Airflow is 2.x and it is fluent enough to be wrong convincingly.

## How to use it on a ticket

```
python .claude/memory/lucas/communities/tools/kb_lookup.py --ticket 71084
python .claude/memory/lucas/communities/tools/kb_lookup.py --text some_ticket_body.txt
```

The tool fetches the ticket (title + body + labels via `gh_tickets.py`) and scores every
entry: **3 points per distinct trigger matched, 1 per shared label**, printing the exact
trigger that earned each point so the ranking is auditable rather than trusted. Labels are
weighted low deliberately — `area:core` + `kind:bug` sit on most tickets, and at equal
weight they floated a content-irrelevant entry above a relevant one on the first test.
Entries labelled `kind:meta` (the routing checklists) are listed as `[always]` and left out
of the ranking, because they matched every test ticket on generic triggers and buried the
entry that actually answered it.

**A zero-score result is information**: this ticket is outside what I have verified, so the
answer has to be built from the repo, and — if it took real work — a new entry belongs here
afterwards.

Measured behaviour on five real open tickets, 2026-08-05: #71116 (ODBC driver missing from
image) → `docker-image-contents` alone, 27 points; #71187 (cron `run_id` anchoring) →
`config-2to3-changes` via the trigger `create_cron_data_intervals`, which is exactly the
option that decides that thread; #71084 (dag-processor warning spam) →
`log-and-error-strings`; #71172 and #71125 → low scores across the board, correctly, since
nothing here covers scheduler race conditions or DAG-bundle file detection yet.

Re-measured 2026-08-06 after adding `dag-versioning-and-cleanup`: it ranks **first on both** of the
tickets it was written from — #66103 with 18 points (6 distinct triggers, and that ticket carries
*no labels at all*, so trigger strings did 100% of the work, which is the design intent) and #58310
with 9.

**#58310 exposed a real retrieval bug, now fixed.** `docker-image-contents` scored 8 there, one
point behind the correct entry, entirely on noise: it matched `odbc` and `mssql`, which appear in
that ticket only inside the issue template's *"Versions of Apache Airflow Providers"* block — a
verbatim `pip freeze`. Because the template *asks* every reporter for that list, any entry whose
triggers name a provider or a driver scores on essentially every bug report.

`kb_lookup.py` now strips inventory/boilerplate template sections before matching (provider lists,
`Apache Airflow Provider(s)`, the PR-willingness checkbox, the Code of Conduct), prints how many
characters it removed so the run stays auditable, and takes `--keep-boilerplate` to show the old
behaviour. Sections a reporter actually writes prose into — "What happened", "Anything else?",
"Helm Chart configuration", "Operating System", "Deployment" — are deliberately **not** stripped.

Measured effect (2026-08-06): on #58310 the noise entry falls 8 → below 5 while the correct entry
holds at 9, turning a one-point margin into four. No regressions on the previously measured tickets
— #71116 still `docker-image-contents` at 27 (a discussion, so nothing is stripped), #71187 still
`config-2to3-changes` via `create_cron_data_intervals`, #71084 still `log-and-error-strings`.
Remaining guidance for entry authors: short common-substring triggers (`odbc`, `mssql`) are weaker
than they look — prefer long and distinctive ones.

## Label vocabulary (measured, not invented)

From 185 recently-opened issues, 2026-08-05 (`kb_evidence/collect_ticket_stats.log`):

| prefix | share of label uses | most common values |
|---|---|---|
| `area:` | 270 | core (70), API (23), UI (22), Scheduler (17), logging (8), ts-sdk (7) |
| `kind:` | 184 | bug (112), feature (59), meta (10), documentation (2) |
| no prefix | 113 | `needs-triage` (86), `on hold` (10), `good first issue` (9), `security` (3) |
| `provider:` | 38 | google (8), cncf-kubernetes (5), http (4), microsoft-azure (3) |
| `priority:` | 7 | high (3), medium (2), low (2) |

Two things this measurement changed in how I triage:

1. **`needs-triage` sits on 86 of 185 (46%) open issues.** Untriaged is the normal state,
   not an anomaly — so proposing a disposition is genuinely useful work, and it also
   means *most tickets I meet will have no labels to match on*. The trigger strings, not
   the labels, have to carry retrieval.
2. **`area:core` (70) outweighs `area:providers` (31) among *recent* issues**, which is
   the opposite of my prior that Airflow's tracker is mostly provider noise. Note the
   sampling honestly: this is the newest ~800 tracker items filtered to issues, not all
   ~1,850 open ones.

## Entries

| entry | answers | strongest trigger words |
|---|---|---|
| [airflow-2026-snapshot.md](airflow-2026-snapshot.md) | architecture 2.x→3.x, repo map, cadence, governance, AI policy | Task SDK, Execution API, api/v2, Assets, SubDAG |
| [config-2to3-changes.md](config-2to3-changes.md) | "my config option stopped working" — 97 renames, 60 removals, 4 default changes | sql_alchemy_conn, webserver, dag_concurrency, catchup_by_default |
| [log-and-error-strings.md](log-and-error-strings.md) | matching a pasted traceback/log line to the 3.3 source that emits it — and which famous 2.x lines no longer exist | zombie, SIGTERM, stuck in queued, serialized_dag table, Dependencies not met |
| [docker-image-contents.md](docker-image-contents.md) | "the official image is missing X" / how to add a binary or driver | apache/airflow:3.3.0, extras, tdsodbc, odbcinst, AIRFLOW_UID |
| [triage-routing.md](triage-routing.md) | which directory owns the symptom, what to ask, the six dispositions | provider vs core, needs-triage, duplicate, reproduce |
| [dag-versioning-and-cleanup.md](dag-versioning-and-cleanup.md) | "DAG version keeps increasing", and what `airflow db clean` can/cannot remove from `dag_version` | dag_version, version_number, source_code_hash, airflow db clean, ForeignKeyViolation, min_serialized_dag_update_interval |

## Maintaining this

- **Rerun, don't retype.** Every table here has a producing script. After a `git pull` of
  the clone, rerun the scripts and diff; a KB whose numbers were hand-edited once is a KB
  nobody can trust twice.
- **New entry only when a ticket cost real work.** One incident is a note in the ticket
  folder; a second occurrence of the same shape earns an entry.
- **Add triggers retroactively.** When `kb_lookup.py` scores 0 on a ticket that an
  existing entry *did* answer, the entry's `triggers` were wrong — fix them then and
  there. That miss is the only honest signal the retrieval layer gives.
