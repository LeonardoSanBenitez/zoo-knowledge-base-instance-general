<!--kb
id: airflow-triage-routing
labels: kind:meta, topic:triage, needs-triage
triggers: needs-triage, duplicate, reproduce, good first issue, pending response,
          which component, provider or core, area:core, area:providers, scheduler, dag processor,
          task sdk, execution api, helm chart, ts-sdk, java-sdk, airflowctl, breeze,
          dag not appearing, mapped task, dynamic task mapping, backfill, xcom, timetable,
          logical_date, run_id, deferrable, triggerer, remote logging
verified: 2026-08-05 @24c00690ab; path existence checked by kb_evidence/collect_repo_facts.py
-->

# Routing an Airflow ticket to the code that owns it

Being confidently wrong here is easy and expensive: a provider bug answered as a core bug
wastes the reporter's time and is visible to everyone. This entry is the checklist.

## Step 0 — establish *which artifact's* version

Airflow releases at least six independently versioned things: **core** (3.3.0),
**each of 105 provider distributions**, the **helm chart** (1.22.0), **airflow-ctl**,
the **task SDK**, and the language SDKs (go/java/ts). "I'm on 3.3" answers almost nothing
when the failing code is `providers/google`. Ask for: core version, the relevant provider
version, deployment method (helm/docker-compose/pip/managed), and executor.

## Step 1 — route by symptom

| The reporter says… | Owner | Path |
|---|---|---|
| names a vendor (AWS/GCP/Azure/Databricks/Snowflake/K8s…) | that provider, **own release cadence — the fix may already be shipped** | `providers/<name>/` (grouped: `apache/*`, `common/*`, `microsoft/*`, `cncf/*`) |
| DAG doesn't show up / stale after edit / import error | DAG processor | `airflow-core/src/airflow/dag_processing/{manager,processor}.py`, `importers/python_importer.py` |
| task stays queued/scheduled, run not created, backfill | scheduler | `airflow-core/src/airflow/jobs/scheduler_job_runner.py` |
| wrong `logical_date` / `data_interval` / cron behaviour | timetables | `airflow-core/src/airflow/timetables/` — check `create_cron_data_intervals` first |
| `/api/v2` response, UI data wrong | core API | `airflow-core/src/airflow/api_fastapi/core_api/` |
| worker can't talk to the API server, JWT/401 in task logs | execution API | `airflow-core/src/airflow/api_fastapi/execution_api/` |
| what a DAG author writes (operators, decorators, context, XCom API) | Task SDK | `task-sdk/src/airflow/sdk/definitions/`, `bases/operator.py` |
| task startup, heartbeats, timeouts, task killed | Task SDK runtime | `task-sdk/src/airflow/sdk/execution_time/{supervisor,task_runner}.py` |
| DB state, migration failure, `alembic` | models/migrations | `airflow-core/src/airflow/models/`, `migrations/versions/` |
| k8s deployment, values.yaml, ingress | helm chart | `chart/` (separate version) |
| serialization, timezone, secrets masking | shared code | `shared/` (symlinked into several distributions — a bug here looks like it spans core and SDK) |
| CLI | core CLI vs `airflowctl` | `airflow-core/src/airflow/cli/` vs `airflow-ctl/` |

**The single most common category error**: answering a 3.x question with 2.x
architecture, e.g. suggesting task code open a DB `Session`. Blocked by design in 3.x.

## Step 2 — dedup, always, immediately before drafting

The tracker moves in hours; on 2026-08-05 a same-day PR invalidated two of four
candidates. Minimum sweep:

```
python communities/tools/gh_tickets.py --repo apache/airflow search "<distinctive phrase>"
git -C airflow log -S "<identifier>" --all --oneline   # has this string ever existed?
```

`git log -S` over the full clone is the highest-value command here and the reason the
clone is not blob-filtered. It answers "was this removed deliberately", "which PR
introduced it", and "does this symbol exist at all" — see `log-and-error-strings.md`,
where it proved that nine remembered log lines were renamed, deleted, or invented.

## Step 3 — pick exactly one disposition

Magpie's six classes (`apache/magpie`, adopted by the project):
`BUG`, `FEATURE-REQUEST`, `NEEDS-INFO`, `DUPLICATE`, `INVALID`, `ALREADY-FIXED`.
Exactly one — a two-class proposal stalls the thread.

Two Airflow-specific dispositions on top:

- **Convert issue → discussion.** Documented and *valued* in `ISSUE_TRIAGE_PROCESS.rst`
  when there are no clear reproduction steps or it's really a support question. I can't
  perform the conversion; recommending it with a reason is legitimate.
- **Not a bug, it's a documented 3.x behaviour change.** Check `config-2to3-changes.md`
  and `upgrading_to_airflow3.rst` before agreeing anything is broken. Airflow is old and
  huge; a surprising behaviour usually has an AIP behind it.

## What the tracker actually looks like (measured 2026-08-05)

185 recently-opened issues, `kb_evidence/collect_ticket_stats.log`:

- `needs-triage` on **86 (46%)** — untriaged is the default state.
- `kind:bug` 112 vs `kind:feature` 59 — roughly 2:1.
- `area:core` 70 ≫ `area:providers` 31; `area:API` 23, `area:UI` 22, `area:Scheduler` 17.
- Only **9** `good first issue` and **7** with any `priority:` label — priority is barely
  used, so "no priority label" carries no information.
- Recurring title vocabulary: dag/task (41), api (15), scheduler (14), sdk (12), mapped (9),
  log (9), xcom (7), typescript (6), backfill (4), deferrable (4), `create_cron_data_intervals` (3),
  opentelemetry (3), windows (3).

Read that last list as *where the community's pain is right now*: dynamic task mapping,
logging, the new TS/Java SDKs, and cron data intervals. A ticket in those areas is more
likely to have a sibling already open — dedup harder there.

## Security, before calling anything a vulnerability

Read `airflow-core/docs/security/security_model.rst`, chapter "What is NOT considered a
security vulnerability". DAG-processor/Triggerer DB access is a **documented known
limitation**. DAG authors are trusted by design — "a DAG can run arbitrary code" is not a
finding. Real vulnerabilities go to `security@apache.org`, never a public issue.
