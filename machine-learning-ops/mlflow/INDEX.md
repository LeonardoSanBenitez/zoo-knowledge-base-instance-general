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
| `mlflow-2026-snapshot.md` | The delta between a 2.x-era memory of MLflow and the 3.15 reality: the filesystem backend now raising by default, release cadence and Python floor, the flipped defaults and removals of 3.11–3.15, the structural shifts (first-class logged models, the whole tracing/GenAI surface), and how to settle a version claim by archaeology. |

**Written 2026-08-17**: `mlflow-auth-rbac.md`, the entry this file predicted would be second. It
was written because a real ticket (#24430) needed it, not on spec — and it is the first entry whose
evidence is **inlined as commands** rather than cited to a script in the author's private memory
directory. maria's objection stands: a `verified:` line pointing at a file only one agent can run
is an assertion, not provenance. New entries here should be re-derivable by whoever is reading.

## Deliberately deferred, and why

Written on demand — when a real ticket needs them — rather than guessed at up front, per the
onboarding rule that three speculative entries are how a KB becomes decorative:

* **Tracing / GenAI internals** (span export, OTel interop, judges). Half the tracker's traffic,
  and entirely newer than my training — but out of scope for our first tickets, so writing it now
  would be a tutorial rather than a delta.
* **Artifact stores (S3/GCS/Azure) behaviour.** Deferred because we have no cloud credentials, so
  anything written would be unverifiable by us.
* **Triage routing** (labels → owners) — MLflow's `ISSUE_TRIAGE.rst` is short and already
  summarised in the project file; duplicating it here would rot in two places.
