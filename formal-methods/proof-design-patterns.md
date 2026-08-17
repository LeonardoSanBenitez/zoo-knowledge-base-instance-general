# Proof design patterns — structuring a formalization before touching tactics

Status: **active**. Author: cidral (migrated from `.claude/memory/cidral/lean_knowledge.md`
2026-07-18). Contributors: cidral.

Trigger for this file: **"planning HOW to structure a new formalization, before
writing tactics."** These are strategy/architecture lessons — bigger than any one API
name (those are in `lean-mathlib-api-traps.md`) and independent of the build
environment (`lean-workflow-and-verification.md`). Domain-neutral: they've held across
graph-flow combinatorics (I-CARE) and continuous optimization / real analysis (MUNBa).

---

## Definition shape: recursion/fold beats closed-form-with-side-lemmas

**A recursive/inductive construction aligns with Lean's `induction` tactic far better
than an equivalent closed-form definition with explicit combinatorial side-conditions.**
Concrete case: a "push δ along a chain" construction, first written as a single
closed-form update formula (`f' x y := f x y + (if isStep x y then δ else 0) - ...`),
is mathematically clean but needs SEPARATE non-trivial lemmas up front ("every vertex
in a `Nodup` list has at most one predecessor/successor") before you can even state
what happens at each vertex. Recast as an edge-by-edge **fold** (`stepEdge` for one
edge, `augmentAlong` recursing down the chain), the same content becomes a bundled
induction where each step touches only two entries, and the "only one
predecessor/successor" fact falls out of the recursion's structure *for free*.

**Heuristic:** when a closed-form definition needs an uncomfortable side-lemma just to
state its own correctness, try recasting it as a fold/recursion first — it very likely
routes around exactly that side-lemma. And do NOT over-commit to a "precise design"
written before touching the compiler: treat any pre-written formula as a *hypothesis
to test against `lake env lean`*, not a spec to defend.

## Bundle related facts into ONE conjunction proved by ONE induction

Rather than several separate inductions over the same recursive structure (which
re-derive the same case split repeatedly and risk the branches drifting out of sync),
prove a conjunction of all the related facts in a single induction. Used twice:
`shortcut_spec` (five properties of a loop-cutting function, one induction),
`augmentAlong_cons_spec` (feasibility + three net-flow-delta facts, one induction).

## Mirror an existing proof's shape when the argument is structurally the same

When a new goal's mathematical argument is structurally identical to one already
proved, deliberately mirror that proof's shape rather than re-deriving from scratch —
e.g. a "reachable set is a cut; every positive crossing edge is constrained" pattern
transfers almost verbatim to a "blocking set → cut" argument, swapping only the
underlying relation. But: **a symmetric statement does NOT guarantee its two branches
close with identical tactic sequences.** `field_simp` fully closed one branch of a
symmetric feasibility argument but left a trivial `add_comm`-shaped residual in the
mirror branch (the symmetric lemma applied "the other way" changed term order). Don't
copy-paste-and-assume; check each branch.

## Effort estimation: weight by what the step DOES, not by the paper's word count

**A paper's one-sentence proof step is often the hardest part to formalize, and vice
versa.** "One may push δ units along [an augmenting path]... producing a feasible flow
of strictly larger value" — one sentence, no proof in the paper — became the largest,
hardest file in the whole formalization (~280 lines). Conversely, a step the paper
spelled out in detail (a weak-duality sum manipulation) was short to mechanize. When
estimating a new task, weight by "how much is this step actually doing," not by how
many words the paper spends on it.

## Source route first; simpler proofs are supplemental until bridged

Re-deriving a result can reveal a shorter argument, but a paper formalization is not
merely a theorem-proving exercise. First state the paper's objects and intermediate
claims in its notation, mechanize every valid source step, and localize any invalid
step as the narrowest additional hypothesis that makes it sound. Continue
conditionally to the paper's conclusion. A generic theorem about arbitrary states,
potentials, minimizers, or convergence does not cover a paper-specific item when the
bridge back to the paper's definitions is absent.

Only after that source-route bridge exists should a simpler or stronger derivation be
added. If equivalence is not proved, give it a separate name and describe it as a
supplemental result. This preserves the useful lesson from MUNBa—re-deriving the
starting equations bypassed two unnecessary case splits—without repeating the
KNN–Gini Proposition 4 failure, where a valid abstract termination theorem initially
replaced rather than formalized the authors' fixed-rank centroid argument.

Mechanical sequence when a source step looks wrong:

1. Preserve the source notation and all valid preceding equations.
2. Derive the exact missing equation or side condition.
3. Insert it at the source's point of use and disclose it in the catalog.
4. Prove the source conclusion conditionally.
5. Keep counterexamples and alternative routes separate.
6. Ask the authors whether the interpretation or an unstated property supplies the
   missing condition.

## Sequencing within a proof: shape first, supporting pieces second

- **Sketch a `calc` chain's steps (even as placeholder `sorry`s) before writing its
  supporting `have`s**, not the reverse. A helper written speculatively, before the
  calc block's exact shape is fixed, tends not to fit and gets abandoned as dead code.
  Same root cause as "fold beats closed-form-with-side-lemmas," at smaller scale:
  commit to a proof's shape before writing its supporting pieces.
- **"This feels obvious" is not a reliable signal that a tactic's exact output is safe
  to assume** — especially `simp`/`push_neg`/`norm_num`-family tactics that rewrite
  hypotheses in place. The one real compile error of one session came from skipping the
  scratch-check on something that felt too small to bother with (`push_neg`'s effect
  on a conjunction's second projection), not from a hard API-name guess. When unsure
  whether something is "small enough to skip," it usually isn't — the scratch check
  costs one throwaway file either way.

## Search the library for the exact tool before writing math from scratch

Before reaching for heavy machinery (`intervalIntegral`, a from-scratch tangent-curve
construction, hand-rolled convex-cone duality), check whether Mathlib already packages
exactly the pattern:
- an inequality "proved by integrating a derivative bound" → look in `MeanValue.lean`
  for a comparison/fencing theorem (`image_le_of_deriv_right_le_deriv_boundary`) before
  setting up a Bochner integral.
- a "first-order necessary condition on a level set" → `LagrangeMultipliers.lean`.
- a "theorem of the alternative"/Gordan/Farkas shape → `Convex/Cone/InnerDual.lean`.

Two attached meta-lessons: (1) **a "no existing formalization of [named notion]"
finding from a PRIOR session does not mean the math needs new research** — often the
classical fact is just packaged under a different, un-searched-for name; check the
library for the STRIPPED-DOWN classical version of what the paper really invokes.
(2) For a genuinely SMALL fixed instance (e.g. exactly 2 vectors), proving the needed
case DIRECTLY and constructively (e.g. solving a 2×2 Gram system by Cramer's rule) is
often simpler and more legible than instantiating the general machinery — worth it
when only the small case is needed, at the cost of non-reusability.

## The bridge-file principle (deliverable shape when specializing a library result)

When a target result already exists in a library in general form, the deliverable is
NOT a terse one-line `exact`/`apply` dispatch. It's a file that (1) restates the SOURCE
PAPER's own notation and hypotheses explicitly, (2) states the result in that notation,
(3) proves it by *visibly instantiating* the library fact, with the file's docstring
naming exactly which library theorem(s) are specialized and why. The goal is not "Lean
that compiles" but mechanically-checked confidence in the PAPER's specific claim,
readable by someone checking the paper against the file line by line. (Explicit user
instruction 2026-07-16; also in cidral.md's Lessons Learned.)

## State hand-derived numeric predictions as targets BEFORE proving

If a hand derivation predicts a specific value (e.g. "the normalization is exact only
at ball radius ε=√2, forcing the Lagrange multiplier to equal exactly 1"), write that
target down BEFORE the Lean proof, then check the compiler independently reaches it. It
did (the proof derived μ=1 from first principles) — turning "we hand-checked this
twice" into "the compiler independently confirmed it," a strictly stronger claim, and
the whole reason for formalizing.
