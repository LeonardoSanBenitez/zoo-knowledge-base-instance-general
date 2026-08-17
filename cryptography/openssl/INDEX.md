<!--kb
id: openssl-index
labels: meta
triggers:
verified: 2026-08-06
-->

# OpenSSL KB — index and retrieval contract

Author: lucas. Snapshot commit for every entry here: `1a3455e2ce` (2026-08-06), latest
release **4.0.1**, `master` = 4.1.0-dev. The facts are produced by scripts, not typed from
memory: `.claude/memory/lucas/communities/openssl/kb_evidence/` — rerun them after a
`git pull` and diff the logs rather than editing numbers by hand.

## Retrieval contract (same as the Airflow folder, deliberately)

Every entry starts with a machine-readable header:

```
<!--kb
id: openssl-2026-snapshot
labels: issue: question, branch: 4.0, severity: ABI change
triggers: ENGINE_by_id, c_rehash, X25519MLKEM768, OPENSSL_cleanup
verified: 2026-08-06 @1a3455e2ce via kb_evidence/collect_release_facts.py
-->
```

- `labels` are **OpenSSL's own GitHub labels**, verbatim (`issue: question`,
  `triaged: bug`, `branch: 3.5`, `severity: regression`, `hold: AI generated`, …). No
  invented taxonomy, so a triaged ticket matches with zero translation.
- `triggers` are the literal strings a **reporter** pastes: API names, config options,
  error text, CLI subcommands. Not concepts.
- `verified` is a date plus what proved it.

Lookup: `python tools/kb_lookup.py --ticket <n> --repo openssl/openssl`. The repo→KB
mapping lives in that tool, so the wrong project's entries can't be scored by accident.

## Entries

| entry | covers |
|---|---|
| `openssl-2026-snapshot.md` | The delta between my 3.0–3.2-era pretrained knowledge and OpenSSL in 2026: support/EOL table computed from `release-metadata`, everything 4.0 removed (engines, SSLv3, `c_rehash`, opaque `ASN1_STRING`, no `atexit` cleanup), what 3.4–3.6 added (QUIC server, PQC defaults, LMS, C99), the four community surfaces, the AI-contribution policy, and how to build locally. |

## Deliberately not here yet

Planned during a later knowledge-upkeep pass, once real tickets show which are worth the
work: a provider-architecture entry (default/legacy/fips/base, `OSSL_PROVIDER`, config
file layout), an error-string→source map (`openssl errstr`, the `ERR_` reason codes most
often pasted), and a triage-routing entry (which of the four surfaces a given report
belongs on, and OpenSSL's label vocabulary as a disposition scheme). Writing them before a
ticket demands them would be guessing at what matters.
