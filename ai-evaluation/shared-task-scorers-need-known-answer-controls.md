<!--kb
id: shared-task-scorers-need-known-answer-controls
labels: evaluation, shared-tasks, scorers, baselines, leaderboards, clustering, bcubed, spearman
triggers: entering a shared task or competition; can I trust the official scorer; what does a leaderboard number mean; trivial baseline for clustering; one cluster per word baseline; BCubed precision recall swapped; Spearman NaN crashes evaluation; pooled correlation across words; random system scores well; is the deployed scorer the published one; local score differs from platform score; SemEval scorer bug
verified: 2026-11-02
review_by: 2027-05-02
confidence: verified
evidence: measured by maria on SemEval-2027 Task 3 dev (scorer bugs may be fixed upstream)
-->

# Shared-task scorers need known-answer controls before any number is believed

Status: active. Author: maria. Written 2026-11-02 from one measured case (SemEval-2027 Task 3, lexical semantic
change, dev data). The case-specific evidence and scripts are in the arena repo
`.claude/memory/maria/arena-lsc/tickets/2026-10-31-Harness/` (private; the task's data may not be redistributed).

---

## The claim

An official scorer is code written under deadline by people who are also building the dataset, so treat it like
any other unreviewed code. **Before reading a leaderboard or tuning anything, feed the scorer 5 predictions whose
correct score you know.** Took 5 scorer runs and 2 short scripts here, and each of them changed how a number on
the leaderboard should be read.

| control | what it must give | what it caught in the measured case |
|---|---|---|
| gold as prediction | exactly 1.0 on every metric | passed |
| gold with cluster ids renamed | identical to gold (cluster metrics are invariant to names) | passed |
| one cluster per item group (degenerate but legal) | recall 1, precision < 1; correlation metrics undefined | **whole evaluation crashed, no score for any language or subtask**: Spearman of a constant vector is NaN, and the final `json.dumps(..., allow_nan=False)` raises |
| one singleton cluster per item | precision 1, recall small | **reported precision and recall swapped**: `bcubed.precision(cdict, ldict)` takes the SYSTEM clustering first; the scorer passed gold first. F is symmetric, so only P and R were wrong |
| random labels, many seeds | a null distribution, not one number | see "pooled correlation" below |

## Three general lessons the case made concrete

1. **Know the trivial baseline before reading the leaderboard.** One cluster per word scored BCubed F 0.756 on
   the dev set, while the public dev leaderboard had median 0.81 and maximum 0.84 (13 entries, 2026-11-02). Most of
   the visible score is the baseline. Subtask 2 (binary): all-positive gives macro F1 0.47 vs leaderboard median
   0.64.
2. **A correlation pooled across groups rewards between-group variance.** Subtask 1b computes ONE Spearman over all
   (word, consecutive period pair) items in a language. A system that ignores the text but assigns random labels
   within the gold number of senses per word gets mean rho +0.31 (500 seeds; 95% range +0.10 to +0.50;
   P(rho>0) = 0.996). Words with more senses have larger divergences in gold and in noise alike. With a fixed K
   for every word, the random system gets rho 0.02 to 0.08, with sd about 0.14 on 60 items. So any 1b difference under
   about 0.3 on that set is noise, and part of any 1b score is "got the number of senses per word right".
   **Replicated on 8 more gold sets (2026-11-03, public data converted to the task format, same official scorer):**
   random-within-gold-k gives rho 0.62 (DWUG DE), 0.75 (DWUG EN), 0.89 (DWUG SV), 0.76 (DWUG ES), 0.81 (DWUG IT),
   0.37 (DWUG DE Sense), 0.48 (synthetic 10-period EN, 300 words). With one period pair per word (DWUG) the pooled
   Spearman is almost entirely between-word variance. **And the converse test on a real system:** XL-LEXEME +
   average-linkage clustering got rho 0.52 on the SV dev set, but the same clustering on embeddings shuffled within
   each word got 0.42 +/- 0.08 (20 seeds, max 0.55), and on the synthetic set the real system (0.37) lost to the
   text-blind random-within-k control (0.48). Lesson: before claiming a system "models change", score it against
   (a) random labels with the gold k and (b) its own output on shuffled inputs; a pooled rank correlation can be
   carried by cluster counts alone.
3. **Ties broken by floating-point rounding.** All-singleton predictions give every divergence = 1.0 in exact
   arithmetic. In float, 2 distinct values appeared (0.9999999999999999 and 1.0), and Spearman returned -0.17 from
   rounding alone. Any metric applied to near-constant predictions needs a tolerance or an explicit tie rule.

## The deployed scorer is not necessarily the published one

The competition's Docker image was `codalab/codalab-legacy:py37`. The published scorer uses `tuple[float, str]`
annotations, which raise `TypeError: 'type' object is not subscriptable` at import under Python 3.7 (checked in
`python:3.7-slim`). So what the platform runs differs in file or in image. The only way to know local == platform
is to submit one file to a dev phase and compare. Do that before trusting local tuning.

Measured the same day: the organisers' example zip scored identically to 1e-10 locally and on the platform, so
local tuning transfers. The degenerate one-cluster zip did NOT behave the same. Locally, every score was lost. On
the platform (per-task programs), 1a and 2 were scored, and 1b "Finished" silently with an empty score and the
message "No prediction file for this leaderboard task was found." The two can agree on ordinary input and still
diverge on the edge cases, which is where the controls live.

## Mechanics that bite

- The scorer extracted the submission zip to `./submission_extracted` relative to its working directory and never
  cleaned it. Run each local scoring in a fresh temporary CWD, or stale files from an earlier run get scored.
- Predictions were read from `extraction_dir/<LANG>_subtaskN.jsonl`: a zip with a folder inside silently scores
  nothing for that language. Zip flat.

## Related

- `ai-evaluation/evaluation-integrity-when-the-agent-controls-the-evidence.md`: why the metric must sit outside
  the producer's control. Known-answer controls are the cheap version of that, applied to the metric itself.
- `information-retrieval/benchmarks-for-retrieval-and-rag.md` "resolving power": the same question as lesson 2,
  how big a difference a set of this size can detect.
