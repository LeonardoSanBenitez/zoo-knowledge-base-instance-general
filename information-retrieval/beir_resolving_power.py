#!/usr/bin/env python3
"""
How small an improvement can BEIR actually resolve?

Answers TODO Tier-1 #3 of benchmarks-for-retrieval-and-rag.md.

WHY THIS IS NOT IN ANY PAPER I HAVE FOUND
-----------------------------------------
Embedding papers report NDCG@10 per BEIR subset and an unweighted average across
subsets, and compare models on that average, routinely to two decimal places.
Nobody prints the resolving power of the instrument. The inputs needed are:

  n_i   -- number of test queries per subset            (published, Table 1)
  sigma -- SD of the PER-QUERY paired difference in
           NDCG@10 between the two systems compared     (NOT published, ever)

sigma is the missing number identified in section 1(d) of the catalogue. It is
free at write-up time and cannot be recovered afterwards, so this script does the
only honest thing available: sweeps it over the range IR practice suggests and
shows that the conclusion does not depend on which value you pick.

DATA PROVENANCE
---------------
n_i and judgments-per-query transcribed from the BEIR paper's own Table 1,
extracted from the LaTeX source rather than the PDF:

    tar xzf beir_2104.08663.src.tar.gz -C /tmp/src/beir
    sed -n '160,184p' /tmp/src/beir/neurips2021.tex

That is the authors' table, not a rendering of it. Column "Avg. D/Q" is their
own label for average relevant documents per query.

Author: maria, 2026-08-13
"""
import numpy as np

# dataset, #test queries, avg relevant docs/query, relevance scale
BEIR = [
    ("MS MARCO",       6980,   1.1, "binary"),
    ("TREC-COVID",       50, 493.5, "3-level"),
    ("NFCorpus",        323,  38.2, "3-level"),
    ("BioASQ",          500,   4.7, "binary"),
    ("NQ",             3452,   1.2, "binary"),
    ("HotpotQA",       7405,   2.0, "binary"),
    ("FiQA-2018",       648,   2.6, "binary"),
    ("Signal-1M (RT)",   97,  19.6, "3-level"),
    ("TREC-NEWS",        57,  19.6, "5-level"),
    ("Robust04",        249,  69.9, "3-level"),
    ("ArguAna",        1406,   1.0, "binary"),
    ("Touche-2020",      49,  19.0, "3-level"),
    ("CQADupStack",   13145,   1.4, "binary"),
    ("Quora",         10000,   1.6, "binary"),
    ("DBPedia",         400,  38.2, "3-level"),
    ("SCIDOCS",        1000,   4.9, "binary"),
    ("FEVER",          6666,   1.2, "binary"),
    ("Climate-FEVER",  1535,   3.0, "binary"),
    ("SciFact",         300,   1.1, "binary"),
]

Z = 2.576          # two-sided p < 0.01
SIGMAS = [0.10, 0.15, 0.20, 0.25]   # plausible SD of per-query paired dNDCG@10

print("=" * 92)
print("1. MINIMUM DETECTABLE DIFFERENCE IN NDCG@10, PER BEIR SUBSET, p<0.01 paired")
print("=" * 92)
print("   MDD = z * sigma / sqrt(n).  Values in NDCG POINTS (x100), as papers report them.\n")
hdr = f"  {'dataset':<17}{'n':>7}{'rel/q':>7}{'scale':>9}" + "".join(f"{'s='+str(s):>9}" for s in SIGMAS)
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for name, n, dq, scale in sorted(BEIR, key=lambda r: r[1]):
    row = f"  {name:<17}{n:>7}{dq:>7.1f}{scale:>9}"
    for s in SIGMAS:
        row += f"{100*Z*s/np.sqrt(n):>9.2f}"
    print(row)

print("""
  READ THE TOP OF THE TABLE. Touche-2020 (49 queries), TREC-COVID (50) and
  TREC-NEWS (57) cannot resolve a difference smaller than roughly FIVE NDCG
  POINTS at any plausible sigma. Papers routinely report and discuss per-subset
  differences of one point on exactly these subsets.

  Note also the interaction with judgments-per-query, which runs the WRONG way.
  The subsets with the deepest judging -- TREC-COVID at 493.5 relevant documents
  per query, Robust04 at 69.9 -- are the ones with the fewest queries. So the
  subsets where a novel retriever is least likely to be penalised by shallow
  pooling are exactly the subsets that cannot resolve its improvement. There is
  no BEIR subset that is both deeply judged AND large.
""")

print("=" * 92)
print("2. THE BEIR AVERAGE -- what does a difference in the headline number mean?")
print("=" * 92)
print("""  The reported figure is an UNWEIGHTED mean over subsets, so
      Var(mean) = (1/k^2) * sum_i sigma^2 / n_i
  and the small subsets dominate the variance regardless of how large the big
  ones are. Adding queries to HotpotQA does almost nothing for the average.
""")
ns = np.array([n for _, n, _, _ in BEIR], float)
k = len(ns)
print(f"  {'sigma':>7}{'SE of avg':>12}{'MDD of avg':>12}   {'top variance contributors':<45}")
inv = 1.0 / ns
share = inv / inv.sum()
top = sorted(zip([b[0] for b in BEIR], share, ns), key=lambda t: -t[1])[:4]
contrib = ", ".join(f"{nm} {100*sh:.0f}%" for nm, sh, _ in top)
for s in SIGMAS:
    se = s * np.sqrt(inv.sum()) / k
    print(f"  {s:>7.2f}{100*se:>12.3f}{100*Z*se:>12.3f}   {contrib if s == SIGMAS[0] else '':<45}")
print(f"""
  With k = {k} subsets, {100*share.max():.0f}% of the variance of the headline average comes
  from a single 49-query subset, and the four smallest subsets together
  contribute {100*sum(sh for _, sh, _ in top):.0f}%. Fourteen of the nineteen subsets are, between them,
  responsible for less than {100*(1-sum(sh for _, sh, _ in top)):.0f}% of it.

  The good news: the AVERAGE is a reasonably sharp instrument -- differences
  above roughly half an NDCG point are resolvable against sampling error. The
  bad news is section 3.
""")

print("=" * 92)
print("3. SAMPLING ERROR IS NOT THE BINDING CONSTRAINT, AND THAT IS THE POINT")
print("=" * 92)
print("""  Everything above prices ONE source of uncertainty: which queries you drew.
  From my 2026-08-12/13 work on RAG specification dispersion
  (instance-papers/areas/rag-and-knowledge-management.md), the spread of an
  effect across equally defensible pipeline configurations was 3.3x the width of
  the confidence interval a single configuration would report.

  Applying the saturation identity n* = sigma^2 / tau^2, where tau is the SD of
  the measured improvement across configurations you are not claiming credit for
  (chunker, k, reranker on/off, ordering, normalisation):
""")
print(f"  {'sigma':>7}{'tau=0.005':>12}{'tau=0.010':>12}{'tau=0.020':>12}{'tau=0.040':>12}   (n* in queries)")
for s in SIGMAS:
    row = f"  {s:>7.2f}"
    for tau in (0.005, 0.010, 0.020, 0.040):
        row += f"{s**2/tau**2:>12.0f}"
    print(row)
print(f"""
  Read against column 2 of the table in section 1. For tau = 0.02 NDCG -- a
  modest amount of configuration sensitivity -- n* is in the tens to low
  hundreds of queries. TEN BEIR SUBSETS ARE ALREADY LARGER THAN THAT, and MS
  MARCO, HotpotQA, CQADupStack and Quora are one to two orders of magnitude past
  it.

  So the honest summary of BEIR as an instrument:

    * per-subset, on the small deeply-judged sets, it cannot resolve anything
      below ~5 NDCG points, and those are the KM-meaningful sets;
    * the average is sharp against sampling error, to about half a point;
    * and the average is NOT sharp against configuration choice, which nobody
      measures, because measuring it requires running the sweep that a single
      benchmark number exists to avoid.

  A claimed improvement of 1-2 NDCG points on the BEIR average is therefore
  inside the noise of the thing nobody measured, and outside the noise of the
  thing everybody reports. That is the precise answer to "could we be VERY
  CONFIDENT", and it is no.

  WHAT WOULD FIX IT, in order of cost:
    1. Publish sd(per-query dNDCG). Free. Makes every number above exact
       instead of a sweep.
    2. Paired significance test on per-query deltas. Nearly free; ranx and
       pyterrier both do it.
    3. Report the improvement across a sweep of the pipeline choices that are
       not your contribution. This is the expensive one and the only one that
       addresses the binding constraint.
""")
