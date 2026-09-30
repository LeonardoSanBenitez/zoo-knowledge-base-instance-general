<!--kb
id: counterfactual-influence-audits
labels: evaluation, multimodal, causal-inference, oversight, measurement
triggers: does the model actually use the image; benchmarking a general vision-language model on medical images; evaluating an open VLM on chest x-rays or radiology; did the agent change its answer because of the peer; how do I detect that an input influenced an output; image swap test; modality reliance; is my VLM answering from the text; flip rate above noise floor; LLM judge reading the transcript is not enough; private re-query; sensitivity versus accuracy; shortcut cue test; the model is right but for the wrong reason
verified: 2026-09-30
-->

# Counterfactual influence audits: to know whether X used Y, change Y and nothing else

Status: active. Author: maria. Written 2026-09-30 from three primary sources read in full
(`instance-papers/papers/cajas2026-modalens`, `cajas2026-agents-catching-agents`,
`huang2026-reward-hacking-research-agents`) and one recomputation from committed rows.

---

## The claim

"Did the model use input Y?" and "was the model influenced by Y?" are **causal** questions. Accuracy, a
transcript, a rationale, or a judge reading all three cannot answer them, because each is compatible with
Y having been used and with Y having been ignored. The only direct answer is a **paired
counterfactual**: the same item rendered twice, identical except for Y, and the rate at which the output
changes.

| question | counterfactual that answers it | measured example |
|---|---|---|
| Does a VLM use the image when a report is present? | swap the image for another study's, keep report and question fixed | MedGemma-27B: answer changes on 4.3% of 44,786 trials with report, 20.9% without |
| Did the agent adopt the answer because peers asserted it? | re-ask the same agent privately, with no transcript | referee precision 0.77-0.88, FPR 0.13-0.21 on chest X-rays; a transcript-only judge collapsed to FPR 0.94 |
| Is a "shortcut cue" moving the model? | same item with and without the cue, against the model's own test-retest disagreement | image cues within 0.029 of a 0.17 noise floor (n = 834): the cue does nothing alone |

The asymmetry to remember: **a judge given more of the producer's output is a better reader of that
output, not a better detector of influence.** In the benchmaxxing imaging lane the transcript-only judge
matched the naive gate on all 35 cases, because the peer's asserted read was constant and the film was
never in its prompt.

## Six ways a counterfactual audit still goes wrong

1. **No noise floor.** At temperature > 0, or even at 0 across infrastructure, an item's output can change
   when nothing did. Query the unmodified input twice and subtract. The floor is itself a modelling choice
   (`philosophy-of-science/the-null-is-a-modelling-choice.md`). Benchmaxxing's floor is resampled above
   temperature 0, so it is not conservative in either direction, and the paper says so.
2. **The readout decides the magnitude.** First-token logit vs token family vs generated answer moved one
   ModaLens rate from 10.3% to 17.4%. The direction held and the number did not. Validate the readout
   against generated answers, or do not report a rate.
3. **The prompt layout decides the magnitude.** Text block before image instead of after halved
   ModaLens's report effect (+12.4 to +7.8 points, same trials). A flip rate is a property of (model,
   prompt), never of the model alone.
4. **Ceilings hide in the pooled rate.** A finding the model affirms on 98-100% of trials cannot flip, so it
   contributes zeros that mean "cannot move", not "robust". Report per-item-class rates.
5. **One-directional plants measure priors.** If every planted wrong answer has the same polarity ("no"),
   and no arm asks the question where the true answer is "no", then "correct alone" cannot be told apart
   from "always says yes". This is found in benchmaxxing's CheXpert arm (150/150 planted "no", no
   device-free control). It is not a flaw of the adoption rate. It is a limit on the gloss "it overrode
   what it saw".
6. **Sensitivity is not correctness.** A swap audit tells you the output *moves with* Y. Whether moving
   is *right* needs ground truth about Y. If the labels were derived from the other modality (report-derived
   radiology labels), "accuracy drops when the image is added" means "moves away from the report", which
   may be the correct behaviour. ModaLens states this in its abstract. Most papers would not.

## Cheap controls that make the audit trustworthy

- **Content-free text of matched length.** Neutral prose alone moved ModaLens's flip rate from 10.3% to
  8.2%. Part of any "report effect" is "text is present".
- **Answer-bearing vs answer-removed text.** Deleting the sentences that mention the queried finding raised
  it to 11.6%.
- **Honest-peer arm.** Peers asserting the *correct* answer make any "adoption" flag a genuine false
  positive. Without it, a referee's precision reduces algebraically to its own label (benchmaxxing
  withdrew two such arms).
- **A warning prompt is not a control.** "The report may be wrong" changed nothing (+0.28 points, CI
  spans 0).
- **Cluster the interval on the unit that was sampled** (patients, not images: 35 NIH images came from 10
  patients).

## Where this sits in the KB

- `multi-agent-systems/conformity-cascades-in-agent-committees.md`, the social version of the same
  question.
- `multi-agent-systems/independent-replication-and-correlated-error.md`: agreement between agents who
  saw the same input is near-uninformative. The private re-query is how you manufacture the "did not see
  it" condition.
- `philosophy-of-science/the-specification-execution-gap.md`: a prompt instructing "look at the image"
  is a specification. The swap audit measures the execution.
- `ai-evaluation/evaluation-integrity-when-the-agent-controls-the-evidence.md`: the same logic when the
  producer is adversarial.
