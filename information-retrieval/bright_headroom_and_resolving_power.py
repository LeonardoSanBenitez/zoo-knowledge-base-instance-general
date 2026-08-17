#!/usr/bin/env python3
"""
Why BRIGHT is a better instrument than BEIR, and it is not because it is harder.

THE ARGUMENT
------------
BRIGHT has tiny query sets -- 76 to 194 queries per dataset, 1,384 in total,
against BEIR's 49 to 13,145. On the resolving-power logic of
beir_resolving_power.py that should make it a WORSE instrument. It does not,
and the reason is worth stating as a principle, because it inverts the usual
advice to prefer large evaluation sets:

    An instrument's usefulness is (effect size) / (minimum detectable
    difference), not 1 / (minimum detectable difference).

BEIR is saturated: the best models sit near the ceiling and the differences
under discussion are one NDCG point. BRIGHT has enormous headroom -- the leading
MTEB model scores 59.0 on BEIR and 18.3 on BRIGHT -- so the interventions that
work move it by 12 points. A 12-point effect is trivially resolvable on 100
queries. A 1-point effect is not resolvable on 1,000.

sigma is not assumed here. It is the value measured on real collections in
can_we_tell_retrievers_apart.py: median 0.133, range 0.126-0.213 for the
per-query paired difference in nDCG@10.

DATA PROVENANCE
---------------
BRIGHT Table 1, transcribed from the paper (arXiv:2407.12883v4, ICLR 2025, p.4).
Headline numbers from the abstract and Section 1.

Author: maria, 2026-08-13
"""
import numpy as np

Z = 2.576   # two-sided p < 0.01

# dataset, #queries, #documents, avg positives per query
BRIGHT = [
    ("Biology",           103,  57359,  3.6),
    ("Earth Science",     116, 121249,  5.3),
    ("Economics",         103,  50220,  8.0),
    ("Psychology",        101,  52835,  7.3),
    ("Robotics",          101,  61961,  5.5),
    ("Stack Overflow",    117, 107081,  7.0),
    ("Sustainable Living",108,  60792,  5.6),
    ("LeetCode",          142, 413932,  1.8),
    ("Pony",              112,   7894, 22.5),
    ("AoPS",              111, 188002,  4.7),
    ("TheoremQA-Q",       194, 188002,  3.2),
    ("TheoremQA-T",        76,  23839,  2.0),
]

# measured, not assumed -- see can_we_tell_retrievers_apart.py section 1
SIGMA_MEASURED = 0.133
SIGMA_RANGE = (0.126, 0.213)

print("=" * 88)
print("1. BRIGHT's RESOLVING POWER, using the sigma measured on real collections")
print("=" * 88)
print(f"   sigma = {SIGMA_MEASURED} (median measured; range {SIGMA_RANGE[0]}-{SIGMA_RANGE[1]})")
print(f"   MDD = z * sigma / sqrt(n), in NDCG points\n")
print(f"  {'dataset':<20}{'Q':>6}{'docs':>9}{'pos/Q':>7}{'MDD':>8}{'MDD hi':>8}")
for name, q, d, pos in sorted(BRIGHT, key=lambda r: r[1]):
    mdd = 100 * Z * SIGMA_MEASURED / np.sqrt(q)
    mdd_hi = 100 * Z * SIGMA_RANGE[1] / np.sqrt(q)
    print(f"  {name:<20}{q:>6}{d:>9,}{pos:>7.1f}{mdd:>8.2f}{mdd_hi:>8.2f}")

ns = np.array([q for _, q, _, _ in BRIGHT], float)
k = len(ns)
se_avg = SIGMA_MEASURED * np.sqrt((1 / ns).sum()) / k
print(f"""
  Per dataset: nothing below ~{100*Z*SIGMA_MEASURED/np.sqrt(np.median(ns)):.1f} NDCG points is resolvable, and on
  TheoremQA-T (76 queries) nothing below {100*Z*SIGMA_MEASURED/np.sqrt(76):.1f}.

  The 12-dataset AVERAGE, however:
      SE  = {100*se_avg:.3f} NDCG points
      MDD = {100*Z*se_avg:.3f} NDCG points   at p<0.01
  which is sharper than BEIR's average (MDD 0.40-1.01 points over 19 subsets),
  despite BRIGHT having one twentieth of the queries. The reason is that BRIGHT's
  query counts are BALANCED -- 76 to 194 -- so no single subset dominates the
  variance of the mean. BEIR's average is 78% driven by its four smallest
  subsets. Balance beats size.
""")
share = (1 / ns) / (1 / ns).sum()
print(f"  largest single-subset share of the average's variance: BRIGHT {100*share.max():.1f}%"
      f"   (BEIR: 23%)")

print("\n" + "=" * 88)
print("2. HEADROOM -- why the small query sets do not matter")
print("=" * 88)
effects = [
    ("SFR-Embedding-Mistral: BEIR -> BRIGHT", 59.0 - 18.3,
     "the gap the benchmark exists to expose (abstract)"),
    ("LLM chain-of-thought query reasoning", 12.2,
     "average improvement from reasoning about the query before retrieval (abstract)"),
    ("a typical claimed BEIR SOTA increment", 1.0,
     "what embedding papers actually argue about"),
    ("BM25 param choice, measured by me", 100 * 0.0215,
     "bm25_k0.9_b0.40 vs k1.2_b0.75 on vaswani; p=0.024, NOT significant at n=93"),
]
mdd_typ = 100 * Z * SIGMA_MEASURED / np.sqrt(np.median(ns))
mdd_avg = 100 * Z * se_avg
print(f"  {'effect':<42}{'points':>8}{'/ MDD(one set)':>16}{'/ MDD(avg)':>12}")
for lbl, e, _ in effects:
    print(f"  {lbl:<42}{e:>8.1f}{e/mdd_typ:>16.1f}{e/mdd_avg:>12.1f}")
print(f"""
  Read the last two columns as "how many times larger than the smallest thing
  the instrument can see".

  The reasoning intervention is {12.2/mdd_typ:.0f}x the per-dataset detection floor. You could
  measure it on ONE BRIGHT subset of 103 queries and be sure. A 1-point BEIR
  increment is {1.0/mdd_typ:.1f}x that floor -- i.e. invisible on any single subset, and
  detectable only in an average whose variance is dominated by 49 queries of
  Touche-2020.

  THE PRINCIPLE, which I have not seen stated:

      Choose a benchmark by its HEADROOM-TO-NOISE ratio, not by its size.
      An unsaturated benchmark with 100 queries per subset is a better
      instrument than a saturated one with 10,000, because the interventions
      that work on it move it by an amount you can see.

  This also explains why the field's attention moved to BRIGHT: not fashion,
  and not only difficulty. It is the only place left where the effects are
  bigger than the error bars.
""")

print("=" * 88)
print("3. WHAT THIS MEANS FOR A NEW METHOD -- the agentic case")
print("=" * 88)
print(f"""  BRIGHT's construction has three properties that matter for evaluating
  something MORE AGENTIC than a fixed embedding:

  (a) Relevance is defined by REASONING, not by surface overlap. A document is
      positive iff it "helps reason through the query with critical concepts or
      theories" -- unanimously agreed by one annotator and two PhD reviewers.
      So a system that thinks before it searches is not penalised as off-task;
      it is what the benchmark is for. Contrast a pooled TREC collection, where
      an unusual system retrieves unjudged documents and is scored down.

  (b) The negatives are ADVERSARIALLY SEMANTIC. Annotators Googled for pages
      that are topically similar and do not meet the query's specific
      requirement. So cosine similarity is explicitly not enough, by
      construction, and a clever rule-based or multi-step system has room to
      win rather than merely to match.

  (c) Leakage-resistant. The authors report no substantial gains even when
      models are further trained on the benchmark's documents -- because the
      difficulty is in the query-document RELATION, not in memorising either
      side. That is a structurally better contamination defence than a fresh
      test set, which only works until it is published.

  The one caution, and it is the same confound Gabin et al. hit in RAG: the
  headline improvements come from LLM-augmented pipelines (query rewriting,
  chain-of-thought). That mixes retriever quality with generator quality. If we
  build something agentic and it beats a baseline on BRIGHT, the honest
  decomposition needs the SAME generator on both sides -- otherwise we will have
  measured the LLM we happened to use.
""")
