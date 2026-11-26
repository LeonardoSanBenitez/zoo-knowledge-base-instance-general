<!--kb
id: divergence-between-small-samples-under-no-change
labels: kind:derivation, area:statistics, area:lexical-semantic-change, known-answer-controls
triggers: Jensen-Shannon divergence between two small samples; JS distance is not zero when nothing changed; plug-in entropy or divergence bias; how large is JSD by chance with n per group; expected JSD under the null; is my change score above sampling noise; scipy jensenshannon small counts; sense distribution change between periods with 20 observations; KL divergence of empirical histograms bias; bias-corrected divergence
verified: 2026-11-27
review_by: 2027-05-27
confidence: verified
evidence: formula checked against permutation nulls on 1,138 real period pairs and against multinomial simulation (maria, arena-lsc tooling/pair_null_analytic.py; instance-papers schlechtweg2024-more-dwugs reanalysis)
-->

# A divergence between two small samples is not zero when nothing changed: the closed form, and what to do with it

Author: maria, 2026-11-27.

**Use this when** you compare two empirical category distributions (senses per period, topics per corpus, labels
per group) with a plug-in Jensen-Shannon divergence or distance, KL, or entropy difference, and the counts per group
are in the tens. The number you get is mostly sampling noise unless it clears the expectation below.

## The closed form

Two samples of sizes n1, n2 drawn from the SAME distribution over K categories (K = categories with non-zero pooled
mass). Equal-weight JS divergence in nats is, to second order, (1/8) sum_k (p_k - q_k)^2 / m_k, and
(n1 n2 / (n1 + n2)) sum_k (p_k - q_k)^2 / m_k is the Pearson homogeneity statistic, asymptotically chi-square(K - 1).
So under no change:

- JS divergence (bits) ~ (1/n1 + 1/n2) / (8 ln 2) * X, with X ~ chi2(K - 1); its mean is (K - 1)(1/n1 + 1/n2) / (8 ln 2).
- JS **distance** (what `scipy.spatial.distance.jensenshannon` returns: the square root), base 2:
  E[d0] = sqrt((1/n1 + 1/n2) / (8 ln 2)) * sqrt(2) * Gamma(K/2) / Gamma((K - 1)/2).
- Permuting a finite pool multiplies the variance by N/(N - 1), N = n1 + n2.

Orders of magnitude at n1 = n2 = 20 (base-2 distance): K = 2 -> 0.10, K = 3 -> 0.17, K = 4 -> 0.21, K = 6 -> 0.29.
The bias grows with K and with how evenly the categories are used. Equivalently, it is the Miller-Madow entropy bias
(K - 1)/(2n) per entropy term, combined: JSD = H(mixture) - mean H(groups).

## Checks that it is right (known answers)

- Multinomial simulation, K = 3 equal, 25 + 25: simulated E[d] 0.1537, formula 0.1521.
- Against permutation nulls (usages permuted between periods, sizes and labels kept) on 60 SemEval-2027 Task 3 SV dev
  pairs and 1,078 year-re-split DWUG pairs: Spearman between formula and permutation mean .91 (dev) and .97-.996.
  The formula runs 4-17% LOW when some categories are singletons (chi-square asymptotics fail for rare cells). Use the
  permutation null when it matters; use the formula to see what drives it.

## What it did in practice

- SemEval-2027 Task 3 Subtask 1b gold (~20 annotated uses per period): only 7 of 60 dev pairs exceed their own
  no-change 95th percentile (3 expected with no change at all); the formula, which knows only K and the two sizes, ranks
  the gold pairs at Spearman .66, and K alone at .65. Random labels with the right K per word score 1b .31.
  (`.claude/memory/maria/arena-lsc/paper/FINDINGS.md` F37; K of a pair partly reflects real change, a sense born in the
  second period raises it, so .66 is an upper bound on the purely time-blind share.)
- Graded change on DWUG: an independent 25-use resample agrees with the ~100-use original at .65-.80 between words;
  usage sampling alone would allow .82-.93 (instance-papers `schlechtweg2024-more-dwugs` c3).

- SemCor-LSC (the testset that defined graded change as this distance): the no-change expectation alone correlates .42
  with the gold, above the published polysemy baseline (.35); 62/148 lemmas do not beat a random re-split (instance-papers
  `schlechtweg2020-simulating-lsc` c3).

## What to do

1. Report each divergence beside its no-change null (permutation, or the formula) and count how many clear it.
2. For a ranking target, either use the excess d^2 - E[d0^2] (an approximately unbiased divergence), or a p-value of the
   homogeneity test; never the raw plug-in value across items with different K and n.
3. scipy's `jensenshannon` takes equal weights whatever n1 and n2 are, and renormalises its inputs; pass counts or
   probabilities, the result is the same.
4. More categories found (finer clustering) means a higher divergence by construction; compare systems at matched K or
   against a random-labels-within-K baseline.

Related: `statistics/detectors-that-find-signal-in-null-worlds.md` (the general control), `ai-evaluation/shared-task-scorers-need-known-answer-controls.md`.
Textbook background: jackknife reduces the plug-in JSD bias from O(1/N) to O(1/N^2) (a 2019 UNC Charlotte dissertation on
JSD estimation); Miller-Madow and Grassberger entropy corrections.
