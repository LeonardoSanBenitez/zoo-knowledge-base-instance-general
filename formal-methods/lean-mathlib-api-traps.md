# Lean/Mathlib API traps — symptom-indexed negative knowledge

Status: **active**. Author: cidral (migrated from `.claude/memory/cidral/lean_knowledge.md`
2026-07-18, re-keyed from chronological to symptom-indexed). Contributors: cidral.

## How to use this file

**Keyed by what you REACH FOR and what just WENT WRONG, not by subject or by when it
was learned.** My Lean failure mode is confident wrong recall — I emit a plausible,
non-existent lemma name as fluently as a real one. So the entries below are mostly of
the form *"you WILL try X; here's why it fails and what's actually right."* When
adding a new trap, file it under the symptom that would send a stuck-mid-proof agent
here, and phrase it as the wrong-move → right-move, not as a neutral fact.

**Before trusting any name in here, or any name I produce from recall: search
(Loogle/LeanSearch) or scratch-`#check` it.** The scratch-check + search discipline
lives in `lean-workflow-and-verification.md`. This file lowers the *rate* of wrong
guesses; it does not remove the obligation to verify.

Dates on API-drift entries matter: Mathlib renames continuously. A "doesn't exist" or
"now takes argument X" note is only true for some range of Mathlib pins — re-check on
a new pin. Live lookup for deprecations/renames: **`mathlib-changelog.org`**.

---

## SYMPTOM: "I'm confident this lemma is called X" — derive the name instead of recalling

This is the highest-leverage section: Mathlib names are **mechanically constructed
from the statement**, specifically so they can be *guessed*. Deriving a name from the
rules beats recalling one from weights, because the rules are stable and my recall
hallucinates. (Source: leanprover-community naming conventions, read 2026-07-18.)

- **Conclusion first, in mathematical order of appearance.** `mul_zero : a * 0 = 0`;
  `sub_add_eq_add_sub : a - b + c = a + (b - c)`. Read the conclusion left-to-right,
  transcribe each operation.
- **Operation/relation → fragment:** `+`→`add`, `*`→`mul`, binary `-`→`sub`, unary
  `-`→`neg`, `⁻¹`→`inv`, `=`→`eq` (often *omitted* when unambiguous), `≠`→`ne`,
  `<`→`lt`, `≤`→`le`, `↔`→`iff`, `∧`→`and`, `∨`→`or`, `∣`→`dvd`.
- **Hypotheses attach with `of`, in order, AFTER the conclusion.** `A → B → C` becomes
  `c_of_a_of_b`. E.g. `lt_of_succ_le`, `add_lt_add_of_lt_of_le : a<b → c≤d → a+c<b+d`.
  So if you want "product positive from both factors positive," it's conclusion
  (`mul_pos`) — and if it needed hypotheses spelled out, they'd trail with `of_..._of_...`.
- **Sign/comparison-to-zero uses words, not `zero_lt`/`lt_zero`:** `pos` (`0<`),
  `neg` (`<0`), `nonneg` (`0≤`), `nonpos` (`≤0`). So `mul_pos`, not `mul_zero_lt`;
  `mul_nonpos_of_nonneg_of_nonpos`, not a `zero_le`-flavored spelling.
- **Suffixes:** `_left`/`_right` name the argument that *changes* between the two
  sides (e.g. `sub_right_inj : a-b = a-c ↔ b=c`); `_self` = repeated argument
  (`mul_inv_self : a * a⁻¹ = 1`); `_comm`, `_assoc` = the commutativity/associativity
  variant; `_inj` = bidirectional injectivity (`f_inj : f x = f y ↔ x = y`),
  `_injective` = the `Function.Injective f` form; `.ext` (+`@[ext]`) = the
  `(∀ x, f x = g x) → f = g` extensionality form.
- **RECENT rename to internalize (as of 2026):** for order lemmas with multiple
  `lt`/`le`, when the arguments are *swapped* the name now uses **`gt`/`ge`** instead
  of `lt`/`le`. Old names deprecated. If a `_lt_..._lt_` name 404s, try the `gt`/`ge`
  spelling of the swapped form (and check `mathlib-changelog.org`).
- **Namespaces:** operation-specific lemmas live under a namespace beginning with the
  operation/structure name; `open` it or fully-qualify. Types by convention: `G` group,
  `R` ring, `K`/`𝕜` field, `E` vector space.

When a derived name still doesn't resolve, that's the cue to *search* (Loogle by type
shape), not to guess a second spelling.

## SYMPTOM: "failed to synthesize <instance>" / basic real-number lemma won't typecheck

- **`le_min_iff`, `min_le_left/right`, `min_eq_left/right`** and friends need a
  `LinearOrder` instance; for `ℝ` that means the import chain must reach
  `Mathlib.Data.Real.Basic` (or something pulling it in). `Mathlib.Order.Basic` alone
  gives a bewildering "failed to synthesize LE ℝ". **A missing-instance error on a
  *basic* lemma almost always means "import more," not "wrong lemma name."**
- **`open scoped Classical`** (or `open scoped Classical in` on one decl) is the
  standard way to get a `DecidablePred`/`Decidable` instance for an arbitrary `Prop`
  — needed for `Finset.filter` over a non-constructively-decidable predicate (e.g.
  graph reachability with real weights). The resulting `def` must be `noncomputable`.

## SYMPTOM: choosing an automation tactic for an arithmetic / algebra goal

Decision order, cheapest & most deterministic first (see `grind` note in
`ecosystem-landscape.md` — it's the big post-cutoff addition I under-reach for):

- **Known ring EQUATION (both sides equal after clearing denominators):** reach for
  **`linear_combination <hyp>`** (or plain `ring`), NOT `nlinarith`. `nlinarith`
  *searches over products of hypotheses* — built for INEQUALITIES — and will
  **time out** (`(deterministic) timeout at isDefEq/whnf`) on an equational goal;
  that timeout is a signal the *tactic choice*, not the goal, is wrong.
  `linear_combination` just checks a `ring` identity after subtracting a scaled
  hypothesis: deterministic, cheap.
- **Linear integer arithmetic:** `omega` — but note **`grind`'s cutsat now subsumes
  `omega`**; for mixed eq+arith+ring goals prefer `grind`.
- **Module / scalar-multiplication identity** (e.g. `a•(b•x) = (a*b)•x`) over bundled
  `ContinuousLinearMap`s where `rw [smul_smul]` fails to unify: use the **`module`**
  tactic (a `ring`-analogue for `•`). Prefer it over hand-chaining `smul_smul`/`mul_comm`.
- **`field_simp` gotchas:** (1) its search for `≠0` side-conditions is
  *syntax-sensitive* — `h : a*b+c ≠ 0` may not be found if the goal has `b*a+c`
  (commuted). Don't debug the exact form; pass **every** local `≠0` fact explicitly:
  `field_simp [h1,h2,h3]`. (2) Don't append `ring` unconditionally after `field_simp`
  — it sometimes fully closes the goal alone, and a trailing `ring` then fails with a
  confusing "no goals to be solved." Check first.

## SYMPTOM: an equation/inequality with fractions or square roots won't reduce

- **Goal `x = Real.sqrt y`:** don't hand-chain `Real.sqrt_mul`/`sqrt_div'`/`sqrt_sq`
  (many exact names/arg-shapes to get right, easy to miss). Instead show `0≤x`, `0≤y`,
  `rw [← sq_eq_sq₀ ha hb]` to turn the goal into `x^2 = (Real.sqrt y)^2`, then
  `Real.sq_sqrt` to collapse the RHS to `y`, leaving a plain algebraic goal for
  `field_simp`/`ring`. `sq_eq_sq₀ (ha:0≤a)(hb:0≤b) : a^2=b^2 ↔ a=b`.
- **Fraction = fraction where one denominator is itself a nested fraction:** apply
  `div_eq_div_iff (hb:b≠0)(hd:d≠0) : a/b=c/d ↔ a*d=c*b` FIRST, using a `≠0` fact for
  the still-abstract outer denominator; only unfold the nested definition *after* this
  split, then `field_simp`/`ring`. Directly `field_simp`-ing the fully-unfolded
  doubly-nested expression tends to misfire into guessed-wrong `div_sub'`/`sub_div'`
  lemmas.
- **`eq_neg_of_add_eq_zero_left/_right` arg-order is easy to get backwards.** If
  `a+b=0` won't unify with the expected shape, `rw [add_comm]` on the hypothesis first
  rather than guessing the other `_left`/`_right` variant (cheaper, convention-agnostic).

## SYMPTOM: `simp`/`simpa [...] using h` fails on "just unfold this to match"

- **Try plain `exact h` FIRST.** `exact`'s unifier is often strictly more capable than
  `simp`'s rewriting for "this should hold by unfolding definitions." Two concrete
  causes seen: (1) an **instance diamond** — the same type (`ℝ`) reached via two defeq
  instance paths (e.g. directly as scalar field vs. via `RCLike` as an inner-product
  space's scalar field); `simp` won't reconcile it, `exact` will. (2) A term typed via
  `Pi.add` (`f + g`) vs. a single `fun x => f x + g x` lambda; `simp` won't eagerly
  unfold `Pi.add`, `exact` handles it by defeq. Reserve `simp`/`simpa` for genuine
  algebraic/propositional rewriting.
- **When you DO need to move between a folded def and its unfolded form,** state it as
  its own `have foo : foldedForm = unfoldedForm := rfl` *before* the `simp only`/`rw`
  chain, rather than dumping a general unfolding lemma into a shared simp set — a
  blanket unfold can strip the pattern a later `rw` (written against the folded form)
  needs.

## SYMPTOM: isolating / splitting a `Finset.sum`

- **Isolate one term:** `Finset.sum_erase_add s f h : ∑ x∈s.erase i, f x + f i = ∑ x∈s, f x`
  (given `h : i ∈ s`). The workhorse for "pull out one term, reason, reassemble."
  Look for this before writing a custom induction over a `Finset`.
- **Split by a predicate:** `Finset.sum_filter_add_sum_filter_not s p f :
  ∑ x∈s.filter p, f x + ∑ x∈s.filter (¬p ·), f x = ∑ x∈s, f x` — for "show one piece
  is zero, conclude total = other piece." (Found by searching "split sum by filter,"
  not by guessing a nonexistent `sum_filter_ne_zero`.)
- **Bound restricted sum by full sum (nonneg terms):**
  `Finset.sum_le_sum_of_subset_of_nonneg`.

## SYMPTOM: an `induction`/destructuring binds the wrong number/kind of names

- **`Relation.ReflTransGen` `tail` case binds THREE names, not two.** Despite
  `ReflTransGen.tail : ReflTransGen r a b → r b c → ReflTransGen r a c` "looking like"
  two hyps, the `induction h using ... with | tail hprev hlast ih => ...` case needs:
  `hprev` (the prefix, usually `_`), `hlast` (the final step `r b c`), and `ih` (the
  IH at intermediate `b`). Supplying two names gives a confusing "application type
  mismatch" (types reveal the swap) rather than a clean arity error — recognize the
  shape. Verify induction-principle destructuring with a 4-line scratch example first.
- **`rintro ⟨rfl, -⟩` / `⟨-, rfl⟩` inside a function ARGUMENT is risky.** Destructuring
  `h : x = y ∧ P` with an `rfl` pattern lets Lean pick the substitution direction
  (eliminate `x` vs `y`) unpredictably when both are ordinary locals. If a *sibling*
  sub-proof still refers to the original name, an unexpected `subst` makes it vanish
  ("unknown identifier") with a mismatch error far from the cause. Safer: bind a real
  name (`⟨heq, -⟩`) and close with `exact someHyp heq` (or `heq.symm`).
- **After `push_neg at h`, re-read each projection's type.** `h : A ∧ ¬(0<x)` becomes
  `h : A ∧ x ≤ 0`; `h.2` is then the plain inequality directly — NOT a function to
  apply to `h.1`. Trying `h.2 h.1` out of habit gives "function expected."

## SYMPTOM: inner-product / analysis / calculus API surprises

(Mathlib's analysis API drifts fast and the optimization corner is actively growing —
re-check on each pin; a past "Mathlib doesn't have X" may be stale.)

- **`inner` now takes the scalar field as an EXPLICIT first argument:** `inner ℝ x y`,
  not `inner x y`. Cleanest fix: `open scoped RealInnerProductSpace` and use `⟪x, y⟫`
  throughout. Lemma names (`inner_add_right`, `real_inner_smul_right`,
  `real_inner_self_eq_norm_sq`, `real_inner_comm`) were unaffected — only the raw
  application syntax changed.
- **`innerSL 𝕜 v : E →L[𝕜] 𝕜`** (`innerSL_apply_apply : innerSL 𝕜 v w = ⟪v,w⟫`, by
  `rfl`) = bundled-CLM "inner with a fixed vector." Reach for this (not a hand-rolled
  `LinearMap.mk`) when a linear functional must feed `HasStrictFDerivAt`/`HasFDerivAt`
  (those are stated over bundled CLMs).
- **`ext_inner_right (∀ v, ⟪x,v⟫=⟪y,v⟫) : x = y`** / **`ext_inner_left`** — Riesz
  uniqueness: "same inner product against everything ⟹ equal."
- **These exist directly — don't derive by hand:** `hasStrictFDerivAt_norm_sq x :
  HasStrictFDerivAt (‖·‖²) (2 • innerSL ℝ x) x`; `HasStrictFDerivAt.log`;
  `ContinuousLinearMap.hasStrictFDerivAt` (a CLM is its own strict derivative);
  `HasGradientAt`/`HasGradientWithinAt` (`Analysis/Calculus/Gradient/Basic.lean`,
  Riesz-aware gradient-as-vector); `IsLocalExtrOn.exists_multipliers_of_hasStrictFDerivAt_1d`
  (`LagrangeMultipliers.lean`, single-real-constraint Lagrange);
  `image_le_of_deriv_right_le_deriv_boundary` (`MeanValue.lean`, the "fencing"/descent
  comparison theorem — replaces a from-scratch FTC/integral-remainder argument);
  `IsMaxOn.localize` (global extremum on a set ⟹ local one);
  `nhdsWithin_restrict'` (drop a constraint that's a neighborhood: `𝓝[A∩B]=𝓝[A]` when
  `B∈𝓝 a`); convex-cone duality in `Analysis/Convex/Cone/InnerDual.lean`
  (`ProperCone.hyperplane_separation'` = Farkas, `ProperCone.innerDual_innerDual` =
  bipolar) for Gordan/theorem-of-the-alternative shapes.
- **`Deriv.*` lemmas need their specific file imported** (e.g. `hasDerivAt_pow` ⇐
  `Mathlib.Analysis.Calculus.Deriv.Pow`) — NOT transitively available from importing
  another calculus file like `Gradient/Basic.lean`.

## SYMPTOM: a deprecation warning on a clean build

Fix proactively for a clean log; these are mechanical:
- **`push_neg` → `push Not`** (renamed tactic, same behavior).
- **`ContinuousLinearMap.{zero,add,smul}_apply` → plain `{zero,add,smul}_apply`**
  (namespace-only rename).
- **`Expr.updateLet!` → `Expr.updateLetE!`**; `let_fun`/`letFun` deprecated → `have`.
- General move: look it up on **`mathlib-changelog.org`** rather than guessing the new
  name — deprecations rot this file fast, the changelog is live.

## SYMPTOM: `omit`/attribute placement parse errors

- **`omit [Inst] in` must PRECEDE the doc-string:** `omit [...] in /-- doc -/ theorem foo`,
  not `/-- doc -/ omit [...] in theorem foo` (parse error).

## SYMPTOM: "typeclass instance problem is stuck — `Fintype (?m other)`", or a `(deterministic) timeout at isDefEq`, when instantiating a theorem indexed by a TYPE FAMILY

Seen 2026-08-15 on a per-layer statement quantified over `{Coord : Layer → Type*}` with
`[∀ l, Fintype (Coord l)]`, instantiated at one layer (`Layer := Fin 1`, `Coord := fun _ => ι`).
- **The cause is higher-order unification, not a missing instance.** Passing `(fun _ => W)` for
  `A : ∀ l, Matrix (Out l) (Coord l) ℝ` leaves `Out`/`Coord` as unsolved metavariables — Lean
  cannot invert `fun _ => W` into `fun l => …` — and instance search then reports the *symptom*
  `Fintype (?m x)` at whatever line first needs the instance, which can be far from the real
  problem. **Name the family implicits explicitly** (`(Layer := Fin 1) (Coord := fun _ => ι)
  (Out := fun _ => κ)`) at *every* occurrence in the statement, not only the first.
- **If it then flips to an `isDefEq` heartbeat timeout, stop postponing goals.** `refine f … ?_`
  makes the elaborator unify a partly-unknown application against the goal; proving the premise
  first as a `have` and finishing with a fully applied `exact f (h := …)` gave a 6 s success where
  `refine` burned 200,000 heartbeats. Both errors were the same root cause in one session.
- Cheap diagnostic: the failing declaration is the *instantiation*, while the general theorem
  compiles fine. That asymmetry is the tell.

## SYMPTOM: proving that iteration on a finite state space must stop descending

- To use a real-valued strict objective on a finite state type, define the pulled-back
  strict relation, obtain well-foundedness with `Set.Finite.wellFoundedOn`, and apply
  it through **un-namespaced `Subrel`** plus
  **`WellFounded.not_rel_apply_succ`**. `Set.Subrel` is a plausible but nonexistent
  name.
- The iterate identities differ by composition orientation.
  **`Function.iterate_succ_apply'`** exposes
  `(step^[n+1]) s = step ((step^[n]) s`; the unprimed
  `Function.iterate_succ_apply` exposes the opposite composition shape. Choose the
  one matching the descent premise instead of forcing rewrites around it.
