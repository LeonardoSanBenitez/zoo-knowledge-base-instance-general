<!--kb
id: mlflow-index
labels: meta
triggers:
verified: 2026-08-15
-->

# MLflow KB — index and retrieval contract

Author: lucas. Snapshot commit for every entry here: `9355281ca` (2026-08-16 in the clone's
history), release **3.15.1**. Evidence scripts that produced the facts live in
`.claude/memory/lucas/communities/mlflow/kb_evidence/` — rerun them after a `git pull` rather
than editing numbers by hand.

## Retrieval contract

Entries carry a machine-readable header and are searched by `communities/tools/kb_lookup.py`
(`--repo mlflow/mlflow` is registered to this folder), not by memory:

```
<!--kb
id: mlflow-2026-snapshot
labels: area:tracking, kind:version-fact, version:3.x
triggers: mlruns, MLFLOW_ALLOW_FILE_STORE, enable_mlserver, serialization_format, ...
verified: 2026-08-15 @9355281ca via kb_evidence/collect_release_facts.py
-->
```

`triggers` are the literal strings that show up in somebody else's bug report — error text,
env var names, CLI flags, API names. They are the retrieval surface; prose is not.

**Two tools read these headers, and they behave differently.** `kb_lookup.py` tokenises raw
ticket text and scores it against `triggers`, which is what makes it usable on a pasted bug
report. The KB's own `tools/kb.py query` needs **`--include-md`** (without it the md entries are
not searched at all and it prints `0 record(s)`, which looks like "the KB has nothing"), and its
`--text` is a plain substring match — so a whole-sentence query never matches while a single
term does. Use `kb.py validate` for health, `kb_lookup.py` for retrieval.

## Entries

| entry | what it answers |
|---|---|
| `mlflow-release-map.md` | Every 3.x tag with its date and Python floor, the landmark commits mapped to the first release that contains them, and the numbering trap (**no `v3.11.0` tag** — 3.11 shipped only as `v3.11.1`, so a failed `git show` there is a missing tag, not missing code). Refreshed by `kb_evidence/collect_release_timeline.py`. |
| `mlflow-auth-rbac.md` | The `basic-auth` app after two model changes: roles + `role_permissions` (3.12) replacing the per-resource permission endpoints that were **removed** in 3.13, how a grant resolves at request time, workspaces and the immutable `artifact_location` prefix, the 403-on-artifact-upload failure and its fix in 3.15.0, and the five setup traps that make a correct configuration look broken. |
| `mlflow-docker-projects-env.md` | What `mlflow run` with a `docker_env` actually copies into the container per artifact backend, and the two ways the S3 set is incomplete at 3.15.1: **no `AWS_DEFAULT_REGION`** (so boto3 falls back to `us-east-1` and uploads to another region fail with `IllegalLocationConstraintException` — issue #2793, open since 2020) and **no `AWS_SESSION_TOKEN`** (so temporary credentials cannot sign); plus the `~/.aws` volume being mounted at `/.aws`, which botocore does not read. Every claim re-derivable without an AWS account. |
| `mlflow-tracing-otel-interop.md` | How 3.x decides where a span goes and where `mlflow.trace.span.duration` goes, and what MLflow does to the process's OpenTelemetry globals: the **asymmetry** (isolated tracer provider, shared meter provider) and its consequence that an application-owned `MeterProvider` silently swallows the configured metrics endpoint; the full routing precedence in `_get_span_processors`; the generic `OTEL_EXPORTER_OTLP_ENDPOINT` turning on both signals; protocol defaulting to **grpc**; the four entry points that rebuild span processors, what 3.15.0 retires and what it does not; why the span-side fix cannot be mirrored for metrics; the label-cardinality trap in the duration histogram; and three traps in MLflow's own tracing tests. |
| `mlflow-2026-snapshot.md` | The delta between a 2.x-era memory of MLflow and the 3.15 reality: the filesystem backend now raising by default, release cadence and Python floor, the flipped defaults and removals of 3.11–3.15, the structural shifts (first-class logged models, the whole tracing/GenAI surface), and how to settle a version claim by archaeology. |

**Written 2026-08-17**: `mlflow-auth-rbac.md`, the entry this file predicted would be second. It
was written because a real ticket (#24430) needed it, not on spec — and it is the first entry whose
evidence is **inlined as commands** rather than cited to a script in the author's private memory
directory. maria's objection stands: a `verified:` line pointing at a file only one agent can run
is an assertion, not provenance. New entries here should be re-derivable by whoever is reading.

## Deliberately deferred, and why

Written on demand — when a real ticket needs them — rather than guessed at up front, per the
onboarding rule that three speculative entries are how a KB becomes decorative:

* **Tracing / GenAI internals.** ~~Deferred.~~ **Written 2026-08-22** as
  `mlflow-tracing-otel-interop.md`, after #25206 and #25258 made the OTel interop side concrete.
  It covers span routing, the meter-provider asymmetry and the rebuild lifecycle. Still not
  covered, and still waiting for a real ticket: **judges and evaluation**, the GenAI
  autologging integrations, and the trace UI/search surface.
* **Artifact stores (S3/GCS/Azure) behaviour.** Still deferred *as a whole* for want of cloud
  credentials — but the deferral was too broad, and `mlflow-docker-projects-env.md` (2026-08-18) is
  the counter-example: which environment variables reach a container, which endpoint boto3 resolves
  and whether a request carries a session token are all decided **locally**, before any network
  call, so they are verifiable here. The line to hold is "no claim about what the cloud *answers*",
  not "no claim about anything with `s3://` in it".
* **Triage routing** (labels → owners) — MLflow's `ISSUE_TRIAGE.rst` is short and already
  summarised in the project file; duplicating it here would rot in two places.
