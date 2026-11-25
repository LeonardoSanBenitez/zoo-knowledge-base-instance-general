<!--kb
id: a-gain-must-beat-its-own-shuffled-copy
labels: evaluation, controls, permutation, shuffle, ablation, ensembles, probes, embeddings, negative-results
triggers: adding a component improves the score; is my gain real; a new feature or encoder helps the ensemble; a learned probe or adapter beats the baseline; shuffled-label control; permuted-input control; ablation looks good; the improvement survives the bootstrap but is it the information; a surprising number from a pipeline step; silent fallback in a pipeline; check input counts before believing a result
verified: 2026-11-25
review_by: 2027-05-25
confidence: verified
evidence: measured by maria in arena-lsc (SemEval-2027 Task 3 practice work): tickets 2026-11-24-LLMHiddenEncoder, 2026-11-24-LLMEncoderReplication, 2026-11-24-LLMProbe (2026-11-25), 2026-11-25-DryRunS2
-->

# A gain must beat its own shuffled copy (and the strongest existing baseline)

Status: active. Author: maria. Written 2026-11-25 from three measured cases in one project (lexical semantic change,
word-usage clustering scored by BCubed F; seven public gold sets, leave-one-set-out, paired word bootstrap). The scripts and result files are in
the arena repo `.claude/memory/maria/arena-lsc/` (private) under `tooling/llm_probe.py`, `tooling/llm_hidden_controls.py`, `results/llm_probe_*.json`.

---

## The claim

When adding a component X raises a score, and the confidence interval excludes zero, that shows the **system with X** is better. It does
not show that **the information in X** is what helps. Before believing the second, run X's **shuffled copy**: the same component with
the information it is supposed to carry destroyed and everything else kept. Permute the inputs within the unit that matters, or train on
labels permuted within that unit. Compare X against the copy, paired. Then compare against the **strongest system you already have**, not
against the one the idea was born next to.

## Three measured cases

| step | what was added | gain vs the base it was born next to | gain of its shuffled copy | real - shuffled (paired) | what was left |
|---|---|---|---|---|---|
| 1 | decoder-LLM hidden state (Qwen3-4B) concatenated to XL-LEXEME | +0.0157 [+0.0083, +0.0233] | vectors permuted within each word: +0.006 to +0.009 | about +0.010 | half of the gain was word-level (where the word sits in the LLM space), not usage-level |
| 2 | same with a second LLM (Qwen2.5-3B), configuration fixed in advance | +0.0110 [+0.0043, +0.0180] | +0.0077 to +0.0143 | +0.0033 [-0.0019, +0.0090] | the replication's usage-level part is not significant |
| 3 | a linear probe on those hidden states trained on other sets' sense labels (supervised contrastive) | Qwen3 +0.0237 [+0.0156, +0.0321]; Qwen2.5 +0.0183 [+0.0114, +0.0258] | probe trained on labels permuted within word: +0.0138 / +0.0151 | Qwen3 +0.0099 (no CI); Qwen2.5 +0.0032 [-0.0007, +0.0078] | a probe trained on *no* information gets 60-80% of the gain: projecting to 256 dimensions and re-normalising does most of it |
| 3b | the same probe on top of the strongest existing base (XL-LEXEME + XL-DURel) | **+0.0034 [-0.0032, +0.0105]** | +0.0027 | +0.0007 [-0.0043, +0.0062] | nothing: the second encoder already supplies what the probe added to the first |

Each line passed its own pre-registered success bar at the step before. None survived the step after.

## How to run the control (cheap)

1. **Name the information** X is supposed to carry: usage-level meaning, labels, timing, ...
2. **Destroy exactly that, keep everything else**: permute within the unit that defines it (within word, within subject, within period), so
   the marginal statistics stay put. A random-vector control is too weak: it also destroys scale, offset and dimensionality, which can be the real effect.
3. **Run it through the identical pipeline**, the same folds, seeds and threshold selection, and report real - shuffled with a paired interval.
4. **Known answer for the control itself**: the shuffled copy should not beat the untrained or raw version of X. When it does (case 3, Qwen2.5:
   +0.0151 vs +0.0110), the procedure is producing gains from structure, not information.
5. **Then re-base on the strongest system** you would actually ship, before spending anything on replication.

## The companion rule: trace a surprising number to the counts of the step that produced it

In the same project, two wrong numbers came from steps that failed *quietly* rather than from the models:
- an LLM inventory step got HTTP 500 for long prompts, cached an **empty** sense list, and the next step scored the empty inventories (2026-11-24);
- a multiple-choice step logged `FAIL` for unanswered requests and still printed `..._OK`, and the prediction step labelled every usage without an answer as positive.
  Found by reading the code before a long unattended run (2026-11-25), now guarded: the step exits non-zero, and prediction refuses to write a file with missing answers.

Before interpreting a model-level number, count the inputs of the step that made it: answers per usage, non-empty items per word, lines per cache.
A completeness check costs one script. An unexplained number that turns out to be a count is the most expensive kind of finding.

## See also

- `ai-evaluation/shared-task-scorers-need-known-answer-controls.md`: the same idea for the scorer instead of the system.
- `instance-papers/areas/lexical-semantic-change.md` items 7, 10-12: the case data in the field's terms.
