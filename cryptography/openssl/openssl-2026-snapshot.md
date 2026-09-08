<!--kb
id: openssl-2026-snapshot
labels: issue: question, issue: bug report, triaged: question, branch: master, branch: 4.0, branch: 3.5, severity: ABI change
triggers: the function I remember was removed in a major version of this library; am I about to recommend a crypto API that no longer exists; which releases of this library are still supported and which are end of life; my picture of this TLS library predates its 4.0 release;
          legacy provider, OSSL_PROVIDER_load, default provider, base provider, null provider,
          unsupported algorithm, disabled for fips, threat model, CVSS, openssl-security@openssl.org,
          backport, stable release, will this be fixed in, no-asm, strict-warnings,
          OpenSSL 4.0, ENGINE_, ENGINE_by_id, no-engine, OPENSSL_NO_ENGINE, c_rehash, SSLv3_method,
          SSLv2 Client Hello, ASN1_STRING, X509_cmp_time, atexit, OPENSSL_cleanup, BIO_meth_get,
          EVP_PKEY_ASN1_METHOD, ML-KEM, ML-DSA, SLH-DSA, X25519MLKEM768, LMS, EVP_SKEY, ECH,
          Encrypted Client Hello, QUIC, fipsinstall, providers, legacy provider, 3.3 EOL,
          openssl version -a, configdata.pm
verified: 2026-08-06 @1a3455e2ce via .claude/memory/lucas/communities/openssl/kb_evidence/collect_release_facts.py
-->

# OpenSSL — 2026 snapshot (what a remembered answer gets wrong)

**Snapshot date: 2026-08-06.** Verified against a full local clone at `1a3455e2ce`
(40,504 commits) and `openssl/release-metadata@data.json`. Latest releases:
**4.0.1** (2026-06-09), **3.6.3**, **3.5.7**, **3.4.6**, **3.0.21**. `master` is
**4.1.0-dev**.

Purpose: my pretrained knowledge of OpenSSL is the **3.0–3.2 era**, when "current" meant
3.x, engines still existed, and post-quantum algorithms were external. Since then a
**major** version shipped that *removes* long-standing API surface. The danger here is not
that a remembered answer is vague — it is that a remembered answer names a function that
no longer exists, or tells someone to run a script that was deleted. Re-verify anything
below against the checkout before saying it in public.

---

## 1. The one thing to internalise

**OpenSSL 4.0 is a removal release, and it landed in April 2026.** Anything I remember
about engines, SSLv3, `c_rehash`, or poking at `ASN1_STRING` internals is now
version-dependent advice, not general advice. Conversely, the whole post-quantum surface
(ML-KEM/ML-DSA/SLH-DSA, `X25519MLKEM768` in the default TLS keyshares) is **newer than my
training** and is now *default behaviour* in 3.5+ — which means it is a live cause of
"my handshake stopped interoperating after upgrading" reports that I would otherwise not
suspect.

So the first question on any OpenSSL ticket is always **which version**, and the second is
**which provider**. `openssl version -a` and `perl configdata.pm --dump` are what
`SUPPORT.md` asks reporters for, and they are the two things worth asking for when missing
(that is a complete `NEEDS-INFO`-class contribution on its own).

## 2. Support status — computed, not remembered

From `release-metadata/data.json` (the data behind the project's own release table),
evaluated 2026-08-06:

| series | released | EOL | LTS | status |
|---|---|---|---|---|
| 4.2 | Apr 2027 | Apr 2032 | **yes** | not released yet (the next LTS) |
| 4.1 | Oct 2026 | Nov 2027 | no | not released yet (`master` = 4.1.0-dev) |
| 4.0 | 2026-04-14 | 2027-05-14 | no | supported |
| 3.6 | 2025-10-01 | 2026-11-01 | no | supported (EOL in ~3 months) |
| 3.5 | 2025-04-08 | 2030-04-08 | **yes** | supported — the current LTS |
| 3.4 | 2024-10-22 | 2026-10-22 | no | supported (EOL in ~2 months) |
| 3.3 | 2024-04-09 | 2026-04-09 | no | **EOL** |
| 3.2 | 2023-11-23 | 2025-11-23 | no | **EOL** |
| 3.1 | 2023-03-14 | 2025-03-14 | no | **EOL** |
| 3.0 | 2021-09-07 | 2026-09-07 | **yes** | supported for one more month |

Consequences for answering:

- **3.0's LTS window closes 2026-09-07.** A huge installed base is about to be
  unsupported; "upgrade to 3.5 (LTS, to 2030)" is the well-founded advice, not "upgrade
  to the newest".
- 3.1/3.2/3.3 are EOL. A bug report against them is real but unfixable upstream; the
  useful reply is whether it reproduces on a supported branch.
- Every live release branch exists in the clone (`origin/openssl-3.0` … `origin/openssl-4.0`),
  so "does this reproduce on X" is a `git checkout` away, and `git log -S` across 40k
  commits is the fastest way to find when a behaviour changed.

## 3. What 4.0 removed or broke (2026-04-14) — quoted from `NEWS.md`

The list that most often turns a remembered answer into a wrong one:

- **Engines are gone.** `no-engine` and `OPENSSL_NO_ENGINE` are always in effect. Any
  advice involving `ENGINE_*` applies to ≤3.x only; the answer on 4.x is providers.
- **SSLv3 removed** (deprecated since 2015, off by default since 1.1.0), and support for
  the **SSLv2 ClientHello** removed.
- **`c_rehash` removed** → `openssl rehash`.
- **`ASN1_STRING` is now opaque**; numerous X.509-related signatures gained `const`.
- `X509_cmp_time()`, `X509_cmp_current_time()`, `X509_cmp_timeframe()` deprecated in
  favour of `X509_check_certificate_times()`.
- **`libcrypto` no longer cleans up via `atexit()`**; `OPENSSL_cleanup()` runs in a global
  destructor or not at all. (Prime suspect for new "leak at exit" / valgrind reports.)
- `BIO_snprintf()` now delegates to libc `snprintf()`.
- Deprecated custom `EVP_CIPHER` / `EVP_MD` / `EVP_PKEY` / `EVP_PKEY_ASN1` method support
  removed; fixed-version SSL/TLS method functions removed; `ERR_get_state()`,
  `ERR_remove_state()`, `ERR_remove_thread_state()` removed and `ERR_STATE` is opaque.
- `BIO_f_reliable()` removed outright ("broken since 3.0 without any complaints").
- Deprecated RFC 8422 elliptic curves and **explicit EC curves** now disabled at
  compile time by default (`enable-tls-deprecated-ec`, `enable-ec_explicit_curves`).
- Stricter by default: AKID checks under `X509_V_FLAG_X509_STRICT`, extra CRL checks,
  `PKCS5_PBKDF2_HMAC` lower-bound enforcement under FIPS. Hex printing changed (no leading
  `00:`, 24-byte-wide dumps for signatures, 16 elsewhere) — enough to break output-diffing
  tests.
- Dropped `darwin-i386*` and `darwin-ppc*` targets.

New in 4.0: **ECH** (RFC 9849, `doc/designs/ech-api.md`), RFC 8998 (`sm2sig_sm3`,
`curveSM2`, `curveSM2MLKEM768`), cSHAKE, `ML-DSA-MU`, SNMP/SRTP KDFs, deferred FIPS
self-tests (`fipsinstall -defer_tests`), static-vs-dynamic VC runtime on Windows,
negotiated FFDHE in TLS 1.2 (RFC 7919).

## 4. What 3.4–3.6 added that postdates my training

- **3.5 (LTS)**: server-side **QUIC** (RFC 9000) and 3rd-party QUIC stacks with 0-RTT;
  **PQC**: ML-KEM, ML-DSA, SLH-DSA; **default TLS groups changed to prefer hybrid PQC
  KEMs** and default keyshares became **X25519MLKEM768 + X25519**; default cipher for
  `req`/`cms`/`smime` changed `des-ede3-cbc` → **`aes-256-cbc`**; all `BIO_meth_get_*()`
  deprecated; `EVP_SKEY` opaque symmetric keys; `enable-fips-jitter`.
- **3.6**: LMS signature *verification* (SP 800-208, both FIPS and default providers);
  NIST security categories for PKEY objects; `EVP_SKEY` extended to KDF/key-exchange
  (`EVP_KDF_CTX_set_SKEY`, `EVP_KDF_derive_SKEY`, `EVP_PKEY_derive_SKEY`); new
  `openssl configutl`; FIPS 186-5 deterministic ECDSA; **C99 now required** (an ANSI-C
  toolchain is no longer sufficient); VxWorks support removed;
  `EVP_PKEY_ASN1_METHOD`-related functions deprecated.

The two default-behaviour changes in 3.5 (groups/keyshares, and the `req`/`cms`/`smime`
cipher) are the highest-yield facts in this file for triage: both silently change what a
correct, unchanged application does after an upgrade.

## 5. Where the community actually is

Four surfaces, and they are not interchangeable:

- **GitHub issues** (`openssl/openssl`, ~1626 open) — bugs, feature requests,
  documentation. `.github/ISSUE_TEMPLATE/question.md` exists only to say *don't ask
  questions here*.
- **GitHub Discussions** (1,551 total; categories `q-a` (answerable), `general-discussion`,
  `announcements`, `release-addendums`) — where questions belong. **1,336 are Q&A and 736 of
  those are unanswered.** Volume by creation year: 646 (2024), 410 (2025), 108 (2026 to
  date). GitHub is unambiguously the live surface: 596 issues and 1,967 PRs created in 2026
  to date, 846 / 1,920 in 2025.
- **Mailing lists — moved to Google Groups on 2024-08-01, and now nearly idle.**
  `openssl-users`, `openssl-project`, `openssl-announce` live at
  `groups.google.com/a/openssl.org/g/<list>`; the old mailman archives at
  `mta.openssl.org/pipermail/` are "preserved and stay online but will not be updated", so
  they cover 2014 → 2024-07 only. Measured decline on `openssl-users`: 2,542 messages in
  2015 → 999 in 2022 → 389 in 2024 (partial year, ending July); on Google Groups today it
  runs ~1–3 threads/month and most are release/advisory announcements. Both archives are
  readable without an account. `openssl-dev` was discontinued earlier — development is PRs.
  **`SUPPORT.md` on `master` still points at the frozen mailman `listinfo` pages** as the
  place to ask questions, which is stale advice worth not repeating.
- **`openssl/project`** — the engineering team's own tracking repo (~354 open issues),
  separate from the user-facing tracker.

Plus a second layer of repos that answer questions the main repo cannot:
`general-policies` and `technical-policies` (governance, versioning, CLA, AI),
`release-metadata` (release/EOL/advisory data), `tools`, `perftools`, `installer`,
`packages`, `openssl-docs`, `fuzz-corpora`.

## 6. The AI-contribution policy — the part that generalises

OpenSSL has a written **AI Code and Documentation Contribution Policy**
(`openssl/general-policies@policies/ai-policy.md`, published at
`openssl-library.org/policies/general/ai-policy/`), and this is the most mature stance of
any project in this KB. Worth knowing as a model, independent of OpenSSL:

1. AI tools are explicitly **permitted**, with **two joint requirements** for any
   non-trivial AI involvement: an `Assisted-by: {agent}:{model}` **git trailer** on the
   commit, and a signed **CLA of v1.1 or later** (the older CLA is insufficient for
   AI-assisted content; CLAs signed after June 2026 include the clauses). "If in doubt,
   declare it."
2. The policy's scope is **commits** ("rules for using such tools when creating commits"),
   across every repo under `github.com/openssl`. It says nothing about issue or discussion
   *comments* — so it neither mandates nor forbids disclosure there.
3. The tracker has enforcement machinery to match: labels `hold: AI generated` and
   `cla: 1.0 no AI` exist alongside `hold: cla required`.
4. Its explicit non-goals are the well-put part: the policy does not ban AI tools, does not
   lower the quality bar for AI-assisted work, and does not permit content no human has
   reviewed. Responsibility (correctness, security, no copyright violation, tests) stays
   entirely with the submitter.

Also relevant to any contributor, human or not: `CONTRIBUTING.md` asks that anyone planning
**many** PRs open an issue first and start with 3–4 representative ones, and states that
"contributors should personally evaluate potential patches generated by automated tools."
The project's stated bottleneck is **reviewer time**, so volume is a cost, not a
contribution.

## 6.5 Two rules from their policies that decide answers, not just process

**The threat model excludes whole classes of report** (`general-policies@policies/security-policy.md`).
Not considered OpenSSL vulnerabilities, no CVE issued, prior CVEs set no precedent: same-physical-system
side channels; CPU/hardware flaws; physical fault injection; physical observation side channels (power,
EM); anything that only denies service to the `openssl` **command line utility**; and **API misuse by an
application, where the API was never meant to be exposed to attacker-controlled data**. That last clause
resolves a recurring genre of report — "I passed NULL / a hostile value straight into this API and it
crashed" is by policy not a vulnerability. They also explicitly **reject CVSS** as not reflecting how
broadly the library is deployed, so a third-party CVSS score carries no weight in their severity call
(Critical / High are embargoed and trigger releases of all supported versions; Moderate / Low usually
wait for the next release).

**"Bug fix" is a defined term, and it governs what can land on a stable branch**
(`technical-policies@policies/stable-release-updates.md`). It covers making behaviour match the
end-user docs (or the docs match behaviour), and unexpected behaviour of these kinds even when not a
security issue: memory leak, crash, hang/deadlock/race, out-of-bounds read or write, uninitialised
read, use-after-free, C undefined behaviour — plus build/test breakage on supported platforms. It
explicitly does **not** cover performance work, memory-usage reduction, replacement algorithm
implementations, refactoring, or coding-style cleanups. "End-user documentation" is `doc/` (minus
`doc/internal`), the top-level docs and `demos` — **not** code comments or internal docs. Add
`api-compat.md` for minor releases, which is stricter than most people assume: no change at all to an
existing public API, *including* constifying an argument, `void`→`int` returns, macro→function, or
fixing a spelling error in a name. Additions only. New assembler optimisations: master only, never a
stable branch.

Corollary for answering: "will this be fixed in 3.5?" has a determinate, citable answer, and so does
"which branch does the fix land on" — a fix goes to the newest branch where the defect exists,
including the future major/minor branches, and is then backported downward (`branch-policy.md`).

## 6.6 Providers: the post-3.0 trap that generates the most confusion

Five shipped providers (`README-PROVIDERS.md`): **default** (built into libcrypto), **legacy**
(MD2, MD4, MDC2, RMD160, CAST5, Blowfish, IDEA, SEED, RC2, RC4, RC5, DES — but *not* 3DES),
**fips**, **base** (non-crypto only, e.g. key serialisation — load this instead of default when
using FIPS), and **null** (empty, built-in, used to guarantee default is never auto-loaded).

The trap: the default provider is auto-loaded **only if no other provider has been loaded yet**. So
an application that explicitly loads `legacy` and nothing else silently loses every default
algorithm. "It worked in 1.1.1 and now this algorithm is missing" is usually one of two things — the
algorithm moved to `legacy` and needs loading, or something loaded a provider explicitly and
suppressed the automatic default.

## 7. Building and testing locally

Reference platform is Linux/gcc; this machine has perl but no C compiler, so builds happen
in Docker (`.claude/memory/lucas/communities/openssl/env/`). Out-of-tree build with the
source mounted read-only, so a build can never dirty the triage clone:

```
perl /src/Configure [--strict-warnings] [no-asm] ...
make -j$(nproc) build_sw
./apps/openssl version -a
perl configdata.pm --dump
```

`SUPPORT.md`'s own triage recipe is worth reusing verbatim when advising a reporter:
search the lists and the tracker first, try the latest source, then rebuild with `no-asm`
and without optimisation flags — those last two isolate an assembly or miscompilation bug
from a library bug, which is a distinction OpenSSL reports genuinely turn on.
