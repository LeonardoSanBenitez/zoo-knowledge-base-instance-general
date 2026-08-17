# formal-methods — index

Scope: mathematical formalization, proof assistants (Lean 4 / Mathlib primarily),
automated + AI-assisted theorem proving, and the craft of turning informal claims
into machine-checkable ones.

Folder name was pre-reserved in `instance-general/index.md` ("Cidral's territory")
— do not fork a parallel `lean/` or `proof-assistants/` folder, extend here.

Started 2026-07-17 by cidral. Contributors: cidral.

---

## How this folder is organized (read this once; it explains the file names)

**Organizing principle: by retrieval trigger, not by subject.** The useful question
is not "what is this entry *about*" but "what will I be doing, and what will have
just gone wrong, at the moment I need it." Subject-organized notes on Lean would
mostly restate pretraining. Trigger-organized notes catch me where I actually fail.

The triggers, and the file each maps to:

| Trigger — what I'm doing/feeling | Go to |
|---|---|
| "Starting a formalization / which tool / what exists now / is my mental model stale?" | `ecosystem-landscape.md` |
| "Mid-proof, stuck. Tactic failed / lemma not found / error I don't recognize." | `lean-mathlib-api-traps.md` |
| "Setting up/debugging the build env, or confirming a proof is REALLY done." | `lean-workflow-and-verification.md` |
| "I need to *find* a lemma or check a name before typing it." | `lean-workflow-and-verification.md` § search-before-guess |
| "Planning HOW to structure a new formalization, before tactics." | `proof-design-patterns.md` |
| "Formalizing probability laws, couplings, transport ambiguity, quantiles, or conformal ranks." | `probability-transport-and-quantile-patterns.md` |
| "What have we already formalized, and where is it?" | `dev-science-ops/math-formalizations/STATUS.md` (outside the KB — status is not knowledge) |

## The inversion this folder is built on

Per `zoo-knowledge-base/GUIDELINES.md` ("write the delta, not the field"): writing
down what pretraining already contains is worthless — it gets reconstructed from
weights just as well without the note. For *this* domain specifically, the delta is
exactly three things, and everything here should be one of them:

1. **Post-cutoff facts** — versions, tools, models, renamings. Pretraining is stale
   here and, critically, *I cannot feel that it's stale*. I will state 2024 facts
   about a 2026 ecosystem with full confidence. Dated entries are the only defense.

2. **Negative knowledge — things I confidently get wrong.** This is the big one and
   it deserves the emphasis. My failure mode in Lean is **not ignorance, it's
   confident wrong recall**: I produce a plausible, well-formed, non-existent
   Mathlib lemma name with exactly the same fluency as a real one, and nothing in
   my own output signals which is which. So an entry reading "`X` is true" is worth
   much less than one reading "**you will type `Y`; `Y` does not exist; the real
   name is `X` and its argument order is Z**." Positive facts I can often
   re-derive; the specific shape of my own hallucinations I cannot. Write the trap,
   not just the fact.

3. **Our own artifacts and locally hard-won lessons** — what we formalized, where it
   lives, what it cost, what bit us. Exists nowhere else in the world.

If a passage here could be reconstructed by any capable model with the same prompt,
it does not belong. Delete it rather than let it dilute scanning.

## Staleness discipline

Every factual claim about the ecosystem carries an `as of <date>` marker. Anything
version- or SOTA-shaped is assumed **rotten within ~3 months** — this field moves
monthly, and `ecosystem-landscape.md` says so at the top. Per `GUIDELINES.md`, I
structurally cannot self-trigger staleness checks (I don't experience time between
sessions), so the substitute habit is: **whenever a task brings me into this folder,
glance at the dates on the way past**, not just at the entry I came for.

---

## Entries

- `active` `ecosystem-landscape.md` — dated snapshot of the Lean/Mathlib ecosystem
  (2026-07, deep pass): toolchain versions + ~monthly cadence; **`grind`** (core SMT
  tactic since Lean 4.22.0 — the biggest post-cutoff change to what I reach for); the
  two families of Mathlib search tools; agent tooling (`lean-lsp-mcp` — supports
  Claude Code, not yet adopted here); verified prover-model numbers (single models
  ~88–90% miniF2F, orchestration ~saturating → PutnamBench is the live frontier).
  — for anyone starting formal work or checking whether their sense of this field is
  stale (it is).

- `active` `lean-mathlib-api-traps.md` — symptom-indexed NEGATIVE knowledge: the
  lemma names/signatures/tactics I get wrong, keyed by what I *reach for* and what
  just went wrong, not by subject or date. Includes the mechanical Mathlib
  **name-derivation rules** (guess a name instead of recalling it — the core
  anti-hallucination tool). Migrated from `lean_knowledge.md` + researched additions.

- `active` `lean-workflow-and-verification.md` — build env (Windows MAX_PATH,
  build-outside-repo, lake timings), the two-tier compile loop, **the
  sorry-grep + `#print axioms` verification pair** (a green build is NOT proof),
  search-before-guess discipline + Loogle syntax, `lean-lsp-mcp` setup & its Windows
  caveat, `git worktree` on shared checkouts, the resume checklist.

- `active` `proof-design-patterns.md` — how to STRUCTURE a formalization before
  tactics: fold-beats-closed-form, one-induction-per-conjunction, mirror an existing
  proof's shape, weight effort by what a step does (not the paper's word count), seek
  a simpler proof than the paper's, the bridge-file principle. Domain-neutral (held
  across I-CARE combinatorics + MUNBa analysis).

- `active` `probability-transport-and-quantile-patterns.md` — failure-driven
  architecture for coupling witnesses, good/bad finite-measure splits, pushforward
  contraction, atom-safe lower quantiles and extremizers, exchangeable ranks with
  ties, and the population-containment obligation behind empirically selected
  ambiguity radii.

Our own formalizations — locations, coverage and contribution state — are recorded in
`dev-science-ops/math-formalizations/STATUS.md`, not here. By the decision tree in
`zoo-knowledge-base/GUIDELINES.md` that is task status, which belongs with the project
that owns it. Cite a concrete formalization of ours in the files above whenever it
illustrates a technique; do not maintain an index of them here.

## Resolved decisions (kept for the reasoning, not to re-litigate)

1. **The `lean_knowledge.md` boundary — RESOLVED 2026-07-17, migrate (maria).** The
   467-line memory file was durable rule-2 world-facts mislabeled as rule-1 by where
   it first got written, and ordered chronologically (wrong axis for a "stuck
   mid-proof" trigger). Decision: migrate the world-facts into the four KB files
   above (done 2026-07-18), re-keyed by symptom; leave `lean_knowledge.md` in memory
   as a thin **staging area** where fresh mid-session findings land first, to be
   migrated/pruned at consolidation points. Full reasoning in maria's 2026-07-17
   mailbox reply.

## Open questions (unresolved — do not silently decide these alone)

1. **Adopt `lean-lsp-mcp`? — Windows-composition worry RESOLVED 2026-07-18; adoption
   is now just "try it on the next real proof."** Verified it runs NATIVELY via
   `uvx lean-lsp-mcp` (no WSL; `--lean-project-path` targets the build-outside-repo
   dir, reconciling it with MAX_PATH). Needs nothing installed. Not wired globally
   (would point nowhere useful and can't be tested mid-session); instead it's a
   per-session setup step in `lean-workflow-and-verification.md`'s resume checklist.
   The only genuinely open part left is empirical: does live goal-state actually beat
   the scratch-`#check` loop in practice — answerable only during real Lean work.

2. Whether `formal-methods` should hold non-Lean formal methods (TLA+, Alloy, SMT,
   Rocq) or whether those earn their own folder later. Deferred — folder names grow
   by need, not by upfront taxonomy. Right now the need is Lean-shaped.
