<!--kb
id: geometry-of-numbers-in-lean
labels: lean, mathlib, geometry-of-numbers, lattices, convex-bodies, successive-minima, minkowski, haar-measure, gauge
triggers: I am about to formalize something about lattices and convex bodies; does Mathlib have successive minima; is Minkowski's second theorem in Mathlib; what is in Mathlib's geometry of numbers file; how do I state a successive minimum in Lean; is there a Lean squeezing lemma; who in the Lean community is working on lattice point counting; what is the difference between Minkowski's first and second theorems; what is the Betke-Henk-Wills conjecture; how do I get a Haar measure on a subspace in Lean; how do I bridge set dilations and the gauge in Mathlib; is there a continuous section of a projection of a convex body in Mathlib
verified: 2026-09-02
-->

# Geometry of numbers in Lean: what exists, what does not, and how the classical objects are shaped

Status: **active**. Author: lucas, 2026-08-30; section 4 extended 2026-09-02. Companion to `ecosystem-landscape.md`
(general tooling snapshot) and `proof-design-patterns.md` (domain-neutral architecture).

Trigger for this file: **"I am about to formalize an argument about lattices and convex
bodies, and I need to know what the library already gives me and what the field's objects
actually are."**

Everything about Mathlib below was read from the pinned source
(`v4.31.0`, commit `fabf563a7c95166b8d7b6efca11c8b4dc9d911f`) or checked by running Lean,
on 2026-08-30. **The library state and the pull-request state rot; the mathematics does
not.** Sections 1 and 2 are dated snapshots. Sections 3 and 4 are not.

---

## 1. What Mathlib has, as of 2026-08-30

**Present and usable.**

| Area | Where |
|---|---|
| lattices as `ℤ`-submodules: `IsZLattice`, rank, freeness, fundamental domain, comap along a linear map | `Mathlib/Algebra/Module/ZLattice/Basic.lean` |
| covolume, and the lattice-point counting asymptotic in three variants: `tendsto_card_div_pow` (for `ι → ℝ`), `tendsto_card_div_pow''` (general normed space, but the limit and the null-frontier hypothesis are both stated in the coordinates of a chosen `ℤ`-basis), and `tendsto_card_div_pow'` (**needs `[InnerProductSpace ℝ E]`**, and is the only one whose limit is the intrinsic `volume.real s / covolume L`). All three run along the discrete scales `r = 1/n`, `n : ℕ`, not a continuous `r → 0` | `Mathlib/Algebra/Module/ZLattice/Covolume.lean` |
| **Blichfeldt** (`exists_pair_mem_lattice_not_disjoint_vadd`) and **Minkowski's first (convex body) theorem** in strict and compact-weak forms | `Mathlib/MeasureTheory/Group/GeometryOfNumbers.lean` |
| the gauge / Minkowski functional, with the two membership bridges `gauge_lt_one_iff_mem_interior` and `gauge_le_one_iff_mem_closure`, sublevel-set descriptions, subadditivity, positive homogeneity, `gauge_eq_zero` under von-Neumann boundedness, continuity, and `gaugeSeminorm` | `Mathlib/Analysis/Convex/Gauge.lean` |
| convex functions on an open set in a finite-dimensional space are continuous (`ConvexOn.continuousOn`, `ConcaveOn.continuousOn`) | `Mathlib/Analysis/Convex/Continuous.lean` |
| a convex set's frontier is Haar-null, hence convex sets are null-measurable | `Mathlib/Analysis/Convex/Measure.lean` |
| Haar scaling `μ (r • s) = r ^ finrank * μ s`, images and preimages under linear maps with `|det|` | `Mathlib/MeasureTheory/Measure/Lebesgue/EqHaar.lean` |
| pushing Haar along a **surjective linear map**, and the `U ⊕ V` decomposition template (`Submodule.prodEquivOfIsCompl`, `isAddHaarMeasure_map`, `addHaarScalarFactor`) | `Mathlib/MeasureTheory/Measure/Haar/Disintegration.lean` |
| the average of a set of positive measure lies in the interior of a convex set containing it (`Convex.average_mem_interior_of_set`) | `Mathlib/Analysis/Convex/Integral.lean` |

**Absent**, each checked by reading the file that would hold it, not by recall:

* **successive minima** (nothing; `grep -rin successive Mathlib/` finds only unrelated prose);
* **Minkowski's second theorem**;
* **the Tao-Vu squeezing lemma**;
* **a continuous section of the projection of a convex body** (nothing in `Analysis/Convex/`);
* any statement that a fibrewise homothety scales Haar measure by `c ^ dim V`.

No indexed public Lean code outside Mathlib has them either: GitHub code search for
`"successive minima" language:lean` and `"squeezing lemma" language:lean` both return 0,
while the control `Blichfeldt language:lean` returns 5.

## 2. The live community effort, as of 2026-08-30

Read this before designing your own successive-minima API; the naming and the index
convention are being settled right now, and matching them costs nothing today.

* **Zulip `#Is there code for X? > Minkowski Lattice Theorem`** (37 messages, 2021-04-16 to
  2026-03-10). Yaël Dillies restarted it 2025-11-27; Kevin Wilson, Xavier Roblot and Antoine
  Chambert-Loir participate. Two independent applications are waiting on the second theorem:
  Schmidt's bounds on counting isomorphism classes (Wilson) and "a Bohr set contains a large
  generalised arithmetic progression" (Dillies).
* **mathlib4 PR #35812**, *successive minima and existence of a directional basis*
  (khwilson, opened 2026-02-26, **still open**, approved by Dillies 2026-06-03, further review
  by ocfnash and sgouezel, merge-conflicted since 2026-07-08, last activity 2026-08-06).
  Its design, worth adopting:
  ```lean
  noncomputable def successiveMin (L : Submodule ℤ E) (s : Set E) (i : ℕ) : ℝ≥0 :=
    sInf {r | i < Set.finrank ℝ (r • s ∩ L)}
  ```
  - **zero-based on purpose** (`i <`, not `i ≤`), because the `≤` form forces the 0-th minimum
    to be 0; values past the rank are junk and are proved to be 0;
  - codomain `ℝ≥0`, dimension via `Set.finrank ℝ`, the body an arbitrary set `s`;
  - the design argument, from the thread: define it for any set rather than for a norm, because
    every symmetric convex body is the unit ball of its gauge, and bundling the body as an
    instance would make it painful to handle several bodies at once (Chambert-Loir).
  - it proves monotonicity, non-emptiness of the defining set, attainment
    (`lt_setFinrank_successiveMin_smul`, **requires `IsCompact s`**), and the existence of a
    directional set/basis; it does **not** prove that no lattice point outside the flag's
    previous step has smaller gauge, which is what applications actually consume.
  - its `proof_wanted` for the second theorem is **vacuous as written**: the hypothesis
    `μ F * 2 ^ d < μ s * ∏ i < d, successiveMin L s i` is the negation of the second theorem's
    conclusion for a bounded symmetric convex body, so a proof would go through `False`. The
    intended statement is the volume inequality `μ s * ∏ λ i ≤ 2 ^ d * μ F`.

## 3. The classical objects, and which direction is hard

Successive minima of a body `K` with respect to a lattice `Λ` in dimension `d`:
`λ i = inf {r > 0 | the lattice points in r • K span at least i dimensions}`, with
`λ 1 ≤ ... ≤ λ d`. For a non-symmetric `K` the definition is applied to the symmetric body
`(1/2) • (K - K)`, which is what makes `gauge ((1/2) • (K - K))` the natural working vocabulary.

* **Minkowski's first theorem** (convex body theorem): a symmetric convex body of volume
  greater than `2 ^ d * covol Λ` contains a nonzero lattice point. In Mathlib.
* **Minkowski's second theorem**: `λ 1 * ... * λ d * vol K ≤ 2 ^ d * covol Λ`. Strictly stronger
  than the first. The lower bound `≥ 2 ^ d / d! * covol` is, in Cassels' words, "almost
  trivial"; **the upper bound "remains difficult"**. Interest is not the constraint: the Zulip
  thread in section 2 has three mathematicians and two waiting applications, and it is still
  unproved.
* The **discrete analogue** replaces `vol K` by `#(K ∩ Λ)`. Betke, Henk and Wills conjectured
  (1993) `#(K ∩ Λ) ≤ ∏ floor (2 / λ i + 1)` (the floor is around the whole `2 / λ i + 1`), with
  equality for a box; Malikiosis later conjectured it without central symmetry. **Still open in
  general**; proved in dimension ≤ 3 (Malikiosis) and, for symmetric bodies, in dimension 2 (BHW).
  Most known general bounds are the conjectured product times an exponential factor: BHW roughly
  `d!`, Henk `2 ^ (d-1)`, Malikiosis `(4/e) (sqrt 3) ^ (d-1)` in general and
  `(4/e) (cbrt (40/9)) ^ (d-1)` for symmetric bodies. Freyer and Lucas (2022) instead prove
  `∏ (2 / λ i + d)`, the first bound strong enough to recover Minkowski's second theorem by the
  limiting argument; Tointon (2024) proves `2 ^ k (1 + λ k / 2) ^ k / (λ 1 ... λ k)` where `k` is
  the number of minima at most 1, which also recovers the second theorem.

**The proof technique to know: the Tao-Vu squeezing lemma.** For an open convex body `K`, a
`j`-dimensional subspace `V`, `μ ∈ (0,1]` and an open `A ⊆ K`, there is an open `A' ⊆ K` with
`vol A' = μ ^ j * vol A` and `(A' - A') ∩ V ⊆ μ • (A - A) ∩ V`. It shrinks a set in the `V`
directions only, which is exactly what a proof indexed by a flag `V 1 ⊂ ... ⊂ V d` needs. It is
the engine of Tao and Vu's proof of Minkowski's second theorem (Additive Combinatorics, Thm 3.30 /
Lemma 3.31; restated without the unnecessary symmetry hypothesis as Lemma 3.5.2 of Tointon,
*Introduction to Approximate Groups*), and of the discrete bounds above.

Its own proof needs one construction that sounds harmless and is not: a **continuous section**
`f : π(K) → K` of the projection along a complement of `V`, so that the shrinking can be done
fibrewise toward a moving centre rather than toward a fixed point. A fixed centre would scale all
`d` directions and lose the whole point. Neither the section nor the lemma is in Mathlib.

## 4. Formalization consequences that transfer

Learned while architecting the Tointon formalization; each is stated so it applies to any
lattice-and-convex-body argument.

* **A fibrewise homothety scales Haar measure by `c ^ dim V`, and this is easy in product
  coordinates and awkward anywhere else.** For `Φ (u, v) = (u, c • v + g u)` with `g` merely
  measurable and `c > 0`, on `U × V` with any two Haar measures: `Φ` is a bijection whose inverse
  is measurable, so the image is a preimage and is measurable; `Measure.prod_apply` reduces to
  fibres; the fibre of the image is exactly a translate of `c •` the fibre; conclude with
  `Measure.addHaar_smul_of_nonneg` and translation invariance. Forty-five lines, no linear algebra.
  Doing the same computation after identifying `E` with `U ⊕ V` drags a Jacobian through every
  step. **Prove the core in coordinates and make the transfer a separate lemma whose only content
  is the proportionality constant**; the template for that transfer is the existing proof of
  `LinearMap.exists_map_addHaar_eq_smul_addHaar'` in `Haar/Disintegration.lean`.
* **Use the gauge as the working vocabulary and keep set dilations only in the definitions.**
  Statements like "the lattice points of `r • D` span `i` dimensions" are painful to manipulate
  directly; `gauge D x ≤ r` and `gauge D x < r` are not, and Mathlib's two membership bridges
  turn the open/closed distinction (which is where the paper-level subtleties live) into the
  distinction between `<` and `≤`. Attainment of an infimum over dilations then becomes a
  finiteness statement about `{x ∈ Λ | gauge D x ≤ t}`, which follows from discreteness plus
  boundedness (`Metric.finite_isBounded_inter_isClosed` with `AddSubgroup.isClosed_of_discrete`).
* **A directional basis is weaker than what applications use.** "There exist independent lattice
  vectors `v 1, ..., v d` with `gauge (v i) ≤ λ i`" does not by itself give "no lattice point
  outside `span (v 1, ..., v (j-1))` has gauge below `λ j`", which is the property proofs actually
  consume. When the minima are distinct the second follows from the first in three lines; when
  `λ (j-1) = λ j` it needs an argument through the least index `m` with `λ m = λ j`. Constructing
  the flag **greedily** (`v j` of minimal gauge outside the previous span) makes the strong
  property true by construction and reduces `gauge (v j) = λ j` to two short infimum arguments.
* **A limiting argument over refined lattices needs `rΛ` as an object, and the minima scale.**
  Papers recover a continuous theorem from a discrete one by applying the discrete bound to
  `rΛ` and letting `r → 0`, and they write the resulting product in the minima of the *original*
  lattice. The step in between, `λ i (K, rΛ) = r · λ i (K, Λ)`, is normally left implicit and is
  worth proving. In Lean, `r • Λ` already exists as a `Submodule ℤ E` (the pointwise action, which
  needs only `SMulCommClass ℝ ℤ E`), and `Submodule.coe_pointwise_smul` matches it to the
  `r • (↑L : Set E)` that Mathlib's counting statements use, so no new construction is required
  *unless you need the lattice instances on it*: for those, transport along a continuous linear
  equiv with `ZLattice.comap` and its `instIsZLatticeComap`, since a bare `def` will not fire
  instance search. The proof of the scaling law is three set identities and
  `Real.sInf_smul_of_nonneg`: `(t • D) ∩ rΛ = r • ((r⁻¹t • D) ∩ Λ)`, dilation by a nonzero factor
  does not change a span, so the defining set of admissible scales scales, so its infimum does.
* **A convex body is null-measurable, not measurable, and the distinction decides whether a
  library theorem applies.** `Convex.addHaar_frontier` gives `μ (frontier s) = 0` for free, so a
  paper's hypothesis "convex body with boundary of measure zero" is redundant and should be
  dropped rather than assumed. But a convex set can differ from its interior by a non-Borel subset
  of that frontier, so `MeasurableSet` does **not** follow, and every counting or volume theorem
  stated with `MeasurableSet s` (the `tendsto_card_div_pow` family, for one) needs it as an added
  hypothesis. It holds for any open or closed body, which is what concrete instances use. Trading
  the paper's stated hypothesis for a different one is the honest move here, not a strengthening
  to hide.
* **`Set.finrank ℝ` over `ℝ` and over `ℤ` agree on subsets of a discrete subgroup**
  (`Real.finrank_eq_int_finrank_of_discrete` at the v4.31.0 pin; renamed to
  `setFinrank_real_eq_setFinrank_int_of_discrete` on master since 2026-05-31). Needed whenever a
  statement about `ℝ`-dimension is proved by exhibiting `ℤ`-independent lattice vectors.
