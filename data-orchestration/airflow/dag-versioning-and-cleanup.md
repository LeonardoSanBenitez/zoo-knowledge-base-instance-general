<!--kb
id: airflow-dag-versioning-and-cleanup
labels: area:core, area:serialization, area:API, kind:bug, topic:dag-versioning, version:3.x
triggers: our version table has tens of thousands of rows and keeps growing; why does every re-parse create a new version of the same pipeline; the cleanup command ran but did not delete what I expected; a scheduled pipeline is filling the database with serialized copies of itself;
          dag version keeps increasing, DAG Versioning, dag_version, version_number,
          serialized_dag, source_code_hash, dag_version_id, min_serialized_dag_update_interval,
          airflow db clean, clean-before-timestamp, ForeignKeyViolation,
          "Encountered error when attempting to clean table", "not cleaned due to errors",
          _airflow_deleted__dag_version, skip_if_referenced, keep_last, dag_code,
          dag_version_inflation_check_level, RUNTIME_VARYING_VALUE, AIR304,
          "runtime-variable values in Dag construction"
verified: 2026-08-08 @3.3.0 + 3.2.2 images and tag 3.3.0 sources, via
          .claude/memory/lucas/communities/airflow/tickets/i58310/ (7 scripts, 8 logs).
          2026-08-08 revision CORRECTED the source_code_hash discriminator, which was stated
          backwards here and in a public comment; see "The diagnostic that does NOT separate them".
-->

# DAG versioning: why version counts explode, and what `db clean` can do about it

Airflow 3 creates a row in `dag_version` (plus `serialized_dag` and `dag_code`) as DAGs are
re-parsed. Deployments report counts in the tens of thousands — 54k versions against 74k runs in
one case — and the resulting tables become an operational problem. This entry covers what actually
drives the count and what cleanup can and cannot remove.

**Every fact below was run, not recalled**, in `apache/airflow:3.3.0` and `apache/airflow:3.2.2`;
source citations are at tag `3.3.0`. This matters because the released packages differ from `main`
(e.g. `main` has `SerializedDAG.to_dict`, 3.3.0 has `DagSerialization.to_dict`) — cite the tag.

## The rule that decides whether a new version is created

`SerializedDagModel.write_dag`, `airflow-core/src/airflow/models/serialized_dag.py:600-770`:

1. If `min_update_interval` has not elapsed since the last write → **return immediately**, before
   the hash is even computed. The real parse path passes
   `[core] min_serialized_dag_update_interval` (default **30 s**) here
   (`dag_processing/collection.py:281-289`), so parses inside that window never write at all.
2. Compute the hash of the serialized DAG. Unchanged → no new version.
3. Changed, **and the latest version has no task instances** → the existing row is **overwritten in
   place** (direct `UPDATE` of `_data`, `_data_compressed`, `dag_hash`). *No new version.*
4. Changed, **and the latest version has task instances** → a new `DagVersion` is created, because
   overwriting would rewrite history under a run that already executed.

So **the version counter measures "how often the serialization changed *while the previous version
was already in use*"**, not how often it changed. This is the mechanism behind the widely-reported
and long-unexplained asymmetry: *parse, parse, parse* does not bump the version, but *trigger a
run, parse* does.

Introduced by #46934 ("Optimize DAG versioning for dynamic DAGs"), released in **3.0.0**, so it
applies to every 3.x deployment. #60937 (3.2.0) made the task-instance check an `EXISTS` rather
than loading every TI, after it caused DAG-processor OOMs.

Measured on 3.3.0 (`version_bump_mechanism.log`): five consecutive parses of a DAG carrying a
`uuid4()` in a template field left `version_number` at 1 **while the stored hash changed each
time**; after a task instance was attached, every further parse added exactly one version. An
unchanging DAG moved nothing, before or after a run.

## Two distinct root causes, one symptom

Reports of "versions keep increasing" split into two families, and the usual advice only fits one:

**(A) Non-deterministic DAG content.** `uuid4()`, `datetime.now()` and similar evaluated at parse
time, landing in a template field. Every parse genuinely differs. Fix is in the DAG file.

**(B) Divergent parsers alternating between two stable serializations.** Two DAG processors with
different code produce different output and ping-pong: with more than one processor and a busy DAG,
growth is roughly one version per parse and unbounded, because the hash comparison is only ever
against the *latest* version. Observed causes: one processor running an older provider build (so
`template_fields` differed by one entry), and rolling redeploys where old and new pods coexist
(20-70 versions from a single redeploy of an otherwise static DAG). **The DAG file is not the
problem and editing it will not help.**

**The diagnostic that does NOT separate them — corrected 2026-08-08, having previously been stated
here (and posted publicly) the wrong way round.** Comparing `dag_code.source_code_hash` across
consecutive versions is cheap and worth doing, but it does not identify the family:

- `source_code_hash` is the hash of **the DAG file's text read off disk** (`models/dagcode.py:68`;
  written by `DagCode.write_code` → `get_code_from_file`, `:88-94`);
- a file containing `uuid.uuid4()` **does not change its text between parses**, so family (A)
  produces an identical code hash with a differing `dag_hash` — exactly the signature previously
  attributed to family (B) alone.

Measured on `apache/airflow:3.3.0` (5 versions of a `uuid4()` DAG: 1 distinct `source_code_hash`,
5 distinct `dag_hash`; control with a genuinely edited file: 5 distinct `source_code_hash`).

So the correct reading is:

- code hash **changes** → someone edited the DAG file; version growth is explained and benign;
- code hash **identical** while `serialized_dag.data` differs → family (A) *or* (B), undecided.

**What does separate them** is Airflow's own documented step: diff the `serialized_dag` payload
between two consecutive versions and see which field moved
(`airflow-core/docs/faq.rst`, `faq:dag-version-inflation`, first released 3.3.0). A field traceable
to the DAG file is (A); one that is not — e.g. `template_fields` differing by an entry — is (B).

Useful corollary: a query for "many versions sharing one `source_code_hash`" is a **better**
inflation alarm than the static checker, because it observes the outcome rather than the syntax and
therefore also catches values produced by helper functions, which the checker cannot see at all
(see below).

## What `airflow db clean` can remove

Config: `airflow-core/src/airflow/utils/db_cleanup.py:216-229` — recency column `created_at`,
`keep_last=True` grouped by `dag_id`, `dependent_tables=["task_instance", "dag_run"]`,
`skip_if_referenced=[("task_instance", "dag_version_id")]`. Present since **3.0.0** (#44389).

Measured behaviour, both images, `--clean-before-timestamp <horizon> --skip-archive --yes`:

| scenario | 3.3.0 | 3.2.2 |
|---|---|---|
| versions whose task instances are **also** past the horizon | one pass takes `dag_version` 6 → 1 and `serialized_dag` 6 → 1, exit 0 | **identical** — the fix is never exercised |
| versions past the horizon whose task instances are **current** | `Found 0 rows meeting deletion criteria`, exit 0, rows skipped cleanly | `Found 5 rows…` → `Encountered error when attempting to clean table 'dag_version'` → `The following tables were not cleaned due to errors: ['dag_version']`, **exit code 0** |

Four operationally important consequences:

1. **One pass is enough.** `task_instance` is cleaned earlier in the same run than `dag_version`
   (order of `config_list`), so versions freed by that deletion are removed in the same command.
2. **The newest version per DAG always survives** (`keep_last` by `dag_id`) — the table floors at
   one row per DAG.
3. **The binding constraint is the `task_instance` retention window**, not anything about versions.
   `task_instance.dag_version_id` is `ON DELETE RESTRICT` (`models/taskinstance.py:619-621`; it
   became RESTRICT in 3.1.0 via migration `0072_3_1_0_change_ti_dag_version_fk_to_restrict`), so a
   pinned version is skipped, silently and correctly.
4. **Pre-3.3, the failure is silent: `exit code: 0`.** It is a warning, so a nightly cron job
   reports success while `dag_version` never shrinks — the most likely explanation when someone
   says "we have cleanup configured and still have 54k rows". Fixed by #68339 (`skip_if_referenced`,
   **3.3.0**); the trail of duplicates before it: #56192, #59474, #61390, #63703, #66177. On MySQL
   the same delete is reported to hang on metadata locks (#66177) — *not reproduced here*, SQLite
   raises and the error is caught.

Note that a row count before and after **cannot** distinguish 3.2 from 3.3 in the pinned case —
both leave the rows in place. Only the log line does.

## Related: many versions and API-server memory

**Start here, because Airflow documents this chain itself:** FAQ *"How to prevent API server memory
growth"* (`faq:api-server-memory-growth`, added #65036, first released **3.3.0**) states that the
api-server keeps deserialized DAG objects in memory **keyed by DAG version id**, and cross-references
the version-inflation entry. Two levers, and the *defaults* are what decide whether advice about
them is useful (read from `git show 3.3.0:…/config_templates/config.yml`, not from the FAQ prose):

| option | default @3.3.0 | added | note |
|---|---|---|---|
| `[api] dag_cache_size` | **64** | 3.3.0 | LRU keyed by DAG version id; `0` = unbounded, the pre-3.2 behaviour |
| `[api] dag_cache_ttl` | 3600 | 3.3.0 | staleness: may serve the previous version until expiry |
| `[api] server_type` | **uvicorn** | 3.2.0 | rolling worker recycling works **only** under `gunicorn` |
| `[api] worker_refresh_interval` | **0** (off) | 3.2.0 | ignored with uvicorn (SIGTTOU kills newest, not oldest) |

So on 3.3 the DAG cache is already bounded unless the deployment set it to `0`, while worker
recycling — the lever the FAQ leads with — is off by default. Telling a 3.3 reporter to "bound the
cache" is advice to fix something already fixed; the recycling one is the live suggestion.

Reported: opening an older DagRun in the UI OOMs api-server pods on a DAG with 54k versions. The
intuitive explanation — "the grid endpoint loads every version" — is **wrong at 3.3.0**:
`api_fastapi/core_api/routes/ui/grid.py:200-232` bounds historical serialized DAGs to those
referenced by task instances of the runs *on the current page*, streams with `yield_per=5`, merges
each and `expunge()`s it. The endpoint has been memory-hardened deliberately.

Unverified hypothesis worth testing before repeating: `_merge_node_dicts` accumulates the *union*
of node structures across versions, so with heavily parameterised DAGs whose task ids differ per
version, the merged structure could grow with the number of distinct task sets rather than the page
size. Open threads on this endpoint: PR #69832 (holds a pooled DB connection across deserialization
for DAGs with many versions) and #65712 (metadata-DB contention). #64877 is adjacent — api-server
hangs when viewing a task absent from the latest DAG code — but a different trigger.

## Traps for whoever answers one of these tickets

- **Do not tell a family-(B) reporter to clean up their DAG file.** Ask for the `serialized_dag`
  payload diff between consecutive versions — *not* the `source_code_hash` comparison, which cannot
  tell the families apart (see above). Two of the four reporters seen so far are family (B) and were
  given family-(A) advice.
- **The static checker (`[dag_processor] dag_version_inflation_check_level`, default `warning` since
  3.2) sees through no function call at all**, so its silence is not evidence of family (B).
  Verified on 3.3.0: `x = uuid.uuid4()` then `x` in a task argument warns; `x = build_id()` does not
  — same file or imported, plain function or class method, and not even when the helper is what
  builds the task. It parses one file with `ast` and resolves a name only against assignments whose
  right-hand side it already recognises. Reporters hit this: the pattern most likely to survive code
  review is precisely a tidy helper function.
- **ruff's `AIR304` (`airflow3-dag-dynamic-value`) is not a substitute** for catching this at review
  time: absent from ruff 0.14.4, a **preview** rule in 0.16.2 (so `--select AIR304` selects nothing
  without `--preview`), and strictly weaker than Airflow's own checker — it flags only the inline
  `uuid.uuid4()` case and misses `x = uuid.uuid4()` used one line later. Airflow's FAQ recommends it,
  but that paragraph is on `main` and not yet on the published stable page.
- **Do not assert that pre-3.3 `db clean` "fails"** without saying *when*: in the common case where
  the pinning task instances are themselves being cleaned, 3.2.2 behaves identically to 3.3.0.
- **The changelog tells you what changed in the code, not whether it changes anything for the
  user's scenario.** Both of the above were wrong in a first draft and were caught only by running
  the scenario on both images.
