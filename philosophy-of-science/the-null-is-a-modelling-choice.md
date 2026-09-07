# The null is a modelling choice, it is almost never zero, and almost nobody says which one they used

```toml
schema  = "zoo-topic-entry/typed/0.1"
id      = "the-null-is-a-modelling-choice"
kind    = "synthesis"
status  = "active"
areas   = ["philosophy-of-science", "statistics"]
authors = ["maria"]
created = 2026-09-07
updated = 2026-09-07
confidence = "verified"
verified = 2026-09-07
triggers = [
  "what should my null hypothesis be",
  "my p value is tiny but I do not trust it",
  "is my simulated null the right null",
  "two papers disagree and both have simulations",
  "how do I know my control condition controls for anything",
  "my estimator returns a non-zero value when nothing is happening",
  "the effect I found is the size of my own artifact",
  "how do I test whether my design could have detected anything",
  "my regressor is built from the same data as my outcome",
  "shuffling the labels did not break the association",
  "why did my robustness check agree to four decimal places",
  "how do I evaluate my own retrieval system fairly",
  "my first principal component is document length",
  "should I use counts or densities as features",
  "does my dimensionality reduction show anything real",
]
sources = [
  "the instances below are all measured in this instance; see instance-papers/areas/treatment-effect-heterogeneity.md and the records under it",
]
see_also = [
  "comparing-dispersion-between-two-groups",
  "the-specification-execution-gap",
  "construct-validity-and-formalization",
]
```

Author: maria, 2026-09-07. Every instance below is one I measured, in this
instance, with the numbers in the record. That is the point: none of this is
reconstructible from a textbook, because textbooks state the rule ("specify the
null") and the failures are all in what happens when you try.

## The claim

**A null hypothesis is a description of a world.** Writing "H₀: θ = 0" names a
number, not a world, and the number is only the right one if the world in which
the mechanism is absent happens to produce it. In every case I have looked at
carefully, it did not — because designs impose structure, scales have bounds,
estimators have their own behaviour, and analysts make choices before the
statistic is computed.

Seven distinct ways it goes wrong. They are not variants of one another; each was
found separately, and five of them were found in my own work rather than someone
else's -- including one I found twice, in two unrelated projects, in a single day,
without recognising the second as the first.

## 1. Two nulls, one statistic, and nobody says which

Two literatures, no shared authors, same shape.

**Psychiatry.** Comparing spread between a treated and a control arm, `lnVR`
tests *additive* homogeneity (the treatment shifts everyone equally) and `lnCVR`
tests *multiplicative* homogeneity (it multiplies everyone equally). Each is
unbiased under its own null and badly wrong under the other's: on a corpus with
**zero** individual variation by construction, an additive truth returns lnVR
0.999 / lnCVR 1.204, and a multiplicative truth returns 0.829 / 0.999. **A
17–20% apparent effect is available from the choice alone**, against real signals
of a few per cent. No paper in that literature says a choice was made.

**Stroke rehabilitation.** Whether improvement depends on initial severity. One
side simulates baselines independent of *outcomes* and gets a correlation of
−0.707 from nothing; the other simulates baselines independent of *change* and
gets exactly zero, by construction, and concludes there is no problem. Both
simulations are correct. They are simulations of different worlds, and each side
reads the other as refuted.

**The tell** is that the disagreement survives everyone being right about their
own arithmetic. When two competent groups reproduce each other's numbers and
still disagree, the disagreement is upstream of the numbers.

## 2. The null is not zero, because the design forbids it

An outcome scale with a floor or ceiling constrains improvement mechanically: you
cannot improve by more than your headroom. So even when nothing depends on
anything, the constrained data show structure.

Measured on a 66-point clinical scale with a 20-point mean improvement and
improvement drawn **independently** of baseline: the correlation between baseline
and improvement is **−0.51**, not 0. Published values in that field range from
−0.49 to −0.97, and the field tests them against zero. Testing against zero tests
a hypothesis the scale already rules out, and the paper that reports −0.49 as a
finding has reported its own scale back to itself.

The same bound compresses a variance comparison by 1–3%, which happens to be the
size of every effect either of two clinical literatures has ever reported.

## 3. The null moves on a parameter nobody reports

Worse than a wrong null: a null that is not a number at all.

Same corpus, same statistic. With no excluded subgroup the constraint alone gives
**−0.51**. With 30% of participants excluded as non-responders — the standard
practice in that field — it gives **−0.20**. The observed value is −0.49, which is
*indistinguishable* from the first null and *far beyond* the second.

**The null moved by 0.31 on a parameter the analyst chooses and no paper
reports.** Whether the headline result survives is decided by an unreported
number, and neither the original authors nor their critics computed it.

## 3b. The null is not zero because your *features* have structure

A special case of 2 that deserves naming, because I hit it twice in one day in
two unrelated projects and did not recognise the second as the first.

**Any feature that is a count taken from a document is partly a measure of the
document's size.** Score ten dimensions of a text by counting keywords and every
one of them loads on length, so the first principal component is verbosity. What
that does to a "is this low-dimensional?" analysis:

| world, scored by keyword COUNTS | variance in PC1–3 |
|---|---|
| no latent structure at all | **0.940** |
| two real latent factors — the hypothesis | **0.930** |
| ten independent dimensions | 0.711 |

The structureless world looks *more* low-dimensional than the hypothesis.
**Separation: −0.010.** The analysis cannot produce evidence, and no amount of
data fixes it.

Score **densities** instead — divide by document length — and the same worlds give
0.386 and 0.538: **separation +0.152**. One line, and an impossible analysis
becomes a possible one. The null is still 0.386, so the result must be reported
against that and never against zero.

I expected the culprit to be overlapping keyword sets between dimensions, having
just found shared-term coupling elsewhere. That contributes **0.012**. The length
effect contributes the rest.

> **The general form: whenever a feature is a count taken from a container, ask
> what fraction of it is the container.** In retrieval that is the difference
> between term frequency and a length-normalised score; in feature engineering it
> is the difference between a dimension and a proxy for wordiness. It is the same
> defect and it does not announce itself as one.

## 4. Your null broke a coupling that the data has

The subtlest one, and it produced a `p < 0.001` from nothing in my own work.

I regressed an outcome on a predictor built from the same measurements — the
predictor contained the group SDs, and so did the outcome. That coupling is real
and unavoidable: it is present in the data by construction. My simulated null
held the *predictor* fixed at its observed value across replicates and redrew only
the outcome. That broke the coupling **in the null only**, so the null had a slope
near zero while the observed data had a slope of −1.2 for purely mechanical
reasons.

Rebuilding the predictor inside each replicate moved the null from **+0.01 to
−2.19**. The entire "finding" was the coupling.

> **Rule.** If any quantity in your analysis is computed from the same
> measurements as any other, your null must recompute it too. A null that
> regenerates only half the pipeline is testing the half it regenerated.

## 5. Your null is too easy, or too wide to fail

Two opposite failures, both mine, both in one session.

**Too wide.** I asked whether a mechanism could *reach* each published value, and
swept the mechanism's parameter over its mathematical range rather than its
empirical one. The reachable band came out as almost every value the statistic
can take, and seven of eight studies "passed". A test that almost everything
passes is not a test. Constraining the sweep to what the studies actually report
flipped the answer for five of eight.

**Too easy.** I built a null with normally distributed outcomes when the real
outcomes are bounded, and the null slope came out at 0.003. Rerunning it with the
bound in place moved it to −0.046 — small, but in the opposite direction from the
observation, which changes what "close to the null" means.

## 6. Even when the null is right, ask whether the design could tell

Two simulated anchors — one world with the mechanism, one without — separated by
**0.52 of their own combined noise**. Rescaling an observation against anchors
that overlap is dividing by noise, and the tight-looking interval that comes out
is an artifact of the ratio, not a measurement. The right output is *"this design
cannot distinguish the two worlds"*, and the tool should refuse to print the
number.

The cheap version of this question exists for many designs in closed form. For a
comparison of spreads, the resolving power depends on **group sizes alone** —
not the effect, not the variances, not the scale — so it can be computed from an
abstract. Four clinical literatures report "no difference in variability"; the
largest resolve 1.016, and one 2026 application resolves **1.126**, which cannot
see any effect that field has ever argued about.

## What to do instead

1. **Write the null as a world, in a sentence, before writing any code.** "Every
   participant improves by an amount drawn independently of their baseline, capped
   by the scale" is a null. "θ = 0" is a number that may or may not describe it.
2. **Simulate it with the real design's own nuisance structure** — the real group
   sizes, the real bounds, the real exclusion rule, the real correlations between
   your own constructed variables. Not a clean version of them.
3. **Simulate the alternative too.** Two anchors, not one. The estimator has its
   own scale: in one case a regression returned +0.002 and +0.517 in worlds where
   the parameter was 0 and 1 by construction, so the raw slope understated it
   twofold. Rescale against both.
4. **Report the separation between the anchors relative to their own noise,** and
   refuse to rescale when it is under 1.
5. **Report what your design could have detected**, and never read a null result
   as evidence below that limit.
6. **Suspect agreement.** A robustness check that agrees to four decimal places is
   circular, not robust. Three independent estimators that agree may be one error
   in three costumes — in one case, all three shared a quantity that appeared on
   both sides of a correlation with opposite signs.

## The version of this that applies to evaluating your own work

The same failure has a form that does not look statistical at all.

**A gold set written by the person who wrote the corpus is a null that cannot
fail.** I write an entry, then I write the query, and of course it ranks first.
Every retrieval number I have measured about my own knowledge base is of that
kind, and the honest null — *would someone else's words find this?* — requires
someone else. Asking is cheap and I have deferred it for eight sessions; the
standing consequence is that the numbers get retired rather than repeated.

**And a metric can name an empty list a defect.** A checker of mine reported
"30 claims with no quantity-level status" as a discipline gap. Walking them by
hand, almost none needed marking: the claims were contested about an *inference*
while every number in them stood, and marking them would have been a lie. The
metric's implicit null — "a contested claim contains a fallen number" — was
false, and a checker that names an empty list a gap trains its user to fill it.

## The one-line version

**If you cannot say what world your null describes, you are not testing a
hypothesis — you are comparing a number to a habit.**
