<!--kb
id: standardised-effect-size-depends-on-the-unit
labels: statistics, effect-size, measurement, evaluation, llm-evaluation
triggers: Cohen's d of 16; is this effect size plausible; effect size across random seeds; d for a proportion; standardised mean difference of an LLM benchmark; effect size is huge because variance is tiny; averaging over cases then computing d; how big is a prompting effect; Hedges g on five seeds; should I report d or a risk difference
verified: 2026-09-30
-->

# A standardised effect size is only as meaningful as the unit it was standardised over

Status: active. Author: maria. Written 2026-09-30 from the recomputation in
`instance-papers/papers/arslan2026-bodhi-engineering/reanalysis/` (two stdlib scripts, one with a
known-answer null control).

---

## The claim

Cohen's d = (difference in means) / (a standard deviation). The *choice of that SD* is a choice of
**unit**: per response, per case averaged over repeats, or per seed averaged over cases. The mean
difference is identical across these choices. The SD is not, and it shrinks roughly with the square root
of how much averaging happened first. So **the same behaviour change can be reported as d = 0.7 or d = 6**
without anyone computing anything wrong, and the paper rarely says which unit it used.

## The measured case

A clinical-LLM prompting paper (BMJ Health Care Inform 2026, e101877) reports "very large effect sizes"
on 200 vignettes x 5 seeds: context-seeking d = 16.38, hedging ("humility") d = 5.80. Its Table 1 prints
mean +- SD across the five seeds, and **all eight printed d values reproduce to rounding as difference /
pooled SD of the five seed means**. The same rates standardised per response:

| metric | rates | printed d (seed unit, n = 5) | per-response d (binary) |
|---|---|---:|---:|
| context-seeking, model A | 7.8% to 97.3% | 16.38 | 4.04 |
| context-seeking, model B | 0.0% to 73.5% | 19.54 | 2.36 |
| hedging, model A | 1.7% to 21.9% | 5.80 | **0.66** |
| hedging, model B | 0.0% to 4.1% | 1.16 | **0.29** |

A simulation of the design (`cohens_d_by_unit.py`) gives, for the first row, d of about 4 per response,
about 9 on case means, about 6 paired on cases and about 68 on seed means. The reported 16 is simply
where that paper's seed-to-seed spread happened to land. The null control (identical arms) returns
d near 0 under every unit, so the spread comes from the unit and not from the simulation.

## Why it happens and why it matters

- **Averaging divides the SD by sqrt(k)** before d is computed. A d on 200-case means is not comparable to
  a d on individuals, and neither is comparable to Cohen's 0.2 / 0.5 / 0.8 conventions, which were
  written for individuals.
- **For a binary outcome, per-unit d is bounded** by the rates. 7.8% to 97.3% cannot exceed about 4 per
  response. A d of 16 on a binary behaviour is by itself proof that someone averaged first.
- **Seed-level SD measures reproducibility of the pipeline**, which is worth reporting, but under its own
  name. Dividing by it turns "the mean is stable across seeds" into "the effect is enormous".
- **Hedges' g does not rescue it.** With n = 5 per arm the small-sample factor is 0.90. The reported
  values match the uncorrected d, so a correction said to be applied was not visible either.

This is the same move as "rescaling by noise" in `philosophy-of-science/the-null-is-a-modelling-choice.md`,
failure 6: dividing a difference by a quantity that is small for reasons unrelated to the effect.

## What to report instead

1. **The risk difference or mean difference in natural units, with an interval clustered on the sampled
   unit** (cases, or patients). The paper above prints these too (+89.6 pp, +20.3 pp), and they are the
   honest numbers.
2. If a standardised effect is wanted, **state the unit in the same sentence** ("d on per-response binary
   outcomes") and use the unit a reader will compare against.
3. **Report seed-to-seed SD separately** as a reproducibility statistic.
4. **Sanity bound:** for a binary outcome, compute (p1 - p0) / sqrt((p0 q0 + p1 q1) / 2). If the reported d
   exceeds it, the unit is not the response.

## Related

- `statistics/comparing-dispersion-between-two-groups.md`: another case where a ratio statistic's
  meaning is set by a reporting convention.
- `instance-papers/CONTRIBUTING.md` §3: "Ratios of near-zero quantities are not effect sizes."
