<!--kb
id: detectors-that-find-signal-in-null-worlds
labels: kind:synthesis, area:statistics, area:replicability-and-selective-reporting, known-answer-controls, meta-science
triggers: before I trust this detector or validation; my statistic says there is an effect, could it say that with no effect; how to test an estimator with a known answer; a correlation that validates a predictor looks too good; baseline change correlation; excess significance count; replication forecast calibration; z-curve validation; careless responder flag rate; which instruments in the KB have measured operating characteristics
verified: 2026-11-05
review_by: 2027-05-05
confidence: verified
evidence: every number below was recomputed by maria in the linked instance-papers records; none is quoted from a paper
-->

# Detectors that find signal in null worlds — a catalogue, and the one control that catches them

Author: maria, 2026-11-05. Every case below was found the same way: feed the instrument a world where the answer is
known to be "nothing", and see what it says. Ten checks across six records and five fields returned signal from
nothing (`python tools/kb.py instruments --verdict artifact`); four more instruments were calibrated and passed.
The point of this entry is the shape, so that the next instrument gets the control before it gets believed.

## The cases (numbers from the records; the record is the source)

| instrument | null world fed to it | what it returned | record |
|---|---|---|---|
| r(baseline, change) as evidence of proportional recovery | ceiling only, outcomes shuffled | r = -0.869 | `hope2019-not-so-proportional` |
| r(baseline, change) as evidence of heterogeneous response | true rho = 0, reliability 1.00 | rho = -0.141 | `mccutcheon2022-reappraising-variability` |
| mean-variance coupling slope | additive effect + scale floor | slope .349 (looks like coupling) | `maria2026-antidepressant-variability-recalibration` |
| many-analysts agreement headline | each hypothesis column permuted | 0.20 | `botviniknezer2020-narps` |
| Mahalanobis careless-responder flag (nominal .001) | no outliers: copula of the clean data | flags 12.5% | `vandam2024-ime-psychometrics` |
| expected positive trials from single-test power | NO reporting bias, 4 outcomes/abstract | 96.4 'expected' vs 65.7 assumed | `coronadomontoya2016-mindfulness-positive-results` |
| z-curve validated by outcome-stratified samples | z permuted across rows | r(ERR, RR) = .645; trivial statistic .945 | `roseler2023-zcurve-validation` |

Instruments that PASSED their known-answer check in the same sessions (so the control is not a ritual that always
fails): TIVA at 5 studies (4.3% false flags; 78% power vs a null file drawer), the Mantel test (FPR .07; but 14% power
for diffuse signal), the pooled-weight variance estimator (bias .0035), Pawel-Held SH forecasts under honest selection.

## Four mechanisms, and which cases they explain

1. **The statistic shares a term with the outcome.** change = Y - X correlated with X; a ratio regressed on its own
   numerator; an inverse-variance weight that contains the effect. (proportional recovery, heterogeneous response,
   variance pooling.) Check: does the statistic have a non-zero expectation when X and Y are independent?
2. **A bound or floor creates the pattern.** Truncation removes variance from the arm that improves more.
   (mean-variance coupling.) Check: simulate the bound with no effect.
3. **The null used for comparison is not the one the data came from.** A chi-square cut for multivariate normal data
   applied to skewed Likert items; single-test power compared with an any-of-k positivity rule. (Mahalanobis flag,
   excess-positive count.) Check: rebuild the null from the data's own marginals / the analysis's own definition.
4. **The validation sample is constructed from the outcome.** Mixing two fixed pools in a chosen ratio makes ANY
   statistic that differs between the pools track the ratio with r near 1. (z-curve.) Check: permute the input,
   substitute a trivial statistic, and validate where the outcome varies naturally.

## The control, as a procedure

1. Write down the instrument's claimed reading ("r < 0 means proportional recovery").
2. Build the null world from the data's own structure: permute the link, keep the margins; or simulate the design
   with the effect set to zero; or substitute a trivial statistic.
3. Run the instrument exactly as published. If it returns the headline (or a sizeable fraction of it), the
   headline is not evidence. Record it as an `instrument_checks` entry (zoo-paper-record 1.7) with `verdict: artifact`.
4. Run it at least once with the effect injected, so you also know its power (a control that can only fail is
   not a control).
5. One permutation is one draw: in the z-curve case a single permutation gave r = -.30 and another .645. Report the
   distribution over permutations, not one.

## What this entry does not claim
That the papers' effects are absent. Several survive once the right null is used (coronadomontoya2016: the excess
positives shrink from 1.6x to about 1.25-1.5x but remain). The claim is narrower: the instrument as published could
not have told.

## See also
- `philosophy-of-science/the-null-is-a-modelling-choice.md` -- which null to build is itself a modelling decision;
  this entry is the operational half (build it, run the instrument in it, record the verdict).
