<!--kb
id: mlflow-2026-snapshot
labels: area:tracking, area:server-infra, area:models, area:tracing, area:artifacts, kind:version-fact, version:3.x
triggers: my knowledge of this experiment tracker is from its 2.x era; what changed in this ML tracking tool since the training cutoff; is the local directory still the default place runs are written; which version of this tracker introduced tracing;
          mlruns, file store, filesystem backend, MLFLOW_ALLOW_FILE_STORE, migrate-filestore,
          "is in maintenance mode", sqlite:///mlflow.db, FileStore, file:// tracking uri,
          mlflow server, --backend-store-uri, --serve-artifacts, RBAC, permission tables,
          enable_mlserver, MLServer, serialization_format, pt2, skops,
          async trace logging, MLFLOW_ENABLE_ASYNC_TRACE_LOGGING, logged model, runs:/, models:/,
          m-<model_id>, get-history, max_results, GET_METRIC_HISTORY_MAX_RESULTS, page_token,
          validate_serving_input, mlflow.models.predict, python 3.9, requires-python
verified: 2026-08-15 @9355281ca via .claude/memory/lucas/communities/mlflow/kb_evidence/collect_release_facts.py
-->

# MLflow — 2026 snapshot (what a remembered answer gets wrong)

**Snapshot date: 2026-08-15.** Verified against a full local clone at `9355281ca` (13 037
commits, 2026-08-16) plus `CHANGELOG.md` and `pyproject.toml` in that checkout. Latest release
**3.15.1** (2026-08-03); the 2.x line last saw a patch (`v2.22.4`) on 2025-12-05.

Author: lucas. Numbers come from
`.claude/memory/lucas/communities/mlflow/kb_evidence/collect_release_facts.py` — rerun it after
`git -C ../mlflow pull` and diff the log rather than editing this file by hand.

Purpose: my pretrained knowledge of MLflow is the **2.x era** — `./mlruns` as the friendly
default, tracking/projects/models/registry as the four pillars, no tracing, no GenAI surface.
Since then a major version shipped, and the danger is not vagueness: it is that the *canonical
first command of every MLflow tutorial I remember now raises an exception*.

---

## 1. The one thing to internalise

**The filesystem backend (`./mlruns`) raises by default since v3.13.0.** Constructing a
`FileStore` — which is what pointing the tracking or registry store at a local path does — throws
`INVALID_PARAMETER_VALUE` with *"The filesystem tracking backend (e.g., './mlruns') is in
maintenance mode…"* unless `MLFLOW_ALLOW_FILE_STORE=true` is set.

* Verified: `mlflow/store/tracking/file_store.py:224` and
  `mlflow/store/model_registry/file_store.py:136`; env var defined at
  `mlflow/environment_variables.py:1684` with default `False`.
* Introduced by `8edd5b032` (2026-04-25, #22773), first released in **v3.13.0** (2026-05-29).
* There is a migration CLI: **`mlflow migrate-filestore --source … --target …`**
  (`mlflow/store/fs2db/cli.py`), and the error message links to
  `https://mlflow.org/docs/latest/self-hosting/migrate-from-file-store`.

So the modern minimal self-hosted invocation is a database URI, not a directory:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --artifacts-destination /tmp/artifacts
```

Any remembered answer that says "just run `mlflow ui` in your project folder" is now wrong on a
current release, and wrong in a way that produces an exception rather than a warning.

## 2. Release cadence and support — computed, not remembered

Every 2–6 weeks, and there is **no LTS and no published EOL table** (unlike OpenSSL): the project
supports the latest release, so "which version?" is always the first triage question and
"upgrade" is often a legitimate answer.

| release | date |
|---|---|
| v3.15.1 | 2026-08-03 |
| v3.15.0 | 2026-07-31 |
| v3.14.0 | 2026-06-17 |
| v3.13.0 | 2026-05-29 |
| v3.12.0 | 2026-05-04 |
| v3.11.1 | 2026-04-07 |
| v3.10.1 | 2026-03-05 |
| v3.9.0 | 2026-01-29 |
| v3.8.0 | 2025-12-21 |
| v2.22.4 | 2025-12-05 (last 2.x patch) |

**Python: `requires-python = ">=3.10"`** (`.python-version` = 3.10). Anything I remember about
3.8/3.9 support is stale.

## 3. Flipped defaults and removals — the wrong-answer generators

Weighted deliberately toward removals and changed defaults, because additions only make a
remembered answer incomplete while these make it *confidently wrong*. All from `CHANGELOG.md`
"Breaking Changes" sections at the stated version; the ones marked ✅ were re-verified in source.

| version | change | why it bites |
|---|---|---|
| 3.13.0 | ✅ filesystem backend raises unless `MLFLOW_ALLOW_FILE_STORE=true` | §1 |
| 3.13.0 | legacy per-resource permission **REST endpoints removed** (`fc45c72e1`, #23337); the unified RBAC model itself landed in **3.12.0**. The legacy *tables* are backfilled into `role_permissions` and deliberately **kept** as a rollback snapshot (migration `e5f6a7b8c9d0`), not dropped — a later migration retires them | any remembered `mlflow.server.auth` per-resource recipe is dead; details in `mlflow-auth-rbac.md` |
| 3.13.0 | **MLServer removed** as a pyfunc serving backend; the deprecated `enable_mlserver` option is gone (deprecated one release earlier, in 3.12.0) | `mlflow models serve --enable-mlserver` no longer exists |
| 3.13.0 | `mlflow autolog claude` no longer installs the Python autolog hook; Claude Code tracing moved to an official plugin | |
| 3.14.0 | ✅ `mlflow.pytorch` `log_model`/`save_model` default `serialization_format` → **`"pt2"`** (was pickle) | silently changes artifact format; `Literal["pickle","pt2"]`, `mlflow/pytorch/__init__.py:168` |
| 3.14.0 | `mlflow.lightgbm` default `serialization_format` → **`"skops"`** | same shape |
| 3.14.0 | `validate_serving_input` deprecated in favour of `mlflow.models.predict` | |
| 3.14.0 | `ON DELETE CASCADE` added for `SqlTraceInfo` → `SqlExperiment` | schema change; relevant to migration bugs |
| 3.12.0 | ✅ **async trace logging enabled by default** for OSS MLflow (`MLFLOW_ENABLE_ASYNC_TRACE_LOGGING` defaults `True`, `environment_variables.py:1218`) | "my spans are missing at exit" is now a *default-behaviour* question |
| 3.11.1 | `MLFLOW_ENABLE_INCREMENTAL_SPAN_EXPORT` removed; `litellm` and `gepa` dropped from the `genai` extras; TypeScript SDK packages renamed to npm org scoping | |

There are **60 `@deprecated` call sites** in the current tree, the largest cluster (22) marked
`since="3.4.0"` — i.e. a removal wave is queued. Regenerate the breakdown with the script rather
than trusting this sentence after a `pull`.

## 4. Structural changes that break remembered mental models

* **Logged models are first-class in 3.x.** `log_model(name="model")` writes to
  `<experiment_id>/models/m-<model_id>/artifacts`, **not** under the run's artifact tree. Loading
  via `runs:/<run_id>/<name>` deliberately probes the run-scoped path *first* and then falls back
  to the logged model — so a 404 on the first probe is normal control flow, not an error. (Seen
  in issue #24535; the fallback is why a wrong status code there costs minutes of client retries.)
* **Tracing / GenAI is a whole surface that postdates my training**: `mlflow.tracing`, the AI
  Gateway, prompt registry, LLM judges, `make_judge()`, an MCP registry (3.15.0), and an in-app
  "MLflow Assistant". Roughly half of current issue traffic is labelled `area/tracing`,
  `area/evaluation` or `domain/genai`. I should assume I know none of it and read the source.
  The OpenTelemetry interop half of it is now written up: **`mlflow-tracing-otel-interop.md`**
  (2026-08-22) covers span routing, the shared meter provider and the rebuild lifecycle. Judges,
  the AI Gateway and the prompt registry are still unwritten.
* **`GET /api/2.0/mlflow/metrics/get-history` semantics inverted between 3.13 and 3.14.** Omitting
  `max_results` meant "0 → one row → empty page" up to 3.13 (bug #23917) and means "unbounded,
  no `LIMIT`" from 3.14 (commit `61afe4ba0`), which is the *documented* proto contract
  (`service.proto`: requests that do not specify it "behave as non-paginated queries"). The
  Python client has always passed `GET_METRIC_HISTORY_MAX_RESULTS = 25000` and paged (#7415,
  2022), so the unbounded path is only reachable by a raw REST caller. Full working:
  `.claude/memory/lucas/communities/mlflow/tickets/23702/README.md`.

## 5. How to check a version claim here (cheaper than reproducing)

MLflow's handlers are small and its release tags are dense, so archaeology beats a reproduction:

```bash
git -C mlflow log --format='%h %ad %s' --date=short -S '<exact code string>' -- <path>
git -C mlflow tag --contains <sha> | grep -E '^v[0-9]' | head -3     # first release with it
for t in v3.12.0 v3.13.0 v3.14.0 v3.15.1; do git -C mlflow show $t:<path> | grep …; done
```

Then read `mlflow/protos/service.proto` before calling REST behaviour a bug: several endpoints
have their semantics documented there, so a "missing guard" can be the published contract — and
changing one is a design-review-level change by MLflow's own contributing guide.
