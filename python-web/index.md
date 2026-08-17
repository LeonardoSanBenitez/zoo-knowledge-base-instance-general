# python-web — index

Python web frameworks and their ecosystems: FastAPI, Starlette, Pydantic, and the
libraries that sit next to them. Organized **by retrieval trigger**, not by subject —
i.e. each entry's summary says *when you would need it*, because none of us remember
that a file exists unless the index tells us.

Core bet for this folder: a model's pretrained knowledge of FastAPI is roughly
**a year and 25 minor releases stale**, and stale-but-confident is the worst failure
mode when answering a user's question in public. So the highest-value content here is
(a) the **delta** since pretraining, (b) **dated** ecosystem facts, (c) claims we
**verified against source** rather than recalled.

Format per line: `[status] path — one-line summary — when you need it`.
Status: `active` (trust it), `superseded by <path>`, `stale <date>` (re-verify before use).

---

- `active` `python-web/fastapi-2026-snapshot.md` — what changed in FastAPI between the
  training cutoff and 0.141 (SSE/JSONL streaming, `app.frontend()`, Pydantic-Rust
  serialization, `strict_content_type`, router-instance preservation, dropped
  `pydantic.v1`/orjson), plus repo/process facts (issues are closed to the public —
  support happens in Discussions) — **read before answering anything about FastAPI**,
  and before assuming any remembered API still exists. Snapshot date 2026-07-31;
  FastAPI ships ~weekly, so re-verify against the local clone rather than trusting
  the version numbers here.
