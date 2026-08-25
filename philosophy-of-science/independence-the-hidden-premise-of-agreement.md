<!--kb
id: independence-the-hidden-premise-of-agreement
labels: meta-analysis, epistemology, measurement, ensembles, replication
triggers: two studies agree, is that evidence; I2 is zero, what does that mean; my ensemble members agree so the answer must be right; how much does replication buy if the replicators share a method; several models gave the same answer; independent confirmation; why did heterogeneity vanish; the analysts all used the same software; convergent validity; does agreement between two sources mean anything; correlated errors; when is a second opinion worth having
verified: 2026-08-25
-->

# Independence is the hidden premise of every argument from agreement

Status: active. Author: maria. Written 2026-08-25, out of finding that a claim of
mine rested on exactly the fallacy it describes.

---

## The claim

Whenever two or more sources agree and you treat the agreement as evidence, you
have assumed their errors are independent. That premise is almost never stated,
is usually false to some degree, and **when it fails the statistics designed to
detect disagreement report the failure as good news.**

This is not a subtle point about correlation structure. It is that
**the observable signature of "our sources are independent and correct" is
identical to the observable signature of "our sources share a defect."** No
amount of agreement can separate them. Only knowledge of *how* the sources were
produced can.

## Why the usual diagnostics cannot see it

| diagnostic | what it is a statistic about | what it is blind to |
|---|---|---|
| I² / Cochran's Q | between-study variance **beyond sampling error** | shared *implementation* or *method* error |
| ensemble variance / self-consistency | disagreement among members | anything the members inherited from a common ancestor |
| inter-rater reliability | rater disagreement | a rubric that misleads all raters the same way |
| a passing replication | the second run got the same answer | both runs sharing a pipeline, a dataset version, a convention |

I² is the clearest case and worth stating precisely, because it is quoted as if
it measured trustworthiness. **I² estimates the share of observed variance not
attributable to sampling error.** Shared implementation error is not sampling
error; it is a *common shift*, which reduces observed variance. So a shared bug
pushes I² **toward zero — exactly where genuine agreement pushes it.** An I² of 0
across two studies running the same program is not convergent validity. It is a
monoculture looking at its own reflection.

## The instance that produced this entry, stated against myself

`maria2026-executability-denominators#c3` (2026-08-24) claimed that harmonising
denominators *creates* agreement the printed numbers hide: two large notebook
corpora, Samuel & Mietchen 2024 and Pimentel 2019, converging to within 0.2
percentage points at the corpus denominator, **τ = 0, I² = 0.0%**. I wrote it up
as a demonstration that careful denominator work reveals real convergence.

The next day I found that one of the two numerators counted 815 executions in
which **nothing had been compared** — the pipeline flags "identical results"
whenever its comparison loop runs zero iterations
(`software-engineering/silent-data-loss-patterns.md`, Pattern 2). Corrected, the
two corpora differ by a factor of 13.

And the second branch is worse than the first. **Samuel & Mietchen state they
used Pimentel's reproducibility code.** So either the numerator was 13.7× too
high and there never was agreement, or the defect is inherited and my I² of 0 was
measuring *two runs of one bug*. Both branches refute the claim, so I did not
need to know which held in order to retract — but only the second is
instructive, and it is the one I could not have seen from the numbers.

**What would have caught it:** one question, asked before computing anything.
*Were these produced by the same program?* It is in the methods section of one of
the two papers. Full details: `instance-papers/papers/maria2026-vacuous-reproduction-flag/`.

## A second way agreement fails, with no dependence involved

Added 2026-08-25, hours after the entry, by applying it to my own new result.

Two studies can be perfectly independent and their agreement still carry no
information — if the agreement is **tighter than the sampling error permits.**

Two by-hand reproduction studies, different fields, different teams, different
criteria, no shared code: **20/59 = 33.90%** and **21/62 = 33.87%**. They agree
to 0.027 percentage points. The standard error *of the difference* is **8.6
percentage points**. Under independent sampling, agreement that close is about a
1-in-400 event.

Which is not a small miracle. It is a **selection effect**: I did not pre-specify
the comparison, I noticed it *because* the numbers matched. With twenty rates on
a page there are 190 pairs, so the probability that *some* pair agrees this
tightly is about 0.38.

> **The tell is `|difference| ≪ SE(difference)`.** When two estimates agree far
> more closely than their own precision allows, you are looking at noise that
> happened to cancel — or at a comparison you chose after seeing the numbers, or
> at one estimate tuned toward the other. None of the three is corroboration.

The companion question, which is cheaper still and which almost nobody asks
before comparing two rates:

> **Could either study have detected the difference you are calling absent?**

At n = 60 per study, the smallest difference detectable at 80% power is about
**24 percentage points**. If the whole range under dispute is thirty points, the
instruments cannot adjudicate anything, and both their disagreements and their
agreements are uninformative. Their *internal* contrasts usually remain fine —
which is an argument for trusting within-study comparisons and distrusting
between-study ones, in any literature whose studies are small.

## The same shape in four other places

1. **LLM ensembles and juries.** Models sharing a base model produce correlated
   errors, so ensemble agreement overstates reliability, and majority voting
   over near-clones buys far less than the vote count implies
   (`instance-papers/papers/kim2025-correlated-errors/`). The remedy people reach
   for — add more members — makes it worse if the members are drawn from the same
   family, because the apparent confidence rises while the effective sample size
   does not.

2. **Many-analyst studies.** Breznau 2022's 73 teams look like 73 independent
   analyses; they share a data file, a construct definition, and a literature.
   The dispersion they measure is real, and it is a *lower* bound on the
   dispersion you would see if the shared parts also varied
   (`instance-papers/papers/breznau2022-hidden-universe/`).

3. **Replication that reuses the pipeline.** Re-running an analysis on the same
   data with the same code tests *transcription*, not *correctness*. This is the
   most common thing called replication and the one most often quoted as if it
   were the strongest.

4. **Evaluating your own knowledge base.** Queries written by the person who
   wrote the entries share the entries' vocabulary; the retrieval score then
   measures the shared vocabulary and not the retrieval
   (`information-retrieval/evaluating-your-own-knowledge-base.md`). I have been
   living with this one knowingly and it is the same fallacy dressed as a metric.

## What to do instead — four questions, cheap, in order

1. **Trace the ancestry before the arithmetic.** For each source: what code, what
   data version, what convention, what upstream did it inherit? This is usually
   one paragraph in a methods section and it decides whether the aggregate means
   anything. Do it *first*, because doing it afterwards means discarding work.
2. **Prefer one source with a different lineage to three more of the same.** A
   single study using an independent implementation is worth more than several
   sharing one. In practice this inverts the usual weighting: after the defect
   above, Trisovic 2022 — whose re-execution used a separate implementation —
   became the only large automated study in that literature with an unimpeached
   numerator, and its weight in any synthesis should *rise*.
3. **When you cannot establish independence, say what you are pooling over.**
   "Pooled across three studies" and "pooled across three runs of one method"
   are different objects; the first is an estimate, the second is a precision
   statement about one method. Both are legitimate; conflating them is not.
4. **Treat agreement asymmetrically.** *Dis*agreement between two sources is
   strong evidence that at least one is wrong, and it does not require
   independence to be informative. *Agreement* requires independence to be
   informative at all. So disagreement is the cheaper signal and should be sought
   deliberately, which is the honest argument for adversarial replication over
   confirmatory replication.

## The one-line version

**Disagreement is informative whatever the sources share. Agreement is
informative only to the extent that they share nothing.** Before quoting a
pooled estimate, an ensemble vote or an I², write down what the sources
inherited — and if the answer is "the same program", you have one measurement
with a confidence interval, not several with a consensus.
