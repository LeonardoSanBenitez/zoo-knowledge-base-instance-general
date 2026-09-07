# Comparing dispersion between two groups: which statistic, what it assumes, and the four traps that survive peer review

```toml
schema  = "zoo-topic-entry/typed/0.1"
id      = "comparing-dispersion-between-two-groups"
kind    = "synthesis"
status  = "active"
areas   = ["statistics"]
authors = ["maria"]
created = 2026-09-06
updated = 2026-09-06
verified = 2026-09-06
confidence = "verified"
triggers = [
  "is group A more variable than group B",
  "variability ratio versus coefficient of variation ratio",
  "when should I use lnCVR instead of lnVR",
  "is the coefficient of variation meaningful for this outcome",
  "my CVR is below 1 and I do not know why",
  "the SD is correlated with the mean, should I normalise",
  "meta-analysis of variances not means",
  "how do I pool a difference of two variances",
  "inverse variance weighting when the weight contains the effect",
  "does this intervention change the spread or only the average",
  "how much of a mean-SD correlation is scale mixing",
  "how do I know whether my estimate describes a corpus or one study",
  "what variability ratio could this meta-analysis have detected",
  "minimum detectable effect for a variance comparison",
  "my outcome has a floor, does that bias the variance comparison",
  "truncation at a scale minimum and the standard deviation",
  "what is the null for a variability ratio on a bounded scale",
  "my regressor and my outcome share a term, how do I build the null",
  "does improvement depend on baseline severity",
  "is my correlation between baseline and change spurious",
  "mathematical coupling Oldham 1962",
  "proportional recovery rule",
]
sources = [
  "Nakagawa et al. 2015, Meta-analysis of variation, Methods Ecol Evol 6:143-152 (eq. 9-13)",
  "instance-papers/areas/treatment-effect-heterogeneity.md and the records under it",
]
see_also = ["the-specification-execution-gap", "construct-validity-and-formalization"]
```

Author: maria, 2026-09-06. Domain-neutral. Everything here was measured on a
51,396-patient clinical corpus (`instance-papers/papers/ploderl2019-personalised-antidepressants`,
`mccutcheon2022-reappraising-variability`), but nothing in it is clinical: the
same three statistics appear whenever two groups are compared on spread rather
than on location — A/B tests on variance, benchmark score dispersion across
seeds, latency tails, model-output variability.

Working code: `zoo-knowledge-base/tools/statlib.py` — `lnvr`, `lncvr`,
`var_diff`, `max_loo_influence`, `re_meta`. Tested in `tools/test_statlib.py`.

## The three statistics, and what each one assumes

For two groups with means `m1, m2`, SDs `s1, s2`, sizes `n1, n2`:

| | statistic | null it tests |
|---|---|---|
| **lnVR** | `ln(s1/s2)` + small-sample correction | *additive* homogeneity: the treatment shifts everyone by the same amount |
| **lnCVR** | `ln((s1/m1)/(s2/m2))` + the same correction | *multiplicative* homogeneity: the treatment multiplies everyone by the same factor |
| **D** | `s1² − s2²` | nothing; it is the raw identified quantity |

They are not three views of one thing. Each is unbiased under its own null and
badly wrong under the other's. On a corpus with **zero** individual variation by
construction, an additive truth returns lnVR 0.999 / lnCVR 1.204, and a
multiplicative truth returns lnVR 0.829 / lnCVR 0.999. **A 17–20% apparent
effect can be manufactured by the choice alone.**

## Trap 1: lnCVR is the mean ratio in disguise

The small-sample corrections in Nakagawa eq. 9 and eq. 11 are **identical** and
therefore cancel. So, per unit of analysis, exactly:

    lnCVR − lnVR = ln(m2 / m1)

Measured over 169 real studies, the largest absolute deviation from that
identity is **2.8e-16** — machine epsilon. lnCVR carries no information beyond
lnVR and the ratio of the two group means. If the groups differ in mean because
the treatment works, **CVR is the treatment effect wearing a denominator.**

### The consequence nobody notices until you look for it

Because the mean ratio is doing the work, **the sign of a CVR result is set by
the reporting convention, not by the data.** In one paper, on the same drugs,
the same authors, the same statistic:

| how the outcome was summarised | k | VR | CVR |
|---|---|---|---|
| pre–post **change** (treated group changes more) | 169 | 1.01 | **0.82** |
| **endpoint** level (treated group ends lower) | 84 | 0.98 | **1.15** |
| one subgroup, change | 11 | 1.04 | **0.65** |
| the same subgroup, endpoint | 13 | 0.93 | **1.37** |

VR is stable. CVR crosses 1, and moves by a factor of 2.1 in the subgroup.
Nothing about the units of observation changed — only which of two
mathematically equivalent summaries got published. The authors interpreted the
0.82 substantively and wrote that it had "no immediately plausible explanation";
the 1.15 was in a supplement and was not discussed.

**Rule.** Before reporting any statistic, ask what it would do under an
equivalent restatement of the same data. A quantity whose sign depends on a
free choice of summary is measuring the choice.

### "But the SD is correlated with the mean, so I should normalise"

This is the standard justification and it needs two checks before it licenses
anything.

1. **Is the correlation within your unit of measurement, or across units?** In
   the corpus above, r(mean, SD) across all studies was **+0.55**; pooled
   *within* measurement instrument it was **+0.135**. **75% of it was
   between-instrument mixing** — longer scales have both larger means and larger
   SDs for reasons that have nothing to do with the treatment.
2. **Is it even the right correlation?** An *across-study* correlation cannot
   license a *within-study, between-group* division. The statistic that would is
   `r(ln(m1/m2), ln(s1/s2))`, and there it was **+0.110, p = 0.154**.

### What to do instead: estimate how much the SD scales with the mean

Model `SD ∝ mean^λ`, so `lnVR = λ · ln(m1/m2)`. Then lnVR assumes λ = 0 and
lnCVR assumes λ = 1, and **λ is estimable** instead of assumed.

**The raw regression slope is not λ.** Regress lnVR on `ln(m1/m2)` in simulated
worlds where λ is 0 and 1 by construction: the slopes come back +0.002 and
+0.517, so the estimator's own scale is **0.515**, not 1 — an uncalibrated slope
understates λ roughly twofold (regression dilution: the observed log mean ratio
carries its own sampling error). Rescale against both anchors:

    λ̂ = (b_observed − b_at_λ=0) / (b_at_λ=1 − b_at_λ=0)

with a bootstrap over units for the interval. On the corpus above,
**λ = 0.098 [−0.024, 0.241]**: lnVR's assumption inside, lnCVR's far outside,
and the published lnCVR applied **10.2×** the correction the data supported.

Two simulated worlds and one regression. It is cheap, and it converts a silent
assumption into a measured parameter with an interval.

> **Provenance, added 2026-09-07.** Most of the *qualitative* content of traps 1
> and 3 is in Mills et al., *Epidemiology* 2021, "Detecting Heterogeneity of
> Intervention Effects Using Analysis and Meta-analysis of Differences in Variance
> Between Trial Arms" — the coefficient of variation needs a ratio scale, a
> mean–SD correlation does not license it, a bounded scale reduces variance in the
> arm that improves more, and a difference in variances may only be pooled within
> one scale. Read it; it is the best single inventory of these methods. What is
> measured rather than restated here: the exact `lnCVR − lnVR` identity, the
> reporting-convention sign flip, λ, the shrinkage curve and its regime reversal,
> the resolving-power calculation — and trap 2, which is a correction to their
> deposited code.

## Trap 2: pooling `D = s1² − s2²` by inverse-variance weighting is biased

D is the attractive statistic — unbiased, sampling distribution known,
**legitimately negative**, no square root, no branch choice. Then you pool it
across studies and the obvious weight breaks it.

The textbook normal-theory variance of a difference of sample variances is

    v = 2 s1⁴/(n1−1) + 2 s2⁴/(n2−1)

which makes the weight **a function of the same draw as the numerator**. When
the two groups differ in size, the smaller group's `s⁴` dominates `v`, so
whichever side is smaller has its deviations shrunk harder, and the pool drifts
the other way.

Measured on a real 169-study corpus where D was **0 by construction**:

| | bias | coverage of a nominal 95% interval |
|---|---|---|
| naive weight, control group smaller | **+0.514** | 90.2% |
| same, group sizes forced equal | +0.064 | 95.6% |
| same, groups swapped | **−0.567** | 90.8% |
| weight from the across-group pooled variance | **−0.003** | 96.6% |

Three falsifiable predictions of the mechanism, all confirmed. **This is the
estimator in the reference implementation for the method** — Mills et al.'s
`MetaAnalysis.R` builds `est_diff_SE` as exactly this and hands it to
inverse-variance pooling — so it is not a straw man. **The fix** is a
weight built from a quantity that does not contain the difference:

    v = 2 s_p⁴ (1/(n1−1) + 1/(n2−1)),   s_p² = the across-group pooled variance

verified at D = 0, +5 and −5. `statlib.var_diff(..., weight="pooled")`. A
common-scale weight also works and is less efficient.

**D carries units.** Squared points of one instrument are not squared points of
another. On a corpus mixing four instruments, the unit-mixed pool moved further
than any difference between the groups did — and the unit string in the record
literally read "squared HAMD/MADRS points", two units in one field, which is
what a unit error looks like when nothing checks units.

## Trap 3: if the outcome is bounded, the null is not 1

An outcome with a floor (a symptom scale that stops at zero, a count, any capped
improvement) is measured as an improvement `X` from a starting point, and cannot
exceed the **headroom** `H = start - floor`. What gets recorded is `min(X, H)`.
Truncation removes variance, and one dimensionless number governs how much:

    z = (mean headroom - mean improvement) / SD(improvement)

**The treated group always has the smaller z, because it improves more.** So a
bounded scale moves the variability ratio away from 1 in a fixed direction,
before any difference between the groups exists.

`statlib.floor_shrinkage(z, headroom_dispersion)` returns
`SD(recorded)/SD(true)`, where `headroom_dispersion` is `SD(H)` in units of
`SD(X)`:

| z | hd=0 | hd=0.5 | hd=1.0 | hd=1.5 | hd=2.0 |
|---|---|---|---|---|---|
| 0.5 | 0.744 | 0.761 | 0.839 | 0.997 | **1.208** |
| 1.0 | 0.867 | 0.857 | 0.872 | 0.962 | **1.127** |
| 1.5 | 0.942 | 0.928 | 0.913 | 0.950 | **1.065** |
| 2.0 | 0.981 | 0.968 | 0.948 | 0.954 | **1.025** |
| 3.0 | 1.000 | 0.998 | 0.988 | 0.976 | 0.993 |

**The direction is a regime, not a law.** A headroom that varies across subjects
adds variance of its own, and above roughly 1.5 improvement-SDs of dispersion the
addition wins and the bound *inflates* the recorded SD. I asserted "a floor biases
variability downward" as a law before computing this table, and the table refuted
it.

Measured on two clinical corpora at z between 1.5 and 2.5, the bias in VR is
**1 to 3%** — which happened to be the size of every effect either literature had
ever reported. In one of them the published, significant result (VR = 0.97,
p = .01) stops excluding 1 once the bias is subtracted.

**Two things this does not license.** It is a *model* — a normal improvement
truncated at a normal headroom — and the within-corpus test that would confirm it
had **no resolving power** on the only corpus that could support it: the
simulated no-mechanism and mechanism-only anchors were separated by 0.52 of their
own noise at k = 68, because the predicted per-trial bias spans 0.11 log units
against a per-trial sampling SD of 0.10. Any correction from this table must be
labelled model-based. And the first version of that test *did* produce a
`p < 0.001` result, which was an artifact: the regressor `z` contains the same
group SDs as `lnVR = log(s1/s2)`, and holding the regressor fixed across
simulated replicates broke that coupling in the null only. **When a regressor is
built from the same quantities as the outcome, the null must rebuild it too.**

## Before anything else: what could this design have seen?

`var(lnVR) = 1/(2(n1−1)) + 1/(2(n2−1))` per study depends on **group sizes only**
— not on the SDs, not on the effect, not on the scale. So the resolving power of a
dispersion comparison is fixed the moment the studies are counted, and it can be
computed from an abstract. `statlib.mde_variability_ratio(k, n_total, split)`.

Measured across four clinical literatures that all report "no difference in
variability": the largest corpora resolve **1.016–1.018**, the mid-sized ones
**1.031–1.038**, and a 2026 application with 15 studies and 1,141 participants
resolves **1.126** — which cannot see any effect that field has ever argued
about. A null result says nothing about any ratio below its own limit, and that
limit is almost never reported.

## The check that neither simulation nor validation will do for you

A contaminated-null simulation was built specifically to test whether the
corrected weight had lost robustness — 129 studies at D = 0, one of them given a
true SD ratio up to 2.7, 300 replicates. **It caught nothing**: both weights
stayed near zero at every contamination level.

On the real data the two weights differed by 1.46 on one subset, and **one study
explained all of it** — deleting it moved the pooled D by 73% of its own CI
half-width and flipped the sign.

> **Simulation validates the estimator. Only leave-one-out validates the
> corpus.** A simulated corpus departs from the null only where you made it, and
> a real one departs where you did not think to look.

Report `max |leave-one-out delta| / CI half-width` beside every pooled estimate
(`statlib.max_loo_influence`). Above ~1 the estimate is describing one study, not
a corpus. Do NOT assert a threshold in a test, though: one wild study also
inflates τ² and widens the interval, so the ratio can stay under 1 while the
estimate is still hostage to that study. It is a number to report, not a gate.

## The fourth trap, which is the same trap: correlating a change with its own baseline

Everything above compares two groups. The same algebra governs a design that looks
unrelated — one group, measured twice, asking whether *how much you improve*
depends on *where you started*. Write baselines `X`, follow-ups `Y`, change
`D = Y − X`. Then

    r(X,D) = [s_Y·r(X,Y) − s_X] / sqrt(s_Y² + s_X² − 2·s_X·s_Y·r(X,Y))

so `r(X,D)` is a function of `r(X,Y)` and the **same variability ratio**
`s_Y/s_X` this entry has been about all along. Consequences:

* **When `s_Y/s_X` is small, `r(X,D)` is driven toward −1 whatever `r(X,Y)` is.**
  At `s_Y/s_X = 0.158`, `r(X,D)` cannot exceed −0.987 for any non-negative
  `r(X,Y)`. A "correlation of −0.97 between initial severity and improvement" is
  then not a finding; it is the ratio.
* **The canonical case:** X and Y independent with equal variance gives
  `r(X,D) = −1/sqrt(2) = −0.707`. Oldham noticed this in 1962 and it keeps being
  rediscovered.
* **A bound makes `s_Y/s_X` small** — which is trap 3 arriving from the other
  direction. So a ceiling manufactures a strong baseline–change correlation with
  no differential response anywhere.
* **`r(X,Y)` and `r(X,D)` have identical residuals.** Fitting change instead of
  outcome does not change which cases are outliers; it only inflates the effect
  size.

**And this is the same identity as the treatment-effect one.** In a two-arm trial,
write a participant's treated outcome as `Y1 = Y0 + δ`. Then the correlation
between the individual effect and the control-arm outcome *is* `r(X,D)`, and the
variability ratio *is* `s_Y/s_X` — verified as functions to machine zero on a
40×40 grid. Two literatures have been arguing about one theorem under two names,
one tracing to Oldham (1962), the other to Nakagawa (2015), neither citing the
other.

**The difference that matters is observability, not mathematics.** When both
measurements are taken on the same unit, `r(X,Y)` is estimable and the identity
*pins* the answer: the correlation is spurious and you can prove it. When one of
the two is counterfactual — the participant is never observed under both
conditions — `r(X,Y)` is not estimable, and the same parameter is not merely
mis-estimated but **unidentified**. Same equation, remediable by reporting in one
case and requiring a different experiment in the other.

**Practical rule.** Never report `r(baseline, change)` alone. Report
`r(X,Y)`, `r(X,D)` and `s_Y/s_X` together, on the *whole* sample before any
subgroup split — and if you are comparing two arms rather than two timepoints,
know that you are reporting two of the three and assuming the missing one.

## And the identification question, which comes first

`VR` and `D` bound the dispersion of individual effects; they do not measure it.
Write the variance of a treated outcome as

    Var(Y1) = Var(Y0) + Var(δ) + 2ρ·SD(Y0)·SD(δ)

where δ is the per-unit effect and ρ its correlation with the untreated outcome.
`D = Var(δ) + 2ρ·SD(Y0)·SD(δ)`. **ρ is not observable in a between-group design
at all** — no unit is seen under both conditions — and the implied SD(δ) moved
by a factor of six across the ρ values one literature had used, on the same data.

Two arms with identical means and SDs are equally consistent with a uniform
effect and with a mixture in which a third of the units are transformed and the
rest untouched. For a two-point mixture where a fraction p gets an extra δ,
`Var(effect) = p(1−p)δ²`, so the whole "how big a subgroup could be hiding here"
question is the single inequality `p(1−p)δ² ≤ D_upper` — closed form, no
simulation grid.

**Ask what the design identifies before auditing the estimator.** If the target
is not identified, a reanalysis is about the estimator's behaviour, not about
the world, and its first sentence should say so.
