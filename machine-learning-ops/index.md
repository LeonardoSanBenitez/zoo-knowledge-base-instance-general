# machine-learning-ops — index

The ML lifecycle tooling layer: experiment tracking, model registries, artifact stores,
serving plumbing, and the auth that guards them. **MLflow first**; anything that occupies the
same problem space (Weights & Biases, Kubeflow, ZenML, Metaflow, DVC, BentoML) lands here when
a real task needs it, not before.

Organized **by retrieval trigger**, not by subject — each line says *when you would need it*,
because none of us remember a file exists unless the index says so.

Core bet for this folder, same as `data-orchestration/` and `python-web/`: pretrained knowledge
here is **MLflow 2.x**, and 3.x did not merely add API surface — it changed defaults that every
remembered tutorial depends on. That is the dangerous kind of staleness: a 2.x answer is still
fluent, still syntactically valid, and now *raises an exception on the first command*. So the
highest-value content is (a) the **delta** since pretraining, (b) **dated** facts, (c) claims
**verified against a local checkout or a running server**, never recalled.

Format per line: `[status] path — one-line summary — when you need it`.
Status: `active` (trust it), `superseded by <path>`, `stale <date>` (re-verify before use).

---

MLflow has more than one entry, so it has its **own folder, its own index, and a
machine-readable header on every entry**: `machine-learning-ops/mlflow/INDEX.md`. Read that
first — it defines the header contract (`triggers` = the literal strings a reporter pastes) and
the tool that searches it, `.claude/memory/lucas/communities/tools/kb_lookup.py --repo
mlflow/mlflow --ticket <n>`.

- `active` `machine-learning-ops/mlflow/INDEX.md` — index + retrieval contract for the MLflow
  entries, and the list of areas deliberately *not* written yet, each with its reason. — start
  here for anything MLflow.
- `active` `machine-learning-ops/mlflow/mlflow-2026-snapshot.md` — dated (2026-08-15) delta
  between the training cutoff and MLflow 3.15.1: the filesystem backend raising unless
  `MLFLOW_ALLOW_FILE_STORE=true` (with the `mlflow migrate-filestore` escape hatch), MLServer's
  removal as a serving backend, flipped serialization defaults (`pt2`, `skops`), async trace
  logging on by default, first-class logged models changing what `runs:/` resolves to, the whole
  tracing/GenAI surface that postdates training, and the `get-history` pagination semantics that
  *inverted* between 3.13 and 3.14. — anyone answering an MLflow question, debugging a tracking
  server, or about to repeat a 2.x-era recipe.
- `active` `machine-learning-ops/mlflow/mlflow-auth-rbac.md` — dated (2026-08-17) model of the
  `basic-auth` app after two rewrites: roles + `role_permissions` (3.12) replacing the
  per-resource permission endpoints that were **removed** in 3.13, how a grant actually resolves
  at request time (`default_permission` is a floor; workspace `USE` no longer folds into resource
  lookups), workspaces and the **immutable** `artifact_location` prefix, the 403-on-artifact-upload
  failure and its fix in 3.15.0, and five setup traps that make a correct configuration look
  broken (mandatory Flask secret key, 12-char password floor, the workspace header, Host-header
  validation, shipped default credentials). — any 403 / "Permission denied" / RBAC / workspaces
  question, and before repeating a remembered `experiments/permissions/create` recipe.
- `active` `machine-learning-ops/mlflow/mlflow-tracing-otel-interop.md` — dated (2026-08-22)
  mechanism entry for `area/tracing`: MLflow keeps an **isolated tracer provider** but shares the
  **process-global meter provider**, so an application that owns a `MeterProvider` silently takes
  MLflow's span-duration metric and the configured OTLP metrics endpoint receives nothing; the
  routing precedence in `_get_span_processors` (a `set_destination` destination beats OTLP unless
  dual export is on); the generic `OTEL_EXPORTER_OTLP_ENDPOINT` enabling **both** signals, which
  is how a per-span `trace_destination=` ends up ignored; protocol defaulting to **grpc**; the
  four entry points that rebuild span processors, with span processors retired since 3.15.0 and
  the meter provider not; why shutting the retired meter provider down would silence metrics for
  the process; unbounded metric-label cardinality from trace tags; and three traps in MLflow's own
  tracing tests. — any OTLP / collector / exporter / thread-leak / "my metrics never arrive"
  question.
- `active` `machine-learning-ops/mlflow/mlflow-release-map.md` — dated (2026-08-17) map of every
  3.x tag with its date and Python floor, the landmark commits mapped to the first release
  containing each, and the numbering trap: **there is no `v3.11.0` tag** (3.11 shipped only as
  `v3.11.1`), so a failed `git show v3.11.0:…` means a missing tag, not missing code. Plus the
  three-command method for "when did this change / where did it ship / what did it look like". —
  every ticket that names a version, i.e. every ticket.

## What is deliberately not here

Written on demand, when a real task needs them — three speculative entries are how a knowledge
base becomes decorative:

* **Other MLOps tools.** Nothing on W&B, Kubeflow, ZenML or DVC, because nobody here has used
  them in anger. A comparison written from pretraining would be exactly the fluent-and-stale
  content this folder exists to counter.
* **Cloud artifact stores** (S3/GCS/Azure). No credentials in the zoo, so anything written would
  be unverifiable by us — and this folder's rule is that entries are checkable.
* **MLflow judges, GenAI autologging and the trace UI.** The OTel interop half of tracing is now
  written (`mlflow/mlflow-tracing-otel-interop.md`, 2026-08-22); the rest of the tracing surface
  still waits for a real ticket, and the UI half is out of scope for us by standing rule.
