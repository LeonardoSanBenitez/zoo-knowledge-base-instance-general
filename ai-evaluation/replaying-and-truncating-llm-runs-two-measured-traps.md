<!--kb
id: replaying-and-truncating-llm-runs-two-measured-traps
labels: evaluation, llm, inference, reproducibility, vllm, greedy-decoding, truncation, max-tokens
triggers: temperature 0 rerun does not reproduce the cached replies; is greedy decoding deterministic across server restarts; byte-identical control failed; replies repeat inside one server session only; reply cut at the max_tokens limit counted as an answer; does a larger completion limit rescue the cut replies; degenerate repetition loop at temperature 0; how to count a truncated generation; finish_reason length; hidden-state free way to read two token limits from one run
verified: 2026-11-24
review_by: 2027-05-24
confidence: reported
evidence: dojo ticket 2026-09-27-CosmosReason2 (priya, vLLM 0.30.0, nvidia cosmos-reason2-8b BF16, one A40 card pair, MedQA/MedMCQA deliberation_channel); files REVIEWS.md 2026-11-21, REPORT_E5.md, REPORT_E7.md. One model, one serving stack: the numbers are a measured case, not a law.
-->

# Replaying and truncating LLM runs: two measured traps

Status: active. Author: maria (placed here 2026-11-24 at priya's hand-over; the measurements are priya's, from the dojo CosmosReason2 ticket). One model and one serving stack. Check before generalising.

## 1. Greedy decoding repeats inside one server session, not across sessions

At temperature 0 on vLLM (same weights, same image, same engine configuration in the server log), a rerun of cached prompts on a fresh server did **not** reproduce the committed replies:
**0 of 15** finished replies byte-identical on card 1 and **1 of 15** on card 0, and **0 of 16** between the two fresh sessions an hour apart. Inside one session the replies did repeat (the earlier determinism check compared two runs within one session). So "temperature 0 is deterministic" held for the cache's own session and for nothing else.

Consequences for anyone running a replay or a known-answer control:
- A control of the form "the rerun must be byte-identical to the committed cache" can fail for a perfectly good pipeline, and a failure of it does not identify the cause (here it first looked like the server context length, 16,384 to 32,768; the probe at the original context failed as well). Run the probe at the original configuration on the original card before blaming a change.
- Determinism must be stated per scope: within a call batch, within a server session, across sessions, across cards. Measure the scope you rely on.
- Any count that comes from one session (here, how many replies hit the limit) belongs to that session and must be reported as such.

## 2. A reply cut at the completion limit is not an answer, and a bigger limit does not rescue it

The deliberation replies recorded as `finish_reason = length` were exactly the limit (all 28 at 8,192 tokens; none of the 692 that stopped reached it, longest 2,930). They are repetition loops, not long thoughts: in each of the 28 the last 400 characters occur 9 to 80 times and the first repeat starts 8% to 37% of the way in. The tails that "read like deliberation" are the repeated passage.

Doubling the limit to 16,384 (one session, 240 prompts): of the 35 replies past 8,192 tokens, **0 finish** and all 35 are still repeating when cut. A cut reply is a reply that does not end, not one that needed room.

Two rules that follow:
- **Count a reply cut at the limit as no answer**, and report beside it the number computed on complete replies. Scoring a parsed letter out of a loop moved results in the measured case (a decoy rate 0.375 to 0.325; an exact p of 0.057 to 0.146 for a claimed gain).
- **Find the cut replies you did not record.** Re-tokenising the stored replies found 20 that no runner flagged (hidden-note session caches), against 28/28 and 0/692 on the cache that recorded finish reasons. The check that makes it safe: a known set (the recorded `length` rows) must all sit exactly at the limit and no `stop` row may reach it.

Side fact used to save a run: under greedy decoding in one session, the reply under a limit L is the first L tokens of the reply under a larger limit. One long run therefore reads both "would it be cut at 8,192?" and "does it finish with more room?" per prompt, provided the within-session identity is verified first (done here: 16 of 16).

## When to re-read

If the serving stack, the model or the completion limit changes, or a runner starts recording finish reasons for the caches that lacked them.
