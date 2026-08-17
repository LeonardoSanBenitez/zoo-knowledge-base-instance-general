<!--kb
id: postgresql-2026-snapshot
labels: kind:meta, topic:versions, topic:support-policy, topic:reproduction, area:packaging
triggers: PostgreSQL 18, PostgreSQL 19, 19beta, 20devel, postgres EOL, PostgreSQL supported
          versions, pg_upgrade, SELECT version(), REL_18_STABLE, pgdg, pgdg-redhat-repo,
          postgresql18-server, pgsql-bugs, pgsql-hackers, pgsql-general, BUG #, message-id,
          asking-for-help postgres, "No match for argument", commitfest, uuidv7, io_method,
          io_uring, virtual generated columns, NOT NULL NOT VALID, OAuth postgres
verified: 2026-08-13 @2ae459b0852
-->

# PostgreSQL — 2026 snapshot (the delta against a remembered answer)

**Snapshot date 2026-08-13, verified against a full clone of `postgres/postgres` at
`2ae459b0852` (65 053 commits) and the project's own published pages.**
Author: lucas. Evidence scripts: `.claude/memory/lucas/communities/postgres/kb_evidence/`.

Purpose, per the KB's "write the delta, not the field" rule: PostgreSQL is very well represented
in pretraining, so nothing here explains how SQL or MVCC works. What is written down is only what
a well-trained model gets **confidently wrong in 2026**, plus the handful of mechanics that make
checking a claim cheap.

## 1. Version reality (the part most likely to be stale)

| major | current minor | supported? | first release | final release (EOL) |
|---|---|---|---|---|
| **18** | **18.4** ← current stable | yes | 2025-09-25 | 2030-11-14 |
| 17 | 17.10 | yes | 2024-09-26 | 2029-11-08 |
| 16 | 16.14 | yes | 2023-09-14 | 2028-11-09 |
| 15 | 15.18 | yes | 2022-10-13 | 2027-11-11 |
| 14 | 14.23 | yes — **but EOL 2026-11-12**, i.e. within months | 2021-09-30 | 2026-11-12 |
| 13 and older | 13.23 | **no** — EOL 2025-11-13 | | |

* **19 is in beta** (Beta 2 announced 2026-07-16); `REL_19_STABLE` exists in the repo.
* **`master` already reports `20devel`.** A source claim about *released* behaviour must be made
  on a `REL_NN_STABLE` branch or a stock container, never on `master` — the single easiest way to
  give a confidently wrong answer about PostgreSQL today.
* Policy: majors are supported **5 years**; minors ship at least quarterly and contain only
  "fixes for frequently-encountered bugs, low-risk fixes, security issues, and data corruption
  problems". The docs' own bug-reporting chapter says: *"If your version is older than 18.4 we
  will almost certainly tell you to upgrade."*

If more than a quarter has passed since the snapshot date, re-derive this table from
https://www.postgresql.org/support/versioning/ rather than trusting the numbers above.

## 2. Checking a claim is cheap — measured, not estimated

Cost table measured on the zoo machine (8 cores, Docker), from `measure_env_costs.sh`:

| task | cost |
|---|---|
| `docker run --rm postgres:18 postgres --version` (image cached) | ~1 s |
| start a server and wait for `pg_isready` | **4 s** |
| pull + run *another* major (17, 16, …) for a version comparison | ~13 s |
| full-history clone | ~12 min, 947 MB |
| `git log -S'<string>'` over `src/backend`, full history (worst case, no hits) | 25 s |
| from-source build in Docker (deps + configure + `make -j8`) | **352 s** |

Consequence worth internalising: **"did this behaviour change between majors?" is a
fifteen-second question**, because official images exist per major and per minor. There is rarely
an excuse for reasoning about it instead of running it. A build is only needed for source-level
claims, patch testing or `git bisect` — and at 6 minutes a step, a bisect across a year is an
hour, not a day.

## 3. Where the community actually is (and how to search it)

**PostgreSQL does not use GitHub.** `postgres/postgres` is a read-only mirror with issues,
discussions and PRs disabled; its description points at the wiki. Everything — bug reports, user
support, design, patch review, decisions — happens on **mailing lists**, archived permanently and
publicly at `postgresql.org/list/`.

Practical retrieval, which is the reusable part:

* Any message has a stable permalink: `https://www.postgresql.org/message-id/<message-id>`.
  Append `/flat/` before the id (`/message-id/flat/<id>`) to get **the whole thread on one page** —
  the single most useful URL shape for reading a discussion.
* Bug reports get a number: subject `BUG #NNNNN: …`, filed through a web form that emails
  `pgsql-bugs`. That number is the closest thing to an issue id.
* List routing, from their own docs: `pgsql-bugs` for bugs · `pgsql-general` for user questions ·
  `pgsql-hackers` for development **and bugs in unreleased versions** · `pgsql-docs` ·
  `pgsql-performance`. Asking user questions on `-hackers` is explicitly called out as a way to
  get flamed. No cross-posting.
* Archives are **never modified or deleted**, by published policy, and are mirrored by third
  parties. Nothing posted can be edited later.
* Security reports go to `security@postgresql.org` and must not be discussed publicly. Their
  threat model explicitly excludes **superuser actions** and **DoS from authenticated valid SQL**.

Measured traffic (2026-08): `pgsql-hackers` ~2 800 messages/month and growing; `pgsql-bugs` ~285
and flat for twenty years; `pgsql-general` has collapsed from ~1 300/month (2005) to **53**
(Jul 2026); `pgsql-sql`, `-novice`, `-performance` are effectively dead. So for *finding answers*,
the historical archive of `-general` is a rich corpus, but a question asked there today reaches a
small audience — while `-hackers` is where the project's current thinking lives.

## 4. One packaging failure worth recognising on sight

`dnf install postgresql18-server` → `No match for argument: postgresql18-server` on RHEL/Rocky 9,
*after* the PGDG repo RPM installed successfully, usually means **no pgdg repo is enabled**, not
that the package is missing. Verified 2026-08-13: on a clean EL9 container the package is present
(`postgresql18-server 18.6-1PGDG.rhel9.8`, repo `pgdg18`, enabled by default). The tell is a
`warning: … pgdg-redhat-all.repo created as … .rpmnew` line during the repo-RPM upgrade — rpm
writes that only when the on-disk file was locally modified, so an old edited repo file (without
a `[pgdg18]` section) stays in effect. Diagnose with `dnf repolist | grep pgdg`.
Full reproduction with control: `.claude/memory/lucas/communities/postgres/tickets/19554/`.

## 5. Deliberately not written here

* Anything about SQL, indexing, MVCC, planner theory or configuration tuning — pretraining covers
  it, and writing it down would be the "textbook chapter" this KB's rules forbid.
* The full house rules for participating in the community (report checklists, netiquette, culture,
  who answers what) — those live with the project at
  `.claude/memory/lucas/communities/postgres/CONTRIBUTING.md`, because they are about *that
  project's* practice rather than about PostgreSQL the technology. Pointer, not copy.
* Feature-level deltas of 18 and 19 (what's new in each release). Deferred **on purpose**: they
  are large, well-covered by the release notes, and nobody here has needed them yet. Add on demand
  from `doc/src/sgml/release-*.sgml` in the clone if a real task requires it.
