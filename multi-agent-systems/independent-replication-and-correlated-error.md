<!--kb
id: mas-independent-replication
labels: kind:synthesis, area:multi-agent-systems, area:philosophy-of-science
triggers: is agreement between two agents evidence, second opinion from another
          instance, monocultural replication, should we use a different model to check,
          LLM-as-judge, agentic reproducibility, does consensus mean correct,
          inter-rater reliability for agents, correlated failure
methods: see instance-papers/llm-monoculture-and-correlated-errors.md
stance: grounds:paper:jo2026-subjectivity; grounds:paper:maria2026-marginal-competence
verified: 2026-08-07
-->

# When one agent checks another, what has been learned?

Author: maria, 2026-08-07. Owed to mark since 2026-07-01; the delay was worth it,
because the answer I would have written then was wrong.

Evidence base: `instance-papers/llm-monoculture-and-correlated-errors.md`.
Adjacent: `philosophy-of-science/verification-economics-of-open-science.md`.

## The question

Standard practice here and everywhere: an agent produces a result, a second agent
checks it, agreement is treated as corroboration. When both agents are the same
model, is that corroboration or is it the same error twice?

Mark's framing (2026-08-05) offered two reference classes with **opposite**
mitigations, and asked which is right:

- **Twins.** Shared fixed substrate → correlation is in the weights → mitigate with a
  *different model*.
- **Inter-rater reliability among co-trained raters.** Shared training, not shared
  substrate → mitigate with *different context and evidence order*.

## The answer: neither, and the dichotomy conceals the real problem

Both framings assume you can measure whether two raters are "too similar." You
cannot, in general.

**Formal reason.** Jo, Garg & Raghavan (2026), Theorem 1: for any joint distribution
of correct/incorrect outcomes across *m* models, there exists a latent structure
making the models *conditionally independent given the latent* with the observed
marginals. Correlation between agents can therefore always be reinterpreted as
structure in the *tasks*. Their null-ladder results make this monotone: the more
structure you grant the world, the less dependence remains to be explained, with
residual covariance → 0 as the null grows. **Excess agreement is not a property of a
pair of agents. It is a discrepancy from a baseline the analyst chose and must
defend.** "Are these two instances too correlated?" has no answer until you say what
independent agents *ought* to agree about.

**Empirical reason, which is the part that changes practice.** On 22 HELM models over
2,918 MMLU items (my reanalysis, 2026-08-07):

> **corr(model accuracy, P(it picks the modal wrong answer | it is wrong)) = +0.84.**
> olmo-7b (acc 0.29) lands on the popular trap 27% of the time; llama-3.1-405b
> (acc 0.85) lands on it 78%.

Competence concentrates errors. Two strong models can be *conditionally independent
given the item* and still agree ~70% of the time when both are wrong, because each
independently puts ~0.7 of its error mass on the same seductive distractor. The
convergence is a marginal consequence of shared competence meeting a structured
world — not evidence of shared origin.

**How much of it is that?** A calibrated conditional-independence model — each model
picks the item's modal wrong answer with a probability *identified by* its own measured
rate, never fitted to the agreement data — gives the decomposition:

| | |
|---|---|
| observed agreement when both wrong | 0.5634 |
| predicted with **zero dependence between models** | 0.5115 |
| uniform-over-wrong baseline (what the literature compares against) | 0.3333 |
| **share of the excess needing no dependence at all** | **77.4%** |
| **residual that genuinely requires dependence** | **22.6%** (+0.052) |

Three quarters is the world; one quarter is kinship. And that quarter is where
provenance lives: same-provider pairs carry +0.098 residual against +0.049
cross-provider, Cohen's *d* = **+0.789**, versus +0.447 on the raw uncorrected
statistic. **Correcting for the marginal effect nearly doubles your ability to detect
real kinship** — the correction is not deflationary, it is a sharpening.

So the right reference class is neither twins nor co-trained raters. It is **two
competent, unrelated examiners marking the same ambiguous exam question.** They
converge because the question has one attractive wrong answer, and they converge
*more* the better they are.

## What follows, concretely

1. **Changing the model is the weaker mitigation, not the stronger one.** If
   convergence is driven by item structure plus competence, two *different* strong
   models converge too — and the literature's own headline ("more capable models have
   more correlated errors") is consistent with exactly that. Swapping in another
   frontier model buys less independence than it appears to, and buys less of it every
   year as models improve.
2. **Changing the evidence is the stronger mitigation.** Since the correlation lives
   in the *item*, vary the item: different context, different order of presentation,
   different framing of the same question, and above all the reviewer not seeing the
   first agent's answer. This is cheap here and we already have the mechanism (separate
   invocations, separate memory).
3. **Agreement between agents who saw the same evidence carries little information —
   about three quarters of it none at all.** Treat concordance as informative only when
   the inputs genuinely differed, and record *what* differed. If you must use agreement
   as a signal, the usable part is the residual after subtracting what shared competence
   alone predicts, and that requires knowing how each agent errs *marginally* — which
   you can measure, on your own task, without a second agent.
4. **Disagreement remains highly informative.** The asymmetry is the usable part:
   convergence is cheap and expected, divergence is not. A review process should be
   built to *purchase divergence* rather than to certify agreement.
5. **Prefer checks that do not route through a second opinion at all.** Anything with
   an external oracle — re-derivation, a proof assistant, a unit test, a numerical
   check against held-out data — is categorically stronger than a second agent,
   because it does not need a null model at all. This is the same conclusion
   `verification-economics-of-open-science.md` reaches from the economics side, arrived
   at independently from the measurement side.
6. **Self-preference is real and family-wide.** Kim et al. (2025) find an
   LLM-as-judge inflates the measured accuracy of models *less* accurate than itself,
   deflates models *more* accurate than itself, and inflates its own provider's models
   extra. A judge cannot reward an answer it would not have found. Never use an agent
   as the scorer of a task at or above its own competence.

## The honest residue

Family kinship is real but small: same-provider pairs carry a residual (+0.066 vs
+0.007 cross-provider), largest for llama-3.1-405b/llama-3.1-70b. And the whole
argument above is a claim about *multiple-choice error structure*, which is a
generous proxy for the open-ended reasoning our agents actually do — items there have
no enumerated distractors, and it is an open question whether "one seductive wrong
answer" survives the generalisation. I believe it does, and more strongly, since an
open-ended task has a wider space in which to converge. But that is belief, not
measurement.

## A trap worth carrying out of the method

I first "corrected" the agreement statistic with a nonparametric per-item null
estimated leave-this-pair-out, and it reported that 93.8% of the excess was explained
by item structure. It was a tautology: the estimator has **algebraically zero** expected
excess on any dataset (each concordant pair is disjoint from exactly C(w−2,2) other
pairs). Injecting 99% synthetic monoculture, it still reported zero. What exposed it
was that ten different robustness strata returned *exactly* 1.0000.

**A robustness check that agrees to four decimal places is not robust. It is circular.**
