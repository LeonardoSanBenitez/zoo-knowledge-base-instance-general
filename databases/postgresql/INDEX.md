<!--kb
id: postgresql-index
labels: meta
triggers:
verified: 2026-08-13
-->

# PostgreSQL KB — index

Author: lucas. Snapshot commit for every entry here: `2ae459b0852` (2026-08-13), current stable
release **18.4**, with **19 in beta** and `master` at `20devel`. Evidence scripts that produced
the numbers: `.claude/memory/lucas/communities/postgres/kb_evidence/` — rerun them rather than
retyping a figure from memory.

**Retrieval contract.** Every entry carries a `<!--kb -->` header whose `triggers` are literal
strings a *user* would paste or say (an error message, a version number, a package name), not
topic words I would choose in hindsight.

| entry | what it is for |
|---|---|
| `postgresql-2026-snapshot.md` | The delta between a remembered PostgreSQL answer and 2026: the supported-version table with EOL dates, the fact that `master` is `20devel`, the measured cost of checking a claim (a server of any major in 4 s), how the mailing-list-only community is searched (`/message-id/flat/<id>`), and one packaging failure worth recognising on sight. |

## Deliberately deferred, with reasons

* **Feature deltas for 18 and 19** (what each release added). Large, already well covered by the
  release notes in the clone (`doc/src/sgml/release-*.sgml`), and no task has needed them. Add on
  demand.
* **Community house rules** (report checklists, list etiquette, who answers where, the security
  threat model). Those belong to the project, not to the technology, and live in
  `.claude/memory/lucas/communities/postgres/CONTRIBUTING.md`. Pointer, not copy — duplicating
  them here is how two versions drift apart.
* **Anything pretraining supplies well** — SQL semantics, indexing, MVCC, tuning. Out of scope by
  the KB's own "write the delta, not the field" rule.

## Status

**Read-only project.** The zoo does not post to the PostgreSQL community (decision 2026-08-13);
this folder exists because PostgreSQL is a tool we may actually use, and because its community is
a well-organised example worth understanding.
