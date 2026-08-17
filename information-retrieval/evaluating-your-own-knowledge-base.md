# Evaluating your own knowledge base — how to measure whether it is working, and the four ways the measurement lies

```toml
schema  = "zoo-topic-entry/typed/0.1"
id      = "evaluating-your-own-knowledge-base"
kind    = "synthesis"
status  = "active"
areas   = ["information-retrieval", "knowledge-management"]
authors = ["maria"]
created = 2026-08-18
updated = 2026-08-18
verified = 2026-08-18
confidence = "verified"
triggers = [
  "how do I know if our knowledge base is actually being used",
  "I added structure to my notes but is retrieval any better",
  "my before and after numbers look too good, what did I do wrong",
  "how many test queries do I need before a retrieval comparison means anything",
  "is a document nobody has ever opened worth keeping",
  "we keep writing documentation that nobody finds",
]
sources = [
  "instance-general/information-retrieval/benchmarks-for-retrieval-and-rag.md",
  "zoo-knowledge-base/tools/retrieval_eval.py",
  "simple-ontology-for-knowledge-bases/CONFORMANCE.md sections 3-5",
]
see_also = ["doc:ir-rag-benchmark-catalogue", "performative-thoroughness-and-reward-bias"]
```

Author: maria, 2026-08-18. Written from a measurement that went wrong twice in
two days on this KB. Every trap below is one I actually fell into, in the order
I fell into it. Extend in place; do not fork.

## The delta

Not "how to evaluate an IR system" — that is a field with textbooks, and the
public-benchmark landscape is catalogued in
`benchmarks-for-retrieval-and-rag.md`. This is the narrower, less-written case:
**you have a small internal corpus, you are both its author and its evaluator,
and you are trying to decide whether some change to how you write is worth the
cost.** That situation defeats most of the standard advice, because the usual
protections — an independent test set, a blind assessor, enough queries — are
all absent by construction.

## 1. Measure being reached, not being tidy

The only thing a knowledge base is for is that when someone has a need and
states it in their own words, the thing that would help comes back. Well-formed
headers, consistent folders, controlled vocabularies are *instrumental*. A
corpus can improve on all of them and get worse at the only thing that counts.

Two asymmetric readings, and the asymmetry is the useful part:

* An entry **never retrieved** is strong evidence against its existence.
* An entry **often retrieved** is weak evidence for it. Retrieval is not use — a
  document can be returned and ignored.

So the actionable signal is the cold list, not the hot list. And the sharpest
signal of all is a **miss**: a query that returned nothing states a need in the
words it arrived in, which is exactly what the corpus lacks and exactly the
text a new entry's triggers should contain.

## 2. Trap one — the reader that skips what it cannot parse

I measured that 21 of 40 entries had never been retrieved, saw they were exactly
the ones lacking a header, and concluded *missing header → unreachable*. I wrote
it into four documents as the measured basis for a new format.

The tool only indexed files that already had a header. Those entries were not
badly ranked; they were **absent from the index**. The report described the
reader while looking exactly like a report on the corpus.

> **Any tool that skips the documents it cannot parse will eventually produce
> evidence that everyone should adopt the format it can parse.**

Fix: index everything — path, title, body — so a missing header costs **rank**,
never **existence**. This also happens to be the only way to honestly test
whether the format is worth anything, because "structured entry vs. nothing at
all" could never have come out any other way.

Generalises well beyond knowledge bases: a benchmark that drops the cases its
metric handles badly; a survey that reaches only the people who answer surveys.

## 3. Trap two — writing the answers after seeing the questions

I froze a gold set *before* converting the entries, which felt rigorous. Then I
wrote each entry's `triggers` *while looking at that gold set*. Four of six
triggers were near-copies of their query. Result: 0/6 → 6/6, all at rank 1.

A before/after that lands on a perfect score is not a strong result, it is a
**contaminated** one. The tell is the same as everywhere else in empirical work:
agreement that is too clean means the two sides are not independent.

Fix: a **held-out** set, written after the change, deliberately in vocabulary
the entry does not use. On that set the same change went 0.253 → 0.460 mean
reciprocal rank — real, but a fraction of what the contaminated set claimed.

## 4. Trap three — reporting a rate when you have one observation

The held-out improvement looked like "roughly doubles MRR". Then:

* **Leave-one-query-out**: dropping the single most favourable query takes the
  mean improvement from +0.207 to +0.068. **67% of the effect is one query.**
* **Exact paired sign test**: 4 of 4 non-tied queries improved, none worsened —
  p = 0.125.
* **And 0.125 is the floor.** With six paired queries and two ties there are
  only 2⁴ = 16 sign assignments, so no effect of any size could have produced
  p < 0.125.

That last point is the one people miss. Reporting "not significant at 0.05"
from such a design is a statement about the *design*, not about the change.
Both readings are available and neither is free.

The honest report is therefore: **one observation with a consistent direction.**
Not a rate, not a multiplier.

> Report always: **n**, the **floor on p** at that n, **leave-one-out
> sensitivity**, and **who wrote the gold set.**

Leave-one-out matters more than the p-value here, because a p-value hides
concentration and leave-one-out exposes it.

## 5. Trap four — being your own assessor

A gold set written by the corpus's author, who knows what every entry says, is
usable **only** as a before/after comparison of that corpus against itself. Its
absolute values (MRR 0.46, recall@3 0.67) mean nothing and must not be quoted.

There is no clean fix available to a solo author. The partial ones:

* Have **someone else** write queries for entries they did not author. Cheap,
  and worth more than another feature.
* Harvest queries from **logged misses** — those were not written for the test,
  which is precisely what makes them good.
* Freeze the set and never add a query after seeing a bad result. Adding one is
  fitting the test to the answer, and it feels like diligence while it happens.

## 6. Resolving power, borrowed from the public-benchmark literature

The companion entry records that several standard IR subsets cannot resolve
differences below a few points — Touché-2020, TREC-COVID and TREC-NEWS cannot
resolve anything under ~5 NDCG points, and 78% of the variance of the headline
average comes from the four smallest subsets.

The transfer is direct and slightly humiliating: **it is incoherent to demand
resolving power of a public benchmark with 50 queries and not of the internal
set of 6 you used to justify your own format.** Before running a comparison,
compute what the design can detect. If the answer is "nothing at the threshold I
intend to use", the choice is to enlarge the set or to report the result as an
observation — not to run it and interpret whatever comes out.

## 7. What this says about structure, so far

On this corpus, measured: added structure bought **nothing** for queries phrased
the way the entry is written, and helped (direction consistent, magnitude not
established) when phrased differently. The mechanism, if real, is narrow and
worth stating because it is not the obvious one:

> Structure pays where the **writing is most personal** — a synthesis in its
> author's own idiom, which readers will search for in words it does not
> contain. It pays least on material already full of the exact strings people
> search with (error messages, version numbers, proper nouns).

Which is roughly the opposite of the intuition that structured formats suit
factual material and get in the way of thinking.

## Open, and unmeasured

* **Decay.** Whether typed `verified` dates and stated re-verification
  procedures pay for themselves is untested here. It is not a retrieval claim
  and none of the above bears on it. Needs a different measurement: how often
  does someone act on a fact that had gone stale?
* **Scale.** Everything above was measured at ~30 entries. Assume the relevance
  floor and the scoring weights break first.
* **Lexical ceiling.** Token overlap cannot bridge "choiceless awareness" ↔
  "open monitoring"; both held-out control failures were exactly that. No amount
  of front matter raises that ceiling — only more triggers, or embeddings, and
  embeddings need a dependency and a build step.
