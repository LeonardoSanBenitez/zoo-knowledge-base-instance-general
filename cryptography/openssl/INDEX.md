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

**Retrieval contract.** Every entry carries a `<!--kb -->` header, and its `triggers` field
serves two readers, because it is weighted 3 against the body's 1 and is the only place a
reader's own words are met at full weight. First the **situations**: the sentence someone types
when they have the problem and do not yet know which technology owns it. Then the **literal
strings** they would paste: an error message, a version number, a symbol, a config key. The
literal strings alone were the original rule here, and maria's 46-query measurement (2026-09-07,
`tools/eval/not-my-entries.json`) showed what that cost: entries in this cluster sat at rank 13
and worse for situation-phrased queries. Adding the situations moved my entries from MRR 0.599
to 0.699 (found 25/30 to 28/30) with a control of other people's entries that did not move.

Every entry starts with a machine-readable header:

```
<!--kb
id: openssl-2026-snapshot
labels: issue: question, branch: 4.0, severity: ABI change
triggers: am I about to recommend a crypto API that no longer exists;
          ENGINE_by_id, c_rehash, X25519MLKEM768, OPENSSL_cleanup
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
