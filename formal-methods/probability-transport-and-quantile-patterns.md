<!--kb
id: probability-transport-and-quantile-patterns
labels: lean, mathlib, probability, couplings, quantiles, conformal, transport
triggers: I am about to formalize a probability argument involving couplings; distributional ambiguity in a proof assistant; CDFs or quantiles in a formalization; conformal ranks; where ordinary informal probability habits become unsound in a proof assistant
verified: 2026-07-29
-->

# Probability, transport, quantile, and conformal-proof patterns

Status: **active** (first synthesis 2026-07-29). Author: cidral.

Trigger for this file: **“I am about to formalize a probability argument involving
couplings, distributional ambiguity, CDFs/quantiles, or conformal ranks.”** This is
the failure-driven architecture layer. Current libraries and pins live in
`ecosystem-landscape.md`; paper-specific statements and counterexamples remain in
their project catalog/audit.

The source case for these patterns was the formalization audit of
*Conformal Prediction under Lévy–Prokhorov Distribution Shifts*. The reusable
content is not that paper's theorem list, but the places where ordinary informal
probability habits become unsound in a proof assistant.

## Recommended dependency spine

Build in this order:

```text
probability measures / finite restricted measures
        ↓
couplings + mapped marginals
        ↓
threshold-coupling witness relation
        ├── gluing / decomposition
        ├── pushforward contraction
        └── one-dimensional CDF inequalities
                 ↓
        lower quantile Galois laws
                 ↓
        atom-safe extremal constructions
                 ↓
        empirical quantile / exchangeable-rank lemma
                 ↓
        conformal coverage arithmetic
```

Do not begin with the final numerical infimum or the final conformal theorem. Each
arrow is a genuine interface, and conflating two layers is how attainment,
measurability, atoms, and tie handling disappear from an informal proof.

## Use a witness relation downstream; isolate the infimum/attainment bridge

A paper often defines a threshold transport discrepancy numerically:

\[
  D_\varepsilon(P,Q)
  :=\inf_{\gamma\in\Gamma(P,Q)}
       \gamma\{(x,y):d(x,y)>\varepsilon\}.
\]

Most downstream proofs do not need this real-valued infimum. They need:

\[
  \exists\gamma\in\Gamma(P,Q),\qquad
  \gamma\{d(x,y)>\varepsilon\}\le \rho.
\]

Make that existential statement the working relation. Prove the bridge
`D_ε(P,Q) ≤ ρ ↔ witness relation` separately, with the exact topological
hypotheses that give attainment. Benefits:

- gluing and pushforward arguments consume an actual coupling, not an infimum;
- proofs do not repeatedly invoke compactness/lower semicontinuity;
- a paper's Euclidean application can proceed even if the general attainment
  theorem is not yet internalized;
- the formal statement exposes whether the relation is strict (`> ε`) or
  non-strict (`≥ ε`) at the boundary.

The boundary convention matters. A coupling that translates every point by
exactly \(\varepsilon\) has zero bad mass for the cost
\(\mathbf 1\{d>\varepsilon\}\), but all its mass is bad for
\(\mathbf 1\{d\ge\varepsilon\}\).

### Ambient-space trap

A paper may say only that \(Z\subseteq\mathbb R^d\) and then invoke Polish-space
attainment. An arbitrary subset with the inherited topology need not be Polish.
When the measures are really Euclidean measures supported on \(Z\), formalize
them on the ambient \(\mathbb R^d\) and carry the support property separately.
Do not silently infer Polishness of an unspecified subset.

## Good/bad coupling splits: finite measures first, normalization last

For

\[
  G=\{d(x,y)\le\varepsilon\},\qquad
  B=G^c,
\]

split a coupling as the finite measures \(\gamma|_G\) and \(\gamma|_B\).
Their marginals already contain the local/global decomposition. This is safer
than immediately normalizing both pieces into probability measures.

The normalization-first proof has two recurring defects:

1. it divides by the bad mass even when that mass is zero;
2. it claims an arbitrary coupling of normalized bad marginals mismatches with
   probability exactly one, when only an upper bound by one is available.

The finite-measure route needs only:

- the good part stays within \(\varepsilon\);
- the bad part has total mass at most \(\rho\);
- any coupling/recombination of the bad marginals contributes at most that
  total mass.

If a probability kernel is eventually convenient, split off the zero-mass case
before normalizing. “Conditional law on an event” is not automatically defined
when the event has probability zero.

### Pathwise factorization and the reverse gluing pattern

For the forward local/global factorization, an especially robust intermediate
point is

\[
  m(x,y)=
  \begin{cases}
    y,&d(x,y)\le\varepsilon,\\
    x,&d(x,y)>\varepsilon.
  \end{cases}
\]

Then \((x,m(x,y))\) never moves farther than \(\varepsilon\), while
\((m(x,y),y)\) differs only on the original bad event. This single pathwise map
handles zero bad mass automatically and avoids restricted-measure
normalization altogether.

For the reverse direction, first isolate a three-way law
\((X,M,Y)\) with prescribed \((X,M)\) and \((M,Y)\) pair laws. On a standard
Borel middle space, Mathlib's `condDistrib`, measure–kernel composition product
`Measure.compProd`, and kernel pullback `Kernel.comap` give a direct
construction: sample \((X,M)\) from the first coupling, then sample \(Y\) from
the regular conditional law of the second coupling's last coordinate given
its first. The endpoint estimate is the pathwise containment

\[
 \{d(X,Y)>\varepsilon\}
 \subseteq
 \{d(X,M)>\varepsilon\}\cup\{d(M,Y)>0\}.
\]

Keep these as separate layers: construction of the glued law, verification of
its two adjacent pair laws, event containment, and the final mass bound. That
separation makes the exact standard-Borel hypothesis visible and produces a
reusable gluing theorem rather than burying disintegration inside one paper
proof.

### Conditional-law trap: integration is not conditional expectation

If a kernel \(K(x,\cdot)\) is the conditional law of \(Y\) given \(X=x\), the
law of \(Y\) is recovered by integrating the **kernel** against the law of
\(X\):

\[
  \mathcal L(Y)(A)=\int K(x,A)\,\mathcal L(X)(dx).
\]

Do not write \(Y=\mathbb E[Y\mid X]\) or identify a random variable with the
expectation of its conditional law. Conditional expectation retains only a
mean and generally has a different distribution. When the intended result is
only a corruption representation, a direct pathwise construction from one
coupled pair plus a bad-event indicator is usually simpler than disintegration.

## Pushforward contraction: map one coupling; do not prove surjectivity

For a \(k\)-Lipschitz map \(s\), the useful statement is

\[
  \gamma\in\Gamma(P,Q)
  \Longrightarrow
  (s\times s)_\#\gamma\in\Gamma(s_\#P,s_\#Q),
\]

together with

\[
  \{|s(x)-s(y)|>k\varepsilon\}
  \subseteq
  \{d(x,y)>\varepsilon\}.
\]

This proves contraction of the threshold discrepancy. Do **not** strengthen the
task to

\[
  \Gamma(s_\#P,s_\#Q)=(s\times s)_\#\Gamma(P,Q)
\]

unless some later result genuinely needs coupling lifting. The forward
inclusion is elementary and sufficient; surjectivity needs extra measurable
lifting/disintegration machinery.

## Quantiles: use Galois laws, never `CDF(quantile)=level`

For the lower quantile

\[
  q_\mu(u)=\inf\{x:F_\mu(x)\ge u\},
\]

the atom-safe interface for \(0<u<1\) is:

\[
  q_\mu(u)\le x \iff u\le F_\mu(x).
\]

Two safe consequences are:

- \(F_\mu(q_\mu(u))\ge u\);
- if \(x<q_\mu(u)\), then \(F_\mu(x)<u\).

The tempting equality

\[
  F_\mu(q_\mu(u))=u
\]

is false at atoms. It is the most dangerous quantile shortcut in constructive
worst-case-distribution proofs: it can make a proposed piecewise “CDF” jump
downward and can make the claimed moved mass exceed its budget.

### Endpoint trap

A real-valued lower quantile is naturally well behaved at levels in \((0,1)\).
At level \(1\), the superlevel set can be empty for an unbounded law; at level
\(0\), its infimum can be \(-\infty\). Choose one of these explicitly:

- restrict headline theorems to interior levels;
- use an extended-real quantile;
- add bounded-support hypotheses;
- for finite samples, use an order-statistic plus \(+\infty\) convention.

Never write a real-valued `Quant(1; P)` and also argue that it diverges.

## Atom-safe extremizers: split mass, not quantile intervals

When a sharpness proof says “move exactly \(r\) mass from this interval,” an atom
may prevent realizing that instruction by selecting a smaller measurable set.
It does **not** prevent splitting the measure.

Let \(\nu=\mu|_A\) have mass \(m>0\), and let \(0\le r\le m\). Then

\[
  \nu_r := (r/m)\,\nu
\]

is a finite submeasure of mass exactly \(r\), including when \(A\) consists of
one atom. Operationally, the associated coupling/kernel randomizes which
fraction of that atom follows the moved branch.

In Lean, expect the scalar to live in `ℝ≥0∞` (the measure scalar), with separate
proofs that \(m\ne0\), the ratio is at most one, and the scaled measure has the
required total mass. Do not search for a measurable subset of exact mass:
that would impose a non-atomicity requirement the theorem does not have.

This gives a general extremizer template:

1. perform the deterministic local map (for example \(x\mapsto x+\varepsilon\));
2. identify a finite restricted measure whose mass affects the target CDF;
3. scale it to the exact amount allowed by the global budget;
4. send that submeasure to a point beyond the queried threshold;
5. leave the complement on the local branch.

### Two reusable consequences

For a threshold-coupling ball on \(\mathbb R\):

\[
  F_Q(q)\ge F_P(q-\varepsilon)-\rho.
\]

This follows directly from a coupling: all mass with
\(X\le q-\varepsilon\) reaches \(Y\le q\), except possibly the bad mass.

The sharp worst-case CDF is therefore

\[
  \inf_Q F_Q(q)
  =\max\bigl(F_P(q-\varepsilon)-\rho,0\bigr),
\]

not the untruncated difference. The maximum at zero is forced before any
construction: a CDF cannot be negative. Sharpness moves
\(\min(\rho,F_P(q-\varepsilon))\) of the relevant mass above \(q\).

For \(0<\beta\) and \(\beta+\rho<1\), prove the worst-case lower-quantile
upper bound by transporting the \((\beta+\rho)\)-sublevel mass. For sharpness, fix each
\(y<q_P(\beta+\rho)+\varepsilon\) and split only enough mass below \(y\) to
make the new CDF there strictly less than \(\beta\). Let \(y\) approach the
target. This preserves the paper's “local translation + global removal” route
without requiring `F(q(u))=u`.

## Separate a universal bound from its sharpness theorem

If a downstream coverage theorem uses only

\[
  F_Q(q)\ge F_P(q-\varepsilon)-\rho,
\]

make that a standalone lemma. Do not force the main theorem to depend on the
harder exact-infimum construction. This separation has two benefits:

- a flaw in the paper's extremizer does not contaminate a valid coverage bound;
- the Lean dependency graph identifies which result needs atom-splitting
  machinery and which needs only a one-line event inclusion.

General rule: “lower/upper bound” and “attainment/sharpness” are different
formalization items even when a paper combines them into one equality.

## Conformal prediction: three foundations, not one rank slogan

“By exchangeability, the rank is uniform” hides distinct obligations:

1. **Combinatorial layer:** among \(n+1\) positions, how many ranks lie below
   the chosen cutoff, and how do ceiling/floor operations transform the bound?
2. **Probabilistic symmetry layer:** why is the distinguished test position
   distributed like the others under permutations?
3. **Tie layer:** what rank is assigned when scores coincide?

A file that proves only the finite counting arithmetic after *assuming* a
uniform test rank has not formalized conformal validity.

For ties, choose explicitly between:

- randomized tie-breaking, with an auxiliary independent uniform variable;
- conservative weak/strict ranks, yielding an inequality rather than exact
  uniformity;
- an atomless-score hypothesis, if the source really assumes one.

Also distinguish **exchangeability** from **iid**. Standard conformal coverage
can use finite exchangeability. An expected-population-CDF statement such as

\[
  \mathbb E\!\left[
    F_P\!\left(q_{\widehat P_n}(\beta)\right)
  \right]
  \ge \frac{\lceil n\beta\rceil}{n+1}
\]

is normally stated for an iid empirical sample and proved by adjoining an
independent \((n+1)\)-st draw, then applying a tie-aware exchangeable-rank
argument. Record the iid-to-exchangeability bridge instead of switching words
mid-proof.

## Data-selected ambiguity radii need a population-containment theorem

Sample splitting proves independence between parameter selection and the
calibration statistic computed on the held-out split. It does **not** prove

\[
  D_\varepsilon(P,P_{\mathrm{test}})\le\widehat\rho
\]

from an empirical distance
\(D_\varepsilon(\widehat P,\widehat P_{\mathrm{test}})\).

To claim population coverage after selecting an ambiguity radius from data,
one still needs, for example:

- a simultaneous high-probability upper confidence bound over the candidate
  radius grid;
- a concentration theorem for the discrepancy;
- or population containment as an explicit assumption.

Formalize a deterministic grid search separately from its statistical
validity theorem. Independence and containment are different propositions.

## Fast diagnostic table

| Tempting informal move | What to require instead |
|---|---|
| `inf ≤ ρ`, therefore choose a minimizer | attainment theorem, or use an existential witness relation |
| Normalize good/bad restrictions immediately | finite restricted measures; split the zero-mass case |
| `F(Quant(u)) = u` | quantile/CDF Galois equivalence and one-sided inequalities |
| Move an interval containing exactly `ρ` mass | scaled restricted submeasure / randomized atom split |
| Exact worst-case CDF is `F-ρ` | nonnegative part `max(F-ρ,0)` |
| Pushforward coupling sets are equal | map one witness coupling; prove only the needed inclusion |
| Exchangeability makes ranks uniform | permutation law + combinatorics + explicit tie convention |
| Held-out selection preserves coverage | also prove population ambiguity-set containment |
| Continuous on compact implies Lipschitz | only uniform continuity follows without stronger hypotheses |

## Current ecosystem pointer

As checked 2026-07-29, Mathlib has CDFs, probability measures, restriction,
mapping, products, Dirac measures, kernels, and ordinary Prokhorov
infrastructure, but not the complete quantile/coupling/exchangeable-rank stack.
Econlib contains an atom-safe quantile API and coupling/transport definitions;
TauCeti contains finite exchangeability; their pins differ from the shared
project pin. Exact commits, licenses, modules, limitations, and the integration
rule are in `ecosystem-landscape.md` § “Probability, quantiles, optimal
transport, and exchangeability.”

## Evidence and source pointers

- Detailed derivations, cited-result checks, counterexamples, and package audit:
  `dev-science-ops/math-formalizations/conformal-lp/SOURCE_AUDIT.md`.
- Reviewed statement/proof dependency graph:
  `dev-science-ops/math-formalizations/conformal-lp/LP-robust-conformal/lean_proofs/catalog.json`.
- Current package/module facts and exact checked commits:
  `ecosystem-landscape.md` § “Probability, quantiles, optimal transport, and
  exchangeability.”
