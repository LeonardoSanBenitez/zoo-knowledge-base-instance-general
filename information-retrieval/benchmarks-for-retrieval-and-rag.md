<!--kb
id: doc:ir-rag-benchmark-catalogue
labels: kind:catalogue, area:information-retrieval, area:rag-and-knowledge-management
cite: maria (2026-08-13), zoo internal. Living document, multi-session.
triggers: how do I evaluate a new embedding model; is my retriever actually better than the baseline; which IR benchmark should I use; can I automatically verify a retrieval improvement; where do I get MS MARCO / BEIR / MTEB; is this benchmark still trustworthy; how many queries do I need to compare two retrievers
methods: benchmark-survey, retrieval-evaluation, automatic-verification-platforms
verified: 2026-08-13
-->

# Benchmarks for retrieval, embeddings and RAG — a working catalogue

Author: maria. Started 2026-08-13. **Living document — expected to take several
sessions.** Status of every entry is stated explicitly; most are `desk-research`
and have not been opened. Do not quote a number from here without checking the
`verification` line.

Placement note: Leonardo asked for "an internal document of yours". I have put
it in the knowledge base rather than in `.claude/memory/maria/` because a
catalogue of public benchmarks is durable, topic-organised, and reusable by
anyone here — which is the standing rule, and I was corrected once for doing
otherwise. My *working queue* for it lives in
`.claude/memory/maria/ir_benchmark_catalogue_queue.md`. Overrule me if you meant
the other placement.

---

## 0. The question this exists to answer

> If we had developed a new embedding method (any way of generating a vector out
> of text), or a new distance metric, or some form of search algorithm (maybe
> some clever set of regexes and rules to find the most relevant pieces of
> text), could we **automatically** evaluate this new technique, and be **VERY
> CONFIDENT** it is indeed an improvement over the state of the art?
> — Leonardo, 2026-08-13

### Selection criteria stated up front (to be applied per entry)

1. **Automatically verified** — a machine decides the score, ideally on held-out
   or sandboxed infrastructure the claimant does not control (Einstein-Arena /
   Kaggle / TIRA shape), not a number the authors compute and report.
2. **Good code and data, fully available**, easy to access — ideally through a
   library that exposes many benchmarks behind one interface.
3. **Widely accepted and used** by the ML/IR community; cited; leaderboards that
   people actually submit to.
4. **Strong focus on knowledge management and document search** — things that
   are meaningful in a human sense, not synthetic probe tasks.

Breadth beats box-ticking. Entries that fail most criteria are still listed, with
the failure recorded — a benchmark that is popular and unreliable is more
important to document than one that is obscure and clean.

---

## 1. The short answer, and it is uncomfortable

**Yes to "automatically", emphatically no to "VERY CONFIDENT" — and the gap is
not a tooling gap.**

The automation exists and is good. `mteb` + `ir_datasets` + `ir_measures` will
score a new embedding model across ~130 tasks with one interface, and TIRA/TIREx
will do it in a sandbox where you never touch the qrels. Building that is solved.

Confidence is not, for four reasons that are separately measurable:

**(a) The reported interval is the wrong instrument.** From my own work on this
corpus (2026-08-12/13, `instance-papers/areas/rag-and-knowledge-management.md`):
the spread of a RAG effect across *equally defensible pipeline configurations*
was **3.3× the width of the 95% CI** any single configuration would report. A
new embedding model is evaluated inside a pipeline — chunker, k, reranker,
prompt, decoder — and moving those moves the score more than the model does.

**(b) There is a size past which more queries buy nothing.** I derived a
**benchmark saturation size** n\* = σ²/τ² — the evaluation-set size at which
sampling error stops being the binding uncertainty relative to specification
dispersion. For open-domain QA it came out ≈1,100 items, and Gabín et al. 2026
reach 1,000–2,000 by an independent criterion. **Benchmarks in this area are
routinely 10× past it.** Adding queries makes the CI shrink around a number that
was never the uncertain part.

**(c) The headline benchmarks are saturated and contaminated.** BEIR is no
longer zero-shot in practice — its datasets appear in training pipelines. MTEB
has 400+ models separated by hundredths of NDCG@10, routinely reported without
any paired significance test. MTEB v2 (2026) scores are **not comparable to
v1**, so the historical leaderboard is not a time series.

**(d) Almost nobody publishes the one number that would fix (a) and (b).** The
standard deviation of the **per-query paired difference**. It is free at write-up
time and unrecoverable afterwards. Without it there is no paired test, no n\*, no
power calculation.

> **Update 2026-08-13, after actually running things.** I measured it:
> **σ = 0.126–0.213 nDCG@10** (median 0.133) across three real collections, in
> `can_we_tell_retrievers_apart.py`. And **TIREx already computes it** for every
> run — the `ir_measures` evaluator emits per-query scores "suitable for
> significance tests". So the number exists, on 1,600 runs across 32 tasks; it
> is simply never carried into the papers.

**(e) — added 2026-08-13, and it is the strongest evidence here.** TIREx measured
how often a system preference established on one task reproduces on another:
**88.1% on the most similar task, 31.0% on the most distant** (their Table 6).
I replicated the shape on three collections of my own with six hand-written
retrievers: **11/15 pairwise preferences kept their sign across all three;
4/15 flipped.** Every flip was a *small* effect (BM25 parameter choices); every
large gap held everywhere. So:

> **A single-benchmark win is not evidence of an improvement. It is evidence
> about a benchmark — unless the effect is large, in which case it transfers.**

That last clause is the practical rule, and it is the same conclusion I reached
independently from Liu et al. 2024 in the RAG area: **big effects transfer, small
ones do not,** and almost all published increments are small.

### What I would actually do, today, to be confident

Not "run BEIR and compare NDCG@10". Rather:

1. **Paired, per-query, with a test.** Keep per-query scores. Paired
   bootstrap or randomisation test on the deltas. Report the per-query SD.
2. **Multiverse, not point estimate.** Sweep the pipeline choices that are not
   your contribution (k, chunker, reranker on/off, ordering) and report the
   distribution of your improvement across them. If your delta is smaller than
   that spread, you have not shown an improvement — you have shown a
   configuration.
3. **A sandbox you do not control** for the headline claim: TIRA/TIREx or a
   live TREC/KDD-Cup-style track. This is the only mechanism on the list that
   attacks the structural problem — *the party who benefits from a claim also
   produces its evidence* (see `philosophy-of-science/verification-economics-of-open-science.md`).
4. **At least one benchmark whose queries were written after your model's
   training cutoff**, to price contamination.
5. **A task where retrieval quality is the binding constraint**, not one where
   the generator masks it.

Sections 3–7 are the catalogue. Section 8 is what remains to be done.

---

## 2. Analysis template

Every entry uses these fields, in this order, so entries can be diffed and
sorted. Missing fields mean "not yet established", never "not applicable".

```
### <Name> (<year>)
**What it measures** — the task, in one sentence.
**Unit / size** — queries, corpus size, documents. n matters more than anything.
**Metric** — and whether a machine computes it unaided.
**Judgments** — how relevance was decided; graded or binary; pooled or complete.
**Access** — library call, URL, license.
**Adoption** — citations, leaderboard traffic, whether papers actually submit.
**KM meaningfulness** — is this document search a human would recognise?
**Drop-in for a new embedding / distance / rule-based retriever?** ← the operative question
**Known failure modes** — saturation, contamination, judgment bias.
**Verification** — one of: `desk-research` (I read about it) | `url-checked` |
   `data-opened` (I downloaded and inspected) | `ran-it` | `deep-read` (paper record exists)
**Refs** — arXiv / DOI / repo, bibtex key.
**TODO** — what I owe this entry.
```

---

## 3. Core retrieval and embedding benchmarks

### BEIR (2021)
**What it measures** — zero-shot retrieval generalisation across heterogeneous
domains and task formats (fact-checking, QA, citation prediction, argument
retrieval, duplicate-question, entity retrieval).
**Unit / size** — 18 datasets (of ~19 curated); sizes range from ~300 queries
(TREC-COVID, SciFact) to millions of documents (MS MARCO). *Sizes unverified.*
**Metric** — NDCG@10, by convention, computed by `trec_eval`/`ir_measures`.
Automatic and unambiguous.
**Judgments** — inherited from the constituent datasets; a mixture of graded
(TREC-derived) and binary/sparse (MS MARCO-derived). **The sparsity is the
central problem**: many BEIR sets have ~1 judged relevant document per query, so
a genuinely better system that retrieves an unjudged relevant document is
*scored down*.
**Access** — `beir` package; also `ir_datasets`; also inside `mteb`. Fully open.
**Adoption** — very high. The default "did it generalise" table in embedding
papers for five years.
**KM meaningfulness** — mixed. TREC-COVID, NFCorpus, SciFact and FiQA are
recognisable document search. Quora duplicate-question and ArguAna are not
document search in a KM sense.
**Drop-in for a new embedding / distance / rule-based retriever?** **Yes, best
in class for this.** The interface is (query, corpus) → ranking; a new distance
metric or a pile of regexes plugs in with no retraining. This is the single most
important property for Leonardo's question and BEIR has it.
**Known failure modes** — (i) **no longer zero-shot**: BEIR sets now routinely
appear in embedding training mixtures; (ii) leaderboard saturation with
differences inside noise; (iii) domain skew academic/Western/English;
(iv) shallow pooling ⇒ systematically penalises novel retrieval behaviour.
**Verification** — **`data-opened`**. Table 1 extracted from the paper's *LaTeX
source*, not the PDF (`tar xzf beir_2104.08663.src.tar.gz`; the table is at
`neurips2021.tex` lines 160–184), and analysed in `beir_resolving_power.py`
alongside this file.
**Refs** — Thakur, Reimers, Rücklé, Srivastava, Gurevych, *BEIR: A Heterogeneous
Benchmark for Zero-shot Evaluation of Information Retrieval Models*, NeurIPS
2021 Datasets & Benchmarks. arXiv:2104.08663. bibtex key `thakur2021beir`.

#### RESOLVING POWER — done 2026-08-13, was TODO Tier-1 #3

Minimum detectable difference in **NDCG points**, paired, p<0.01, as a function
of the per-query paired SD σ (which no paper publishes — see §1(d)):

| dataset | n | rel/q | σ=0.10 | σ=0.15 | σ=0.20 | σ=0.25 |
|---|---|---|---|---|---|---|
| Touché-2020 | 49 | 19.0 | 3.68 | **5.52** | 7.36 | 9.20 |
| TREC-COVID | 50 | 493.5 | 3.64 | **5.46** | 7.29 | 9.11 |
| TREC-NEWS | 57 | 19.6 | 3.41 | **5.12** | 6.82 | 8.53 |
| Signal-1M | 97 | 19.6 | 2.62 | 3.92 | 5.23 | 6.54 |
| Robust04 | 249 | 69.9 | 1.63 | 2.45 | 3.26 | 4.08 |
| SciFact | 300 | 1.1 | 1.49 | 2.23 | 2.97 | 3.72 |
| NFCorpus | 323 | 38.2 | 1.43 | 2.15 | 2.87 | 3.58 |
| DBPedia | 400 | 38.2 | 1.29 | 1.93 | 2.58 | 3.22 |
| … | | | | | | |
| CQADupStack | 13,145 | 1.4 | 0.22 | 0.34 | 0.45 | 0.56 |

Three findings, none of which I have seen published:

1. **Touché-2020, TREC-COVID and TREC-NEWS cannot resolve anything under ~5
   NDCG points** at a plausible σ. Papers routinely discuss one-point movements
   on exactly these subsets.
2. **Judgment depth and query count run the wrong way.** The deeply-judged sets
   (TREC-COVID 493.5 rel/q, Robust04 69.9) are the *smallest*. So the subsets
   where a novel retriever is least penalised by shallow pooling are precisely
   those that cannot resolve its improvement. **There is no BEIR subset that is
   both deeply judged and large** — which bears directly on Leonardo's
   rule-based-retriever case.
3. **The headline average is dominated by its smallest members.** With an
   unweighted mean, `Var = (1/k²)Σσ²/nᵢ`, so **23% of the variance of the BEIR
   average comes from one 49-query subset and 78% from the four smallest.**
   Adding queries to HotpotQA does essentially nothing. The average is
   nonetheless reasonably sharp against *sampling* error: MDD ≈ 0.4–1.0 NDCG
   points.

And then the sting: applying n\* = σ²/τ², at a modest configuration sensitivity
of τ = 0.02 NDCG, saturation is **25–156 queries**. Ten BEIR subsets are already
past it and four are one to two orders of magnitude past it. **A claimed 1–2
point gain on the BEIR average is inside the noise of the thing nobody measures
and outside the noise of the thing everybody reports.**

*Caveat on k:* the script uses all 19 rows of Table 1. Published averages are
usually over 18 (excluding MS MARCO as training data) or over the 13–15 freely
redistributable subsets. The qualitative conclusion is unchanged — dropping
large subsets makes the small-set domination worse, not better.

**TODO** — redo with the actual published subset lists; ask whether anyone has
ever published σ for any BEIR subset.

### MTEB / MMTEB / MTEB v2 (2023 → 2026)
**What it measures** — text embeddings across 8 task families (retrieval,
reranking, clustering, pair classification, classification, STS, summarisation,
bitext mining). Retrieval is one slice, and it largely *is* BEIR.
**Unit / size** — MTEB v1: ~58 datasets, 112 languages (*unverified*). MMTEB
(2025): a large multilingual extension. MTEB v2 (2026) is a re-cut whose scores
are **explicitly not comparable to v1**.
**Metric** — task-appropriate (NDCG@10 for retrieval, v-measure for clustering,
Spearman for STS) then **averaged across tasks**. The averaging is the weak
point — see *The Flaw of Averages* in §7.
**Judgments** — inherited.
**Access** — `pip install mteb`; HuggingFace leaderboard. Excellent tooling; a
new model is a class with an `encode()` method.
**Adoption** — the highest in the embedding world. 400+ models on the board.
**KM meaningfulness** — diluted. A KM-relevant retrieval gain can be washed out
by six non-retrieval task families in the mean.
**Drop-in for a new embedding?** **Yes, the easiest of all.** Implement
`encode()`, run one command. For a new *distance metric* or a *rule-based*
retriever it is a much worse fit — the API assumes vectors and cosine.
**Known failure modes** — (i) **v1/v2 incomparability breaks the time series**;
(ii) 400+ models separated by hundredths, usually with no significance test;
(iii) train/test provenance overlap; (iv) the mean-of-tasks hides which tasks
moved.
**Verification** — `desk-research` + web-checked 2026-08-13 (v2 exists; MMTEB
leaderboard led by KaLM-Embedding-Gemma3-12B at 72.32 as of 2026-07 — *reported,
not verified by me*).
**Refs** — Muennighoff, Tazi, Magne, Reimers, *MTEB*, EACL 2023, arXiv:2210.07316.
MMTEB arXiv:2502.13595. *Maintaining MTEB: Towards Long Term Usability and
Reproducibility of Embedding Benchmarks*, arXiv:2506.21182.
**TODO** — read `2506.21182` properly; it is the maintainers' own account of
what rots. Establish exactly what changed v1→v2 and whether any published
comparison spans the break (that would be a real error to find).

### MS MARCO (2016 → )
**What it measures** — passage and document ranking from real Bing queries.
**Unit / size** — ~8.8M passages, ~500K training queries, ~6,980 dev queries
(*unverified*). V2 and V2.1 are larger; TREC RAG uses **MS MARCO V2.1**.
**Metric** — MRR@10 (dev), NDCG@10 (TREC DL). Automatic.
**Judgments** — **sparse and binary**: typically one judged relevant passage per
dev query. Extremely thin. TREC DL adds deep graded judgments for a small query
set, which is why DL is the better evaluation and MS MARCO dev is the more
reported one.
**Access** — `ir_datasets`, official site. Open.
**Adoption** — the training set of record for dense retrieval. Enormous.
**KM meaningfulness** — high: real web queries, real answers.
**Drop-in?** Yes for ranking; the leaderboard has historically been submission-based.
**Known failure modes** — one-judgment-per-query makes MRR@10 a noisy and
biased instrument; near-universal use as *training* data means "evaluating" on
it measures fit, not generalisation.
**Verification** — `desk-research`.
**Refs** — Nguyen et al., *MS MARCO*, arXiv:1611.09268. bibtex `nguyen2016msmarco`.
**TODO** — pin the exact V2.1 statistics used by TREC RAG 2024/2025.

### TREC Deep Learning Track (2019–)
**What it measures** — passage/document ranking with **deep, graded, pooled
human judgments** over MS MARCO.
**Unit / size** — small query sets (~43–100 judged queries per year), deeply
judged. **This is the opposite trade-off from BEIR and it is the right one for
confidence.**
**Metric** — NDCG@10, AP, RR, with `trec_eval`.
**Judgments** — NIST assessors, graded 0–3, pooled across participating runs.
The gold standard, with the classic pooling caveat: a system unlike anything in
the pool retrieves unjudged documents and is penalised.
**Access** — `ir_datasets`, NIST. Open.
**Adoption** — the IR community's reference point; less used by the ML side,
which is a real cultural split.
**KM meaningfulness** — high.
**Drop-in?** Yes.
**Known failure modes** — small query sets mean wide CIs; pool bias against
genuinely novel methods (**directly relevant to Leonardo's question — a clever
regex retriever is exactly the kind of system a pool built from neural runs
under-judges**).
**Verification** — `desk-research`.
**Refs** — Craswell, Mitra, Yilmaz, Campos et al., annual overviews.
**TODO** — get per-year query counts and judgment depth; compute what effect
size is resolvable at those n. I suspect it is large and that this is the
strongest quantitative point in the whole document.

### BRIGHT (2024/2025)
**What it measures** — **reasoning-intensive** retrieval: queries where lexical
and semantic similarity are insufficient and relevance requires inference.
**Unit / size** — 1,398 real-world queries across 12 datasets (Biology, Earth
Science, Economics, Psychology, Robotics, StackOverflow, Sustainable Living,
LeetCode, Pony, AoPS, TheoremQA-Theorem, TheoremQA-Question).
**Metric** — NDCG@10.
**Judgments** — derived from naturally occurring links/answers.
**Access** — HuggingFace; in `mteb`.
**Adoption** — high and rising; ICLR 2025 Spotlight. Has spawned BRIGHT-PRO, a
multimodal variant, and TEMPO (temporal reasoning retrieval, arXiv:2601.09523).
**KM meaningfulness** — **high, and unusual**: these are questions a person
would actually ask a knowledge base and where keyword search fails.
**Drop-in?** Yes.
**Known failure modes** — the strong results require LLM-augmented pipelines
(query expansion/rewriting), which **confounds retriever quality with generator
quality** — precisely the confound that makes "is my embedding better" hard to
answer. Reproducibility was poor enough that a dedicated paper exists
(*Lighting the Way for BRIGHT: Reproducible Baselines*, arXiv:2509.02558).
**Verification** — **`deep-read`** (arXiv:2407.12883v4, ICLR 2025, pp. 1–6 +
Table 1) **and analysed** in `bright_headroom_and_resolving_power.py`.
**Refs** — Su, Yen, Xia, Shi, Muennighoff, Wang, Liu, Shi, Siegel, Tang, Sun,
Yoon, Arık, Chen, Yu, *BRIGHT*, ICLR 2025. arXiv:2407.12883. OpenReview
`ykuc5q381b`. Data: `huggingface.co/datasets/xlangai/BRIGHT`, code
`github.com/xlang-ai/BRIGHT`.

#### WHY IT IS A BETTER INSTRUMENT THAN BEIR, AND NOT BECAUSE IT IS HARDER

1,384 queries total; **76–194 per dataset**, against BEIR's 49–13,145. On pure
resolving-power logic that should be worse. It is not, and the reason is a
principle I have not seen stated:

> **Choose a benchmark by its headroom-to-noise ratio, not by its size.**

Using the σ = 0.133 *measured* in `can_we_tell_retrievers_apart.py` (not assumed):

| effect | NDCG points | × per-dataset detection floor |
|---|---|---|
| BEIR → BRIGHT drop for the leading MTEB model (59.0 → 18.3) | 40.7 | 12.4× |
| LLM chain-of-thought query reasoning | **12.2** | **3.7×** |
| a typical claimed BEIR SOTA increment | 1.0 | **0.3×** |

The reasoning intervention is measurable on **one** 103-query BRIGHT subset. A
one-point BEIR increment is invisible on any single BEIR subset and survives only
in an average whose variance is 78% driven by four tiny subsets.

And BRIGHT's *average* is the sharper instrument despite one-twentieth the
queries — MDD 0.94 points vs BEIR's 0.40–1.01 — because its query counts are
**balanced** (largest subset share of the average's variance: 12.1%, against
BEIR's 23%). **Balance beats size.**

#### Three properties that matter for an agentic method specifically

- **Relevance is defined by reasoning**, not surface overlap: a document is
  positive iff it "helps reason through the query with critical concepts or
  theories", unanimously agreed by an annotator plus two PhD reviewers. A system
  that *thinks before it searches* is what the benchmark is for — unlike a
  pooled TREC collection, where an unusual system retrieves unjudged documents
  and is scored down.
- **Negatives are adversarially semantic**: annotators Googled for topically
  similar pages that do not meet the query's specific requirement. Cosine
  similarity is insufficient *by construction*, so a clever multi-step or
  rule-based system has room to win rather than merely to match.
- **Leakage-resistant structurally**: no substantial gains even when models are
  further trained on the benchmark's documents, because the difficulty is in the
  query–document *relation*. That beats a fresh test set, which only works until
  it is published.

**The one caution**, and it is the same confound Gabín et al. hit in RAG: the
headline gains come from LLM-augmented pipelines (query rewriting, CoT), which
mixes retriever quality with generator quality. If we build something agentic and
it wins on BRIGHT, the honest decomposition needs **the same generator on both
sides** — otherwise we will have measured the LLM we happened to use.

**TODO** — read arXiv:2509.02558 (*Lighting the Way for BRIGHT: Reproducible
Baselines*); download the HF dataset and run my `rules_coordmatch` on it, since
BRIGHT is where a rule-based system is least disadvantaged.

### Others in this family — logged, not yet analysed
- **LoTTE** (ColBERTv2, 2022) — long-tail topic-stratified StackExchange search.
  Good KM fit. `TODO: analyse`.
- **NanoBEIR** — sub-sampled BEIR for cheap iteration. **Directly relevant to
  the n\* question: what did sub-sampling cost?** `TODO: analyse, high priority`.
- **CoIR** — code retrieval benchmark. `TODO`.
- **MLDR** — multilingual long-document retrieval (from BGE-M3). Long documents
  are the KM-realistic case. `TODO`.
- **TREC-COVID, NFCorpus, SciFact, FiQA, TREC-Robust04** — BEIR constituents
  worth analysing individually; several are the *most* KM-meaningful parts.
- **HTEB — Harder Text Embedding Benchmark** (arXiv:2605.28190), "Beyond
  One-dimensional Static Robustness". Post-cutoff; found 2026-08-13. `TODO: read`.

### Reasoning-intensive and *agentic* retrieval — the branch to watch

Leonardo, 2026-08-13: *"maybe in the future you will contribute to this field,
and more likely will be something more agentic than a pure embedding model, so
benchmarks like this one are of special interest."* Agreed, and the reason is
structural rather than fashionable: an agentic retriever's whole advantage is
that it can take **more than one step**, and a benchmark whose relevance is
defined by *surface overlap* cannot reward that. BRIGHT's is defined by
*reasoning*, which is why it is the right family.

PDFs and LaTeX sources for all of these are fetched (see §Fetching); none read
in depth yet.

- **BRIGHT-PRO** — a three-way split of BRIGHT (StackExchange / Coding /
  Theorem) for finer-grained evaluation. `TODO: locate the primary source; I
  have only a secondary mention.`
- **TEMPO** (arXiv:2601.09523) — *A Realistic Multi-Domain Benchmark for
  Temporal Reasoning-Intensive Retrieval*. Temporal reasoning is the KM case
  that matters most for a knowledge base that ages. `TODO: read early.`
- **Rethinking Reasoning-Intensive Retrieval: Evaluating and Advancing
  Retrievers in Agentic Search Systems** (arXiv:2605.04018) — the title is
  precisely the question. **Highest-priority read in this subsection.**
- **Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via
  Direct Corpus Interaction** (arXiv:2605.05242) — "direct corpus interaction"
  is the agent-browses-rather-than-embeds paradigm; if that is where things go,
  a vector index is not the unit of analysis at all. `TODO: read.`
- **RankEvolve** (arXiv:2602.16932) — *Automating the Discovery of Retrieval
  Algorithms via LLM-Driven Evolution*. Directly relevant to Leonardo's premise:
  it is a machine **inventing** the retrieval algorithm. If it works, the
  question stops being "is my new method better" and becomes "can the search be
  automated end-to-end", and evaluation reliability becomes the binding
  constraint rather than ideas. `TODO: read — possibly the most important paper
  in this document for us specifically.`
- **MRMR** (arXiv:2510.09510) — expert-level multidisciplinary multimodal
  reasoning-intensive retrieval. `TODO.`
- **ICLR 2026 poster: Trade-offs in LLM Compute for Reasoning-Intensive
  Information Retrieval** — quantifies the compute/quality frontier for exactly
  the agentic case. `TODO: find the paper.`

**The evaluation problem this family creates, and that none of them has solved:**
if the retriever calls an LLM, the benchmark measures retriever ⊗ LLM. Every
comparison must therefore hold the LLM fixed across arms, and none of the
abstracts I have read says that it does. This is the same confound as
`gabin2026-lost-in-the-evidence` and `mazuryk2026-powerless-noise`, arriving in a
new subfield that has not yet had its reproduction paper. **That reproduction
paper is a thing we could write.**

---

## 4. End-to-end RAG benchmarks

### CRAG — Comprehensive RAG Benchmark (2024)
**What it measures** — factual QA with mock web and knowledge-graph search APIs,
over 5 domains (finance, sports, music, movies, open encyclopedia) and 8
question types including **false-premise** questions.
**Unit / size** — 4,409 question–answer pairs.
**Metric** — a 4-way scoring (perfect / acceptable / missing / incorrect) with a
scoring rule that **penalises hallucination relative to abstention**. This is
the most thoughtful scoring design in the catalogue.
**Judgments** — **manually verified ground truths**, with automatic evaluation
mechanisms provided.
**Access** — `github.com/facebookresearch/CRAG`; AIcrowd challenge infrastructure.
**Adoption** — KDD Cup 2024: **2.5K+ participants, 5.6K+ submissions**. NeurIPS
2024 D&B.
**KM meaningfulness** — high; explicitly includes time-sensitive and
false-premise questions, which are the failure modes a real knowledge base has.
**Drop-in for a new embedding?** **Partly.** It evaluates the whole system, so a
retriever improvement is measured through a generator. Good for "does my
retriever help end-to-end", bad for isolating the retriever.
**Known failure modes** — mock APIs are a simulation of web search, not web
search. Being a *competition* dataset, the public split has been heavily
optimised against since 2024.
**Verification** — `desk-research`, web-checked 2026-08-13.
**Refs** — Yang et al., *CRAG — Comprehensive RAG Benchmark*, arXiv:2406.04744.
Competition site `kddcup24.github.io`. Systems/findings write-up:
IEEE Data Eng. Bull. Dec 2024, p.163.
**TODO** — **this is the best example of criterion 1 (automatically verified,
sandboxed, competitive) in the whole catalogue.** Study the AIcrowd harness as a
model for what a zoo-internal auto-evaluated challenge would look like.

### TREC RAG Track (2024, 2025)
**What it measures** — retrieval + generation with attribution, over MS MARCO
V2.1. The 2025 edition adds **long, multi-sentence narrative queries** ("deep
search").
**Unit / size** — 2025: **150+ submissions**. Topic counts `TODO`.
**Metric** — multi-layered: relevance assessment, response completeness,
**attribution verification**, and *agreement analysis*. Uses the
**AutoNuggetizer** framework — automatic nugget-based evaluation validated
against human nuggets.
**Judgments** — NIST + LLM-assisted nuggetisation. **The agreement analysis
between automatic and human nuggets is the crux**: it is the field's most
serious attempt to license automatic evaluation of generated text.
**Access** — NIST TREC. Participation requires registration for the live track;
data released after.
**Adoption** — high and institutional.
**KM meaningfulness** — very high. Narrative queries with attribution is exactly
the knowledge-management task.
**Drop-in?** For the retrieval sub-task, yes.
**Known failure modes** — LLM-based nugget assignment inherits LLM-judge
correlated error (see `instance-papers/areas/llm-monoculture-and-correlated-errors.md`
— if judges' errors correlate, a leaderboard partly measures the judge).
**Verification** — `desk-research`, web-checked 2026-08-13.
**Refs** — *Overview of the TREC 2025 RAG Track*, arXiv:2603.09891;
`trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf`. AutoNuggetizer:
arXiv:2411.09607. Related: **TREC 2025 RAGTIME Track**, arXiv:2602.10024.
**TODO** — **highest-priority deep read in this document.** Read 2603.09891 and
2411.09607 together and extract the human/automatic agreement numbers. That
agreement statistic is the single number that says whether automatic RAG
evaluation is trustworthy at all.

### KILT (2021)
**What it measures** — knowledge-intensive language tasks over **one unified
Wikipedia snapshot** — fact checking, entity linking, slot filling, open QA,
dialogue. Provenance is required, not just the answer.
**Unit / size** — 11 datasets, one shared corpus (~5.9M Wikipedia pages,
*unverified*).
**Metric** — downstream accuracy **plus KILT-scores that require correct
provenance** — i.e. you only get credit if you retrieved the right evidence.
**That design is exactly right for KM.**
**Access** — `github.com/facebookresearch/KILT`; HuggingFace.
**Adoption** — high, though somewhat superseded.
**KM meaningfulness** — very high: provenance-conditioned scoring is the
knowledge-management criterion.
**Drop-in?** Yes for the retrieval component.
**Known failure modes** — Wikipedia-only; snapshot ages; provenance annotations
incomplete for some tasks.
**Verification** — `desk-research`.
**Refs** — Petroni et al., *KILT*, NAACL 2021, arXiv:2009.02252.
**TODO** — check whether the provenance-conditioned metric is still maintained.

### Logged, not yet analysed
- **FRAMES** (Google, 2024) — factuality + retrieval + reasoning in one. `TODO`.
- **RGB** (Chen et al., AAAI 2024) — noise robustness, negative rejection,
  information integration, counterfactual robustness. Directly related to the
  Power-of-Noise line I read in depth. `TODO: high priority`.
- **MultiHop-RAG** (2024). `TODO`.
- **RAGBench** — large multi-domain RAG benchmark with explainable labels. `TODO`.
- **LongBench / LongBench v2**, **HELMET**, **RULER**, **BABILong** —
  long-context evaluation; RULER and BABILong are synthetic (weak on criterion 4),
  HELMET is application-shaped. `TODO`.
- **FreshQA / FreshLLMs** — time-sensitive questions, **regenerated over time**,
  which is the only structural answer to contamination in this list.
  `TODO: high priority — the contamination-resistance design is the interesting part`.
- **LegalBench-RAG**, **FinanceBench**, **CUAD**, **BioASQ**, **TREC BioGen** —
  domain-specific, high KM meaningfulness. `TODO`.
- **RIKER / "Coherent Simulated Universe"** (arXiv:2601.08847) — *Scalable and
  Reliable Evaluation of AI Knowledge Retrieval Systems*. Post-cutoff, found
  2026-08-13, title squarely on Leonardo's question. `TODO: read early`.

---

## 5. Automatically-verified platforms — the criterion-1 shortlist

This is the section that matters most for "VERY CONFIDENT", because it is the
only one that attacks *who produces the evidence*.

### TIRA / TIREx — The Information Retrieval Experiment Platform
**What it is** — you submit a **Docker image**, not a run file. TIRA executes it
in a sandbox **with internet access disabled** against read-only mounted data
you never see, so blinded evaluation and exact re-execution are both possible.
Integrates `ir_datasets`, `ir_measures` and PyTerrier.
**Unit / size** — **15 corpora, 1.9 billion documents, 32 shared retrieval
tasks**, all open for submission. 50 standard retrieval approaches already
imported as baselines, from BEIR (17), PyTerrier (20 lexical), ChatNoir, ColBERT,
duoT5, PyGaggle, Pyserini.
**Metric** — `ir_measures`, and the evaluator runs **sanity checks first**: score
ties, NaN scores, empty result sets, unknown queries, **scores contradicting the
ranks**. That is a "print the comparison, not the conclusion" discipline built
into the platform, and it is unusual.
**The field that changes everything** — the evaluator "derives all specified
measures averaged over all queries **and per query (suitable for significance
tests)**". **TIREx computes and retains σ.** That is the number I said in §1(d)
that nobody publishes; the platform has it for every run of every one of the
50 baselines on all 32 tasks. **This is the single most valuable fact in this
document.**
**Drop-in for a new embedding / distance / rule-based retriever?** **Yes, and it
is designed for exactly this.** They added `default_text` fields to `ir_datasets`
so that single-field retrieval software runs on multi-field corpora without
adaptation. Full-rank and re-rank are separate submission types, and re-rank
files are cached, so a new reranker runs on any previous stage's output. A pile
of regexes goes in a Docker image and is scored on 32 tasks.
**Scalability, measured** — 50 approaches × 32 tasks = **1,600 runs, finished in
under a week** on 1,620 CPU cores and 24 GPUs, "started by just clicking a
button".
**Adoption** — CLEF labs (PAN, Touché) since 2012; SemEval 2023 (71 of 171
registered teams, 647 runs). Thin on the ML-side embedding community — the gap.

#### THE FINDING THAT ANSWERS LEONARDO'S QUESTION DIRECTLY (their Table 6)

They took every pairwise system preference established on **TREC DL 2019** and
asked how often it reproduces on a *different* task:

| task | rank | preference reproduces | median effect ratio |
|---|---|---|---|
| TREC DL 2020 | 1 | **88.1%** | 0.90 |
| Touché 2020 (Task 2) | 2 | 77.1% | 0.38 |
| Web track 2004 | 3 | 75.5% | 0.29 |
| TREC-7 | 4 | 73.9% | 0.31 |
| Core 2018 | 5 | 70.2% | 0.24 |
| NFCorpus | 10 | 66.4% | 0.06 |
| Web track 2003 | 15 | 57.8% | 0.04 |
| Web track 2009 | 20 | 44.1% | −0.04 |
| Web track 2010 | 25 | 36.3% | −0.14 |
| Web track 2013 | 30 | **31.0%** | −0.21 |

*Effect ratio: 1 = the improvement reproduces perfectly, 0 = it vanishes,
negative = it reverses.*

**A demonstrated improvement fails to hold on a different task between 12% and
69% of the time, and on the harder half of the tasks the median improvement
retained is essentially zero or negative.** This is measured, on 1,600 runs, by
the people who built the platform. It is the quantitative form of the answer to
"could we be VERY CONFIDENT", and the answer is: not from one benchmark, ever.

#### CORRECTION, 2026-08-13 — I said this platform had "rotted". It has not.

Earlier the same day I wrote that TIREx's public API had rotted, on the evidence
that `www.tira.io/api/datasets` served HTML and `all_datasets()` returned `None`.
**That conclusion was wrong and I am correcting it prominently rather than
quietly.** What I had actually found was two things I misread:

- `www.tira.io` serves a Discourse forum **at the paths I guessed**. The API is
  alive, public and unauthenticated at the correct path:
  `https://tira.io/api/task-list` returns JSON, role `guest`, **95 public tasks,
  9 flagged `is_ir_task`, 129 IR datasets between them.** Verified by direct
  HTTP.
- The failure is a **stale default in the pip client**, not in the platform:
  `tira` 0.0.203 requests `/tira-backend/api/task-list`, which 404s everywhere,
  while `/api/task-list` works on `tira.io`, `www.tira.io` and `archive.tira.io`.
  Worth reporting upstream.

The genuine client defect worth recording: `all_datasets()` returned `None`
instead of raising, which is what let me draw a wrong conclusion from one call.
A method that answers "nothing" when it means "I failed" is the silent-failure
shape I have a whole KB entry about.

#### HOW WE WOULD ACTUALLY MAKE A SUBMISSION — verified end to end, 2026-08-13

Docker 29.3.1 is present on this machine and running. `python -m pip install
tira` gives `tira-cli`, `tira-run`, `tira-run-inference-server`,
`tira-run-notebook` (note: `pip` is not on PATH in Git Bash here — use
`python -m pip`, and the scripts live in `.../Python310/Scripts/`).

```
1. Register       tira.io/tasks -> pick task -> REGISTER (creates a group).
                  All 9 IR tasks require registration.
2. Install        python -m pip install tira
3. Authenticate   tira-cli login          (API key from your submit page)
4. Check          tira-cli verify-installation
5. Build          a Docker image that is POSIX-compatible, self-contained, and
                  RUNS WITH NO INTERNET. It reads $inputDataset and writes
                  $outputDir. Nothing else is prescribed.
6. Submit         tira-cli code-submission --path <dir> --task ir-benchmarks
                  (git repo must be clean -- checked via `git status` -- and
                   contain the Dockerfile)
7. Run            task page -> select submission, resources, dataset -> RUN.
                  Public datasets evaluate immediately; private/test are
                  released by the organisers.
```

`tira-cli verify-installation` already runs here and reports exactly one problem
— *"Your TIRA client is not authenticated"* — which is the correct diagnosis and
the only blocker. (It crashes on Windows without `PYTHONIOENCODING=utf-8`,
because it prints a ✖ glyph; minor, worth reporting.)

**The task to submit to is `ir-benchmarks`** — that is TIREx itself: 40 datasets,
and it hands participants a starter re-ranking image with the contract already
written:

```
image:   webis/tira-application:0.0.36
command: /irds_cli.sh --input_dataset_directory $inputDataset \
                      --output_dataset_path $outputDir --rerank $inputRun
```

**And the decisive practical point: we can rehearse the entire thing offline.**
`tira-cli run` executes approaches locally and `tira-cli evaluate` evaluates runs
locally, against `ir_datasets` collections that already work on this box. So a
new method can be built, containerised, and scored end-to-end here, and the
submission is then only about *who computes the evidence* — which is the entire
reason to use TIREx at all.

**Remaining barriers, honestly** — (i) registration is a human step and requires
an account; (ii) the 9 IR tasks report `software_count` 0 to a guest, so I cannot
confirm from the API how much is live versus archived, and the labs are dated
2022–2024; (iii) Docker images must be self-contained, so anything that calls an
LLM API is out unless the weights ship inside; (iv) little uptake outside IR.
**Verification** — **`deep-read` + `ran-it`**: client installed, CLI executed,
API queried directly, Docker confirmed. Not submitted (needs an account).
**Refs** — Fröbe, Reimer, MacAvaney, Deckers, Reich, Bevendorff, Stein, Hagen,
Potthast, *The Information Retrieval Experiment Platform*, SIGIR 2023,
arXiv:2305.18932. Related: `ir_metadata` (Breuer & Keller).
**TODO** — (a) reach the live platform through the documented GitLab/Docker path
rather than the REST API, and report the rot upstream if confirmed; (b) **ask
whether the per-query score files for the 1,600 runs are obtainable** — that
would be the largest σ dataset in existence and would let n\* be computed for
32 tasks at once; (c) design a zoo-internal harness on this shape.

### TREC / NTCIR / CLEF (annual evaluation campaigns)
**What they are** — the institutional form: fresh topics each year, blind
submission before judgments exist, pooled human assessment afterwards.
**Why it matters** — **fresh topics per year is the only contamination defence
that actually works**, and pre-judgment submission is the only way to be sure
nobody tuned on the answers.
**Cost** — you must participate in the cycle; you cannot evaluate on demand.
**TODO** — check TREC 2026 track list and deadlines. If a zoo method were ever
serious, submitting to a live track is the highest-credibility move available.

### KDD Cup / AIcrowd / Kaggle
**What they are** — hidden test sets, leaderboard, submission limits, a public/
private split to catch leaderboard overfitting.
**Why it matters** — CRAG (§4) proves the model works for RAG at scale.
**Weakness** — one-shot events; the dataset degrades into a normal public
benchmark afterwards.
**TODO** — inventory currently-live retrieval/RAG challenges.

---

## 6. Access and tooling layer

The practical answer to criterion 2. **Check this list before writing any
evaluation code.**

| tool | what it gives | note |
|---|---|---|
| `ir_datasets` | unified access to a very large number of IR collections, queries, qrels | the single most useful package here; MacAvaney et al., SIGIR 2021 |
| `ir_measures` | one interface over `trec_eval` and friends | |
| `mteb` | run an embedding model over ~130 tasks with one call | best-in-class ergonomics; assumes vectors + cosine |
| `beir` | BEIR loading and evaluation | |
| `pyterrier` | full IR experiment pipelines, `pt.Experiment` with significance testing built in | and `pyterrier_rag` for RAG pipelines — this is what Gabín et al. 2026 used |
| `ranx` | fast ranking evaluation, fusion, **statistical comparison**; `ranxhub` shares pre-computed runs | the significance-testing support is why it belongs here |
| `trec_eval` | the reference C implementation | |
| `ir_metadata` | extensible metadata schema for IR experiments | the closest thing in IR to our `paper.json` |

**Verified on this box, 2026-08-13** (`python -m pip install tira ir_datasets
ir_measures` — note `pip` alone is not on PATH here, use `python -m pip`):

- `ir_datasets` **0.6.3 — works, no JVM needed.** Downloads and parses on
  demand. Loaded `vaswani` (11,429 docs), `cranfield` (1,400), `beir/scifact/test`
  (5,183), `antique/test` (403,666) without incident.
  **It independently confirmed my BEIR transcription**: `beir/scifact/test`
  reports 300 queries, 5,183 docs, 339 qrels → 1.1 rel/q, exactly matching the
  BEIR paper's Table 1. That is a transcription check for free.
- `ir_measures` 0.4.3 + `pytrec_eval_terrier` 0.5.10 — installed clean.
- `tira` 0.0.203 — installs; the REST API is unreachable (see the TIREx entry).
- **PyTerrier — not attempted**, needs a JVM. `TODO`.
- `ranx` — not attempted. `TODO`.

**TODO** — PyTerrier + JVM, and `ranx` for its significance testing.

---

## 7. Meta-evaluation — papers about whether benchmarks work

This section is the intellectual core, and it is where my last two sessions
already contributed.

- **PTEB** (arXiv:2510.06730) — stress-tests semantic invariance by **paraphrasing
  the evaluation set at eval time, multi-run**, giving a statistically robust
  protocol instead of one static score. `TODO: read — this is the closest published
  thing to the multiverse discipline I have been arguing for.`
- **The Flaw of Averages: Quantifying Uniformity of Performance on Benchmarks**
  (arXiv:2509.25671) — directly attacks MTEB-style mean-of-tasks. `TODO: read`.
- **Maintaining MTEB** (arXiv:2506.21182) — the maintainers on long-term
  usability and reproducibility. `TODO: read`.
- **Submodular Benchmark Selection** (arXiv:2605.02209) — principled subset
  selection. Bears directly on NanoBEIR and on n\*. `TODO: read`.
- **HTEB** (arXiv:2605.28190). `TODO: read`.
- **Lighting the Way for BRIGHT** (arXiv:2509.02558) — reproducible baselines.
  `TODO: read`.
- **Voorhees** on pool reliability and assessor disagreement; **Sakai** on
  statistical reform in IR; **Fuhr's** "Some Common Mistakes In IR Evaluation,
  And How They Can Be Avoided" (SIGIR Forum 2017). *Classics; I know them from
  pretraining and have not re-read them.* `TODO: get primary sources`.
- **Already in this KB, and load-bearing:**
  - `instance-papers/areas/rag-and-knowledge-management.md` — n\*, specification
    dispersion, the 3.3× CI-to-spread ratio, the Δ-checksum method.
  - `instance-papers/areas/llm-monoculture-and-correlated-errors.md` — why an
    LLM-judged leaderboard partly measures the judge.
  - `instance-general/philosophy-of-science/verification-economics-of-open-science.md`
    — artifact badging is a measured null result; the missing FAIR letter is V.

---

## 8. TODO queue — priorities for the next sessions

**Tier 1 — answers Leonardo's question most directly**
1. Deep-read **TREC 2025 RAG Track** (arXiv:2603.09891) + **AutoNuggetizer**
   (arXiv:2411.09607). Extract the automatic-vs-human agreement statistics.
2. Deep-read **TIREx** (arXiv:2305.18932). Decide whether a zoo-internal
   auto-verified retrieval benchmark should be built on it or imitate it.
3. ~~Fill in judgments-per-query for every BEIR subset and compute n\* and
   minimum resolvable effect.~~ **DONE 2026-08-13** — see the BEIR entry in §3
   and `beir_resolving_power.py`. Follow-ups: (a) redo for the actual published
   subset lists (18-set and the 13–15 redistributable set); (b) the same
   treatment for **MTEB** — much harder, because the average spans 8 task
   families with different metrics and the per-task n are not in one table;
   (c) find out whether σ has *ever* been published for any IR benchmark.

**Tier 2 — breadth**
4. Analyse to template: FreshQA, RGB, NanoBEIR, LoTTE, FRAMES, HELMET, RULER.
5. Read **RIKER** (arXiv:2601.08847), **PTEB**, **Flaw of Averages**,
   **Maintaining MTEB**, **Submodular Benchmark Selection**.
6. Establish exactly what changed **MTEB v1 → v2** and hunt for any published
   comparison that straddles the break.

**Tier 3 — infrastructure**
7. `tools/fetch_benchmark_papers.sh` exists (see below) — extend it as entries
   are added; keep PDFs **outside** the KB, per the 50 MB rule.
8. Verify the §6 tooling actually installs here; record what needs a JVM.
9. Consider a `paper.json` record for each benchmark once deep-read, so
   `kb.py query --method retrieval-evaluation` and `kb.py quantities --about
   judgments_per_query` work. **The catalogue and the record store should not
   fork** — this file is the prose argument, the records carry the numbers.

**Open questions I cannot yet answer**
- Is there *any* benchmark in this catalogue where a purely rule-based retriever
  (regexes, no learning) can be evaluated without a pool bias penalty? Pooling
  systematically under-judges systems unlike those that built the pool, and every
  modern pool is built from neural runs. **If the answer is no, that is a serious
  finding and it directly limits what Leonardo can be confident about.**
- What is the smallest *real* improvement anyone has demonstrated on BEIR that
  survived independent replication? If the honest answer is "we don't know",
  that is the answer to the headline question.

---

## Fetching primary sources, and where heavy things live

Heavy assets are **registered, not hidden.** As of 2026-08-13:

```
python tools/assets.py where     # prints the current root
python tools/assets.py list      # what exists, how big, how to regenerate it
python tools/assets.py verify    # sizes and hashes still match?
python tools/assets.py relocate <path>   # move everything, one command
```

Root resolution: `$ZOO_ASSETS` → `tools/assets.conf` (committed) → `~/zoo-assets`.
The manifest (`assets-manifest.json`) lives **in** the KB because it is small
metadata worth versioning; the bytes live outside it. Currently on `D:` (the
`DATA` volume, following the existing `D:/<project>_assets/` convention), which
is one command away from any external drive Priya prefers.

`tools/fetch_benchmark_papers.sh <dir>` downloads arXiv PDFs **and LaTeX source
bundles** for everything cited here. 29 papers, ~124 MB. Re-runnable, idempotent.

**Prefer the LaTeX source over the PDF for anything with a table.** BEIR's
Table 1 came out clean and greppable from `neurips2021.tex`; from the PDF it
would have been an eyeball estimate. That single habit is the difference between
this catalogue's numbers being checkable and being approximate.

## Executable analyses in this folder

| script | what it establishes | status |
|---|---|---|
| `beir_resolving_power.py` | BEIR's minimum detectable difference per subset; the small-subset domination of the average | runs, no deps beyond numpy |
| `can_we_tell_retrievers_apart.py` | **measures σ** on 3 real collections; 6 hand-written retrievers incl. a rule-based one; paired bootstrap; τ, n\*; cross-collection preference transfer | runs, needs `ir_datasets` |
| `bright_headroom_and_resolving_power.py` | BRIGHT's resolving power using the *measured* σ; the headroom-to-noise principle | runs, numpy only |
