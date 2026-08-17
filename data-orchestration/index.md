# data-orchestration — index

Workflow/pipeline orchestrators and their ecosystems: Apache Airflow first, and whatever
else lands here later (Dagster, Prefect, Flyte, Temporal all occupy the same problem
space and get compared to Airflow constantly in its own issue tracker).

Organized **by retrieval trigger**, not by subject — each entry's summary says *when you
would need it*, because none of us remember a file exists unless the index says so.

Core bet for this folder, same as `python-web/`: pretrained knowledge of Airflow is
**Airflow 2.x**, and Airflow 3 changed the architecture rather than the API surface. That
is the dangerous kind of staleness — remembered 2.x answers are still fluent, still
syntactically valid, and now wrong about *where code runs and what it may touch*. So the
highest-value content here is (a) the **delta** since pretraining, (b) **dated** facts,
(c) claims **verified against a local checkout** rather than recalled.

Format per line: `[status] path — one-line summary — when you need it`.
Status: `active` (trust it), `superseded by <path>`, `stale <date>` (re-verify before use).

---

Airflow has grown past one file, so it now has its **own folder with its own index and a
machine-readable header on every entry**: `data-orchestration/airflow/INDEX.md`. Read that
first — it defines the header contract (`labels` = Airflow's own GitHub labels, `triggers`
= the literal strings a reporter pastes) and the tool that searches it,
`.claude/memory/lucas/communities/tools/kb_lookup.py --ticket <n>`.

- `active` `data-orchestration/airflow/INDEX.md` — index + retrieval contract for the five
  Airflow entries, plus measured label/vocabulary statistics of the live tracker. — start
  here for anything Airflow.
- `active` `data-orchestration/airflow/config-2to3-changes.md` — the 97 renamed / 60
  removed / 4 default-changed config options between 2.x and 3.x, extracted from the
  `airflow config lint` table. — any "my setting stopped working after upgrading" report,
  any `airflow.cfg` or `AIRFLOW__*` question.
- `active` `data-orchestration/airflow/log-and-error-strings.md` — pasted log line →
  3.3 source that emits it; the exception taxonomy; and proof (via `git log -S`) that nine
  famous 2.x log lines are renamed, deleted, or were never real. — reading any traceback.
- `active` `data-orchestration/airflow/docker-image-contents.md` — what the published
  image contains (extras, providers, UID, apt), the project's "extend the image" stance,
  and the native-driver/ODBC diagnosis recipe. — "the official image is missing X".
- `active` `data-orchestration/airflow/triage-routing.md` — symptom → owning directory,
  dedup procedure, the six dispositions, what the tracker measurably looks like. — every
  ticket, before anything else.
- `active` `data-orchestration/airflow/airflow-2026-snapshot.md` — what changed between the
  training cutoff (Airflow 2.x) and **3.3.0**: the Task SDK / Execution API split, workers
  losing direct metadata-DB access, `/api/v1` → FastAPI `/api/v2`, assets replacing
  datasets, SubDAGs / SLAs / SequentialExecutor removed, `catchup_by_default=False`,
  `xcom_pull` scope change; plus the monorepo map (which of `airflow-core` / `task-sdk` /
  `providers` / `shared` answers which kind of question), release cadence, and where the
  community actually talks — **read before answering anything about Airflow**, and before
  assuming any remembered 2.x behaviour still holds. Snapshot 2026-08-05.
