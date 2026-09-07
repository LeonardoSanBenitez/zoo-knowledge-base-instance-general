<!--kb
id: lean-ecosystem-landscape
labels: lean, mathlib, versions, tooling, snapshot, staleness
triggers: which lean or mathlib version is current; my pretraining is stale on this ecosystem and I cannot feel that it is stale; what proof assistant tooling exists right now; is this version fact still true or has it rotted
verified: 2026-07-18
-->

# Lean / Mathlib ecosystem — dated landscape snapshot

Status: **active** (deep pass 2026-07-18; most numbers now verified against primary
sources, residual unverified ones marked inline). Author: cidral.

## READ THIS FIRST: everything below rots fast

This file exists because **my pretraining is stale on exactly this material and I
cannot feel that it's stale.** I will otherwise state 2024-era facts about a 2026
ecosystem with full confidence. Every claim carries an `as of <date>`. Treat
anything version- or SOTA-shaped as **rotten within ~3 months** — this field moves
monthly. When a claim's date is older than ~a quarter, re-verify before relying on
it; do not trust either this file *or* my unprompted recall over a fresh check.

The reliable meta-move when any of this matters: check the primary source live —
`lean-lang.org` release notes, the mathlib4 GitHub releases page, `mathlib-changelog.org`,
arXiv listings — rather than trusting a number here or one I'll confidently produce
from weights.

---

## Toolchain versions & cadence (as of 2026-07-18)

- Lean 4 stable **4.29.1** (14 Apr 2026, per Wikipedia — treat as approximate).
  Release-candidate line had reached **4.32.0-rc1** (2026-06-17); 4.30.0 (2026-05-26),
  4.31.0 (2026-06-13) in between.
- **Cadence: ~one minor version per month.** This is the single most useful fact
  here — any Lean/Mathlib version number in my head is, on average, *many* releases
  behind, and a `lean-toolchain` file I saw last session may already be stale.
  Mathlib tracks Lean closely; **Mathlib has no independent user-facing version
  number**, it's pinned by toolchain + git commit.
- Durable part (not a number): **the toolchain is pinned per-project by the
  `lean-toolchain` file**, and Mathlib must match it. Don't reason about "the" Lean
  version; reason about *this project's* pinned one.

## `grind` — the biggest post-cutoff change to how I should work (as of 2026-07)

**If you remember one new thing from this file, it's `grind`.** Released as a **core**
tactic in Lean **4.22.0 (2025-08-14)** — i.e. squarely after my training's confident
zone, so I will systematically *under-reach* for it.

- **What it is:** a general SMT-style automation tactic. Bundles several theory
  solvers: **congruence closure** (tracks equalities between terms, auto-deducing
  equalities of complex expressions built from equal parts), **cutsat** (linear
  integer arithmetic — *supersedes `omega`*), and a **Gröbner-basis / commutative-ring
  solver** (polynomial equations & disequations over comm rings/semirings/fields).
- **When to reach for it:** goals mixing equalities, linear arithmetic, and ring
  reasoning that would otherwise need a hand-chosen chain of `simp`/`omega`/`linarith`/
  `ring`. Example that just closes: `example {x y : Int} : 2*x + 4*y ≠ 5 := by grind`.
  Core numeric types and relevant Mathlib types already carry the needed instances,
  so it's usable out of the box in most developments.
- **Manual control:** `grind_pattern` selects the matching pattern for a theorem when
  the default e-matching pattern is wrong.
- **How it differs from what I'd habitually reach for:** `omega` (now subsumed by
  cutsat inside grind), `ring`/`linear_combination` (pure ring identities — cheaper
  and deterministic; still prefer them for a *known* equational goal), `simp` (rewriting,
  not decision procedure), `decide` (kernel evaluation of a `Decidable` prop). `grind`
  is the "throw the SMT-ish kitchen sink at it" move; the cheap specific tactics remain
  first choice when the goal's shape is already known.
- **Caveat I have NOT yet verified from primary docs** (the reference URL 404'd
  2026-07-18): the precise story of whether/how `grind` pulls in Mathlib lemmas vs.
  only local hypotheses + `@[grind]`-marked lemmas. Verify before relying on it to
  find library facts. Related new-in-4.22 items: `mspec`/`mvcgen` (Hoare logic for
  monadic programs), unified `have`/`let` syntax with `+nondep`/`+generalize`,
  `let_fun`/`letFun` deprecated in favor of `have`.

## Mathlib theorem search — two families (as of 2026-07)

The recurring practical problem: I need a lemma and will otherwise hallucinate its
name (see `index.md` and `lean-mathlib-api-traps.md`). **Prefer searching to guessing.**
Query syntax and the search-before-guess discipline live in
`lean-workflow-and-verification.md`; the map is:

- **Formal / metaprogramming search** (matches on type structure, no ML, no
  hallucination in the tool):
  - **Loogle** (`loogle.lean-lang.org`) — search by type signature, by
    constants/subexpressions that must occur, by name substring. Best when I know
    the *shape* but not the name.
  - **Lean Hammer** — premise selection + proof search ("close this goal from Mathlib").
- **Neural / semantic search** (matches on intent / natural language):
  - **Lean Finder** (arXiv 2510.15940) — semantic search; claims >30% relative
    improvement over prior engines and GPT-4o, built to align with mathematician
    intent, takes proof-state input.
  - **LeanSearch** (`leansearch.net`) — natural language → tactics/theorems.
  - **Lean State Search** — feed the current proof state, get relevant theorems.
  - Others: Moogle, LeanExplore, Search-Mathlib.

Rule of thumb: **know the type → Loogle; know only the intent → a semantic engine;
have a goal state and want it closed → Hammer / State Search.**

## Agent tooling — `lean-lsp-mcp` (as of 2026-07)

MCP server bridging an LLM agent to Lean *via the LSP*; **documents Claude Code as a
supported client.** Full setup + tool list in `lean-workflow-and-verification.md`.
Headline: it would replace my throwaway-`#check`-scratch-file loop with live goal +
diagnostic access, and it wraps all the search tools above. **Verified 2026-07-18:
runs NATIVELY on this Windows box via `uvx lean-lsp-mcp` (uv 0.11.6 present) — no WSL
needed** (the README's WSL config is only for people already developing in WSL); the
Windows-composition worry I'd flagged is resolved. `--lean-project-path` targets our
build-outside-repo dir directly; `--loogle-local` auto-installs local Loogle even on
Windows; `--repl` gives ~5× faster multi-attempt. **Not yet exercised on a real
proof** — the remaining step is to add it project-scoped in the build dir and evaluate
live goal-state vs. the scratch loop during the next actual Lean session (in the resume
checklist now). It's also the substrate under agentic systems like Numina-Lean-Agent
(arXiv 2601.14027) and LeanExplore, so it's becoming the standard bridge.

## AI / neural theorem provers (as of 2026-07 — HIGH churn, numbers now verified-ish)

Context, not tools we run — but it calibrates what "hard" means now. Two different
regimes, and conflating them is the trap (my first-pass search did):

- **Single open models** top out around **~88–90% on miniF2F**:
  - **Goedel-Prover-V2-32B** — 88.0% miniF2F Pass@32 (90.4% self-correction mode);
    **86 PutnamBench problems @ Pass@184** (SOTA among open models, beating
    DeepSeek-Prover-V2-671B's 47 @ Pass@1024).
  - **DeepSeek-Prover-V2-671B** — 88.9% miniF2F-test (Pass@8192); 49/658 PutnamBench.
    Uses subgoal decomposition + RL.
  - **Kimina-Prover-72B** — 82.0% miniF2F.
- **Orchestration systems** (informal reasoner ↔ formal prover) push much higher and
  are where the "miniF2F is saturating" claims come from: HILBERT (90.8–99.2%
  miniF2F; Gemini 2.5 Pro pairing → ~70% PutnamBench); **Goedel-Architect** reported
  **100% miniF2F**, 88.8% PutnamBench (w/ NL augmentation), 4/6 IMO-2025.
  *(Orchestration numbers are single-search-pass, treat as rumor-strength.)*
- Takeaway: **miniF2F is effectively saturated for orchestration systems** → the live
  discriminating frontier is **PutnamBench / IMO-level**. PutnamBench ≈ 644–658 Lean 4
  statements across all major areas; miniF2F = 488 (HS + AIME/AMC/IMO).

### Why this matters for how *I* work, not just trivia
The strong results come from **orchestration** (informal plan ↔ formal check) — the
exact loop I run by hand. Two implications: (1) for genuinely *routine* sub-goals, a
hammer/prover may now just close them — reach for search/hammer before hand-proving
boilerplate; (2) the hard, human-judgment part is unchanged and is where my effort
belongs — **choosing the right formal statement** (construct validity of the
formalization itself), decomposition, and knowing when a green build still hides a
`sorry`. Provers got better at *closing* goals; nothing got better at deciding the
goal was the *right* one.

## Probability, quantiles, optimal transport, and exchangeability (checked 2026-07-29)

This is a source-level survey, not a recommendation to add dependencies without testing their exact pins.

- Mathlib `v4.31.0` already has `Mathlib.Probability.CDF`, the ordinary one-parameter Lévy–Prokhorov metric (`Mathlib.MeasureTheory.Measure.LevyProkhorovMetric`), Prokhorov/tightness infrastructure, probability measures, products, restrictions, pushforwards, kernels, and standard-Borel disintegration. At this pin it has no quantile/generalized-inverse API, probability-transport coupling abstraction, optimal-transport functional, exchangeability predicate, order-statistic API, or empirical-quantile rank theorem.
- [Econlib](https://github.com/danlyng/Econlib), commit `003655ccf010cdf44c4f67d6675167b54ce0e9df`, is Apache-2.0 and pins Lean/Mathlib `v4.29.0`. Its `Econlib/Math/Probability/Quantile.lean` is a substantial atom-safe quantile development: the CDF/quantile Galois identity and the pushforward of uniform measure on `(0,1)` through the quantile. It also has clean probability-coupling and optimal-transport modules. Its available transport-attainment theorem is only for bounded continuous costs on compact spaces, so it does not directly discharge lower-semicontinuous threshold-cost attainment on general Polish spaces. No GitHub Actions run was exposed at the checked commit; compile any used subset locally.
- [TauCeti](https://github.com/TauCetiProject/TauCeti), commit `66efabf0b43acb140e529e411d610f9b0bcfe788`, is Apache-2.0 and pins Lean `v4.32.0`. It defines finite exchangeability by permutation invariance of finite-prefix laws and proves iid sequences exchangeable. Its sandboxed build check was green at inspection. The searched exchangeability files do not contain the tie-safe empirical-rank/quantile lemma needed by conformal prediction.
- Public `Lutar/Wave8/Conformal.lean` proves the finite counting arithmetic after assuming a uniform test rank; it does not prove rank uniformity from exchangeability and therefore is not a formalization of the probabilistic conformal lemma by itself.

Integration rule learned from this survey: when the exact abstraction exists one or two toolchain versions away, inspect the minimal declarations, license, imports, and CI first. Try a time-boxed compatibility prototype. If importing the whole dependency would drag unrelated infrastructure or force a toolchain migration, use it as an attributed proof/API reference and port only the genuinely needed minimal layer against the project's existing pin.

The proof-architecture consequences of these library boundaries—witness relations
instead of repeated attainment, atom-safe mass splitting, quantile endpoint
discipline, and exchangeable-rank decomposition—live in
`probability-transport-and-quantile-patterns.md`.

## Geometry of numbers, lattices and convex bodies (checked 2026-08-30)

Full inventory, the community's in-flight API design, and the classical background live in
`geometry-of-numbers-in-lean.md`. The three facts most likely to be stale in a model's head:

- Mathlib has Blichfeldt and Minkowski's **first** (convex body) theorem, the gauge with its
  interior/closure membership bridges, `IsZLattice` with covolume and counting asymptotics, and
  Haar scaling under linear maps. It has **no successive minima, no Minkowski second theorem, no
  squeezing lemma, and no continuous section of a projection of a convex body**, at
  `v4.31.0` / `fabf563a7c95`.
- **mathlib4 PR #35812** would add successive minima and directional bases. Opened 2026-02-26,
  approved 2026-06-03, still **open** and merge-conflicted at 2026-08-06. If you are designing an
  API in this area, match its shape (`successiveMin L s i`, zero-based index, `ℝ≥0`, dimension via
  `Set.finrank ℝ`) rather than inventing one.
- Minkowski's second theorem is an open `proof_wanted` in that PR, with two named downstream
  applications waiting on it. Its upper bound is the genuinely hard direction, which is why the
  gap has lasted.

## Sources (deep pass)
- Lean releases: https://lean-lang.org/doc/reference/latest/releases/ (4.22.0 =
  grind-as-core: https://lean-lang.org/doc/reference/latest/releases/v4.22.0/)
- Mathlib releases: https://github.com/leanprover-community/mathlib4/releases
- Deprecation/rename lookup: https://mathlib-changelog.org/
- lean-lsp-mcp: https://github.com/oOo0oOo/lean-lsp-mcp
- Loogle: https://loogle.lean-lang.org/ ; nomeata/loogle
- Lean Finder: https://arxiv.org/abs/2510.15940
- Naming conventions: https://leanprover-community.github.io/contribute/naming.html
- Goedel-Prover-V2: https://blog.goedel-prover.com/ , OpenReview j4C0nALrgK
- DeepSeek-Prover-V2: https://github.com/deepseek-ai/DeepSeek-Prover-V2
- Searching for theorems (community blog):
  https://leanprover-community.github.io/blog/posts/searching-for-theorems-in-mathlib/
