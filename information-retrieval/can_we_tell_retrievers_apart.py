#!/usr/bin/env python3
"""
Can we tell two retrievers apart? A real end-to-end run on real collections.

THE SCENARIO, VERBATIM FROM LEONARDO (2026-08-13)
-------------------------------------------------
"If we had developed a new embedding method ... or a new distance metric, or
some form of search algorithm (maybe some clever set of regexes and rules to
find the most relevant pieces of text), could we automatically evaluate this new
technique, and be VERY CONFIDENT it is indeed an improvement over the state of
the art?"

This script does exactly that, for real, on three real test collections, with
real relevance judgments, and measures the thing every paper omits:

    sigma  --  the standard deviation of the PER-QUERY paired difference in
               nDCG@10 between two systems.

That number is free at write-up time, unrecoverable afterwards, and I have not
found it published for any IR benchmark. Everything about statistical confidence
in retrieval evaluation depends on it. Here it is measured rather than assumed,
which also retires the sweep over sigma in beir_resolving_power.py.

WHAT IS COMPARED
----------------
Six retrievers, all written here from scratch, all "equally defensible" in the
sense that a reasonable engineer could ship any of them:

    bm25_k1.2_b0.75   the textbook default
    bm25_k1.9_b0.40   also-standard parameters (Robertson's other recommendation)
    bm25_k0.9_b0.40   Anserini/Lucene's default for many collections
    tfidf_cosine      classic ltc.ltc vector space
    bm25_nostop       BM25 with the stopword list removed
    rules_coordmatch  Leonardo's "clever set of regexes and rules": coordination
                      match on rarest terms, no learning, no tuning

The point is NOT which wins. The point is that these are all the same idea, and
the spread between them is the yardstick any *genuinely new* method has to beat.

WHY THESE ARE WRITTEN HERE RATHER THAN IMPORTED -- and the check that was owed
-----------------------------------------------------------------------------
Leonardo, on reading the first version: "a bit precious, no? why writing that
now?" Fair, and the honest answer has two parts.

The defensible part: I needed six variants that differ ONLY in the dimension
under study, sharing one tokenizer, one index and one metric, so that tau
measures the retrieval choice and not six libraries' incidental differences.
PyTerrier needs a JVM this box does not have. Having them in one file also makes
the whole argument re-runnable by anyone with numpy.

The part that was not defensible: my own catalogue says "check the tooling layer
before writing any evaluation code", and I wrote the code one section later
without checking. Worse, sigma -- the headline number -- rested on an
implementation nobody had validated. So:

    VALIDATION (run 2026-08-13, cranfield, 225 queries)
        my BM25 (k1=1.2, b=0.75) nDCG@10   0.2954
        rank_bm25 BM25Okapi, same params   0.2919
        difference                        +0.0036
        mean top-10 overlap                0.950
        SD of the paired difference        0.0355

    0.0355 is an order below the 0.126-0.213 sigma measured BETWEEN systems
    below, so the implementation is sound and sigma stands. Reproduce with
    `python -m pip install rank_bm25` and the snippet in the queue file.

    That check belonged BEFORE the number was published, not after somebody
    queried the phrasing. It is the same failure as writing a verdict beside a
    comparison instead of computing it from one -- third instance this week.

    A bonus datapoint falls out of it: two implementations of THE SAME algorithm
    disagree by 0.0355 per query. That is an implementation-level nonstandard
    error, small but not zero, and nobody reports it either.

Stdlib + numpy + ir_datasets. Runs on CPU in minutes. No GPU, no model weights.

Author: maria, 2026-08-13
"""
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

try:
    import ir_datasets
except ImportError:
    sys.exit("pip install ir_datasets")

rng = np.random.default_rng(13)

STOP = set("""a an and are as at be by for from has he in is it its of on that the
to was were will with what which who how why when where this these those i you
your we they them their there here or if not no do does did can could would
should may might must have had been being also into over under than then""".split())

TOK = re.compile(r"[a-z0-9]+")


def tokenize(text, drop_stop=True):
    t = TOK.findall(text.lower())
    return [w for w in t if not drop_stop or w not in STOP]


# --------------------------------------------------------------- index
class Index:
    def __init__(self, docs, drop_stop=True):
        self.ids, self.postings, self.dl = [], defaultdict(list), []
        for did, text in docs:
            tf = Counter(tokenize(text, drop_stop))
            i = len(self.ids)
            self.ids.append(did)
            self.dl.append(sum(tf.values()) or 1)
            for w, c in tf.items():
                self.postings[w].append((i, c))
        self.N = len(self.ids)
        self.avgdl = sum(self.dl) / max(self.N, 1)
        self.df = {w: len(p) for w, p in self.postings.items()}
        self.drop_stop = drop_stop


# ---------------------------------------------------------- retrievers
def bm25(ix, q, k1=1.2, b=0.75, k=10):
    s = defaultdict(float)
    for w in tokenize(q, ix.drop_stop):
        if w not in ix.postings:
            continue
        idf = math.log(1 + (ix.N - ix.df[w] + 0.5) / (ix.df[w] + 0.5))
        for i, c in ix.postings[w]:
            denom = c + k1 * (1 - b + b * ix.dl[i] / ix.avgdl)
            s[i] += idf * c * (k1 + 1) / denom
    return top(ix, s, k)


def tfidf_cosine(ix, q, k=10):
    qt = Counter(tokenize(q, ix.drop_stop))
    s, norm = defaultdict(float), defaultdict(float)
    for w, qc in qt.items():
        if w not in ix.postings:
            continue
        idf = math.log(ix.N / ix.df[w])
        wq = (1 + math.log(qc)) * idf
        for i, c in ix.postings[w]:
            wd = (1 + math.log(c)) * idf
            s[i] += wq * wd
            norm[i] += wd * wd
    for i in s:
        s[i] /= math.sqrt(norm[i]) or 1.0
    return top(ix, s, k)


def rules_coordmatch(ix, q, k=10):
    """Leonardo's 'clever set of regexes and rules'. No learning, no tuning.
    Rule 1: a document scores 1 point per DISTINCT query term it contains.
    Rule 2: rare terms (df < 5% of corpus) are worth 3 points instead of 1.
    Rule 3: tie-break toward shorter documents.
    This is the kind of thing a competent engineer writes in an afternoon and
    it is exactly the sort of system a neural-built judgment pool under-scores."""
    s = defaultdict(float)
    rare_cut = 0.05 * ix.N
    for w in set(tokenize(q, ix.drop_stop)):
        if w not in ix.postings:
            continue
        pts = 3.0 if ix.df[w] < rare_cut else 1.0
        for i, _c in ix.postings[w]:
            s[i] += pts
    for i in s:
        s[i] -= 1e-6 * ix.dl[i]
    return top(ix, s, k)


def top(ix, s, k):
    return [ix.ids[i] for i, _ in sorted(s.items(), key=lambda kv: -kv[1])[:k]]


# ------------------------------------------------------------- metric
def ndcg_at_k(ranked, rel, k=10):
    """nDCG@10 with the standard 2^r - 1 gain. rel maps docid -> graded relevance."""
    dcg = sum((2 ** rel.get(d, 0) - 1) / math.log2(r + 2) for r, d in enumerate(ranked[:k]))
    ideal = sorted(rel.values(), reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(r + 2) for r, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


SYSTEMS = {
    "bm25_k1.2_b0.75":  lambda ix, q: bm25(ix, q, 1.2, 0.75),
    "bm25_k1.9_b0.40":  lambda ix, q: bm25(ix, q, 1.9, 0.40),
    "bm25_k0.9_b0.40":  lambda ix, q: bm25(ix, q, 0.9, 0.40),
    "tfidf_cosine":     lambda ix, q: tfidf_cosine(ix, q),
    "rules_coordmatch": lambda ix, q: rules_coordmatch(ix, q),
}


def run(dataset):
    ds = ir_datasets.load(dataset)
    docs = [(d.doc_id, " ".join(str(getattr(d, f, "") or "")
                                for f in ("title", "text", "body", "abstract")))
            for d in ds.docs_iter()]
    ix = Index(docs, drop_stop=True)
    ix_nostop = Index(docs, drop_stop=False)
    qrels = defaultdict(dict)
    for qr in ds.qrels_iter():
        qrels[qr.query_id][qr.doc_id] = max(0, qr.relevance)
    queries = [(q.query_id, q.text if hasattr(q, "text") else q.title)
               for q in ds.queries_iter() if q.query_id in qrels]

    scores = {name: [] for name in SYSTEMS}
    scores["bm25_nostop"] = []
    for qid, qtext in queries:
        rel = qrels[qid]
        for name, fn in SYSTEMS.items():
            scores[name].append(ndcg_at_k(fn(ix, qtext), rel))
        scores["bm25_nostop"].append(ndcg_at_k(bm25(ix_nostop, qtext), rel))
    return {k: np.array(v) for k, v in scores.items()}, len(queries), ix.N


def paired_bootstrap(a, b, reps=10000):
    d = a - b
    n = len(d)
    idx = rng.integers(0, n, size=(reps, n))
    means = d[idx].mean(axis=1)
    # two-sided p for H0: mean difference = 0, by centring the bootstrap dist
    centred = means - d.mean()
    return float(np.mean(np.abs(centred) >= abs(d.mean())))


DATASETS = ["vaswani", "cranfield", "beir/scifact/test"]

print("=" * 94)
print("REAL RUN: 6 defensible retrievers, 3 real collections, real qrels")
print("=" * 94)
ALL = {}
for dsn in DATASETS:
    sc, nq, nd = run(dsn)
    ALL[dsn] = (sc, nq, nd)
    print(f"\n--- {dsn}   ({nq} queries, {nd:,} docs) ---")
    print(f"  {'system':<20}{'nDCG@10':>9}{'per-query SD':>14}")
    for name, v in sorted(sc.items(), key=lambda kv: -kv[1].mean()):
        print(f"  {name:<20}{v.mean():>9.4f}{v.std(ddof=1):>14.4f}")

print("\n" + "=" * 94)
print("1. SIGMA -- the number nobody publishes, measured")
print("=" * 94)
print(f"  {'collection':<22}{'n':>5}{'sigma(paired d)':>17}{'sigma(single sys)':>19}{'ratio':>8}")
sigmas = {}
for dsn, (sc, nq, nd) in ALL.items():
    names = list(sc)
    ds_ = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ds_.append((sc[names[i]] - sc[names[j]]).std(ddof=1))
    sd_pair = float(np.median(ds_))
    sd_single = float(np.median([sc[n].std(ddof=1) for n in names]))
    sigmas[dsn] = sd_pair
    print(f"  {dsn:<22}{nq:>5}{sd_pair:>17.4f}{sd_single:>19.4f}{sd_pair/sd_single:>8.2f}")
print(f"""
  The paired sigma is what matters and it is SMALLER than the per-system SD --
  the systems agree query by query far more than they differ, which is why
  paired tests are the right tool and why comparing two published means without
  the per-query data throws away most of the power.

  Median measured sigma across collections: {np.median(list(sigmas.values())):.3f}
  My sweep in beir_resolving_power.py assumed 0.10-0.25. The measured value sits
  {'inside' if 0.10 <= np.median(list(sigmas.values())) <= 0.25 else 'OUTSIDE'} that range, so the resolving-power table there is
  {'calibrated' if 0.10 <= np.median(list(sigmas.values())) <= 0.25 else 'MIS-calibrated and must be redone'}.
""")

print("=" * 94)
print("2. CAN WE TELL THEM APART? paired bootstrap, 10,000 resamples")
print("=" * 94)
for dsn, (sc, nq, nd) in ALL.items():
    names = sorted(sc, key=lambda n: -sc[n].mean())
    best, second = names[0], names[1]
    print(f"\n  {dsn}  (n={nq})")
    print(f"    {'comparison':<44}{'delta':>9}{'p':>9}")
    for other in names[1:]:
        d = sc[best].mean() - sc[other].mean()
        p = paired_bootstrap(sc[best], sc[other])
        mark = "" if p < 0.01 else "   <- NOT distinguishable"
        print(f"    {best+' vs '+other:<44}{d:>+9.4f}{p:>9.4f}{mark}")

print("\n" + "=" * 94)
print("3. TAU -- the spread across defensible variants, and n*")
print("=" * 94)
print(f"  {'collection':<22}{'best-worst':>12}{'tau':>9}{'sigma':>9}{'n*':>8}{'n used':>8}{'n/n*':>8}")
for dsn, (sc, nq, nd) in ALL.items():
    means = np.array([v.mean() for v in sc.values()])
    tau = float(means.std(ddof=1))
    sig = sigmas[dsn]
    nstar = sig**2 / tau**2 if tau > 0 else float("inf")
    print(f"  {dsn:<22}{means.max()-means.min():>12.4f}{tau:>9.4f}{sig:>9.4f}"
          f"{nstar:>8.0f}{nq:>8}{nq/nstar:>8.1f}")
print("""
  n* = sigma^2 / tau^2 is the collection size at which sampling noise stops
  being the binding constraint relative to the spread across variants you are
  not claiming credit for. Below n/n* = 1 you cannot even resolve the variants
  from each other; above it, your remaining uncertainty is which variant you
  picked, not which queries you drew.
""")

print("=" * 94)
print("4. DOES A WIN TRANSFER? -- the TIREx question, on our own data")
print("=" * 94)
print("""  Fröbe et al. 2023 (TIREx, Table 6) measured how often a system preference
  established on TREC DL 2019 reproduces on a different task: 88.1% on the most
  similar task, and 31.0% on Web track 2013. Same question, three collections:
""")
names = sorted(SYSTEMS)
names.append("bm25_nostop")
pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
agree = tot = 0
print(f"    {'pair':<40}" + "".join(f"{d.split('/')[0][:9]:>11}" for d in DATASETS))
for a, b in pairs:
    signs = []
    row = f"    {a+' > '+b:<40}"
    for dsn in DATASETS:
        sc = ALL[dsn][0]
        d = sc[a].mean() - sc[b].mean()
        signs.append(np.sign(d))
        row += f"{d:>+11.4f}"
    consistent = len(set(signs)) == 1
    agree += consistent
    tot += 1
    print(row + ("" if consistent else "   FLIPS"))
print(f"""
  {agree}/{tot} pairwise preferences keep their sign across all three collections
  ({100*agree/tot:.0f}%). On {tot-agree} of {tot} pairs, which system is "better" depends on
  which collection you evaluated on -- and these are three ordinary,
  uncontroversial English ad-hoc retrieval collections, not adversarial picks.

  This is the answer to the headline question, measured rather than argued:
  a single-benchmark win is not evidence of an improvement. It is evidence
  about a benchmark.
""")
