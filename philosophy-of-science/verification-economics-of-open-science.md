# Verification economics — why open-science interventions keep failing, and which one doesn't

Status: active. Author: mark. Written 2026-08-05.
Companion to `construct-validity-and-formalization.md` (maria): that entry asks whether
formalizing helps; this one asks who is obliged to *check*, and what the measured return
on each checking mechanism actually is. Extend in place.

## The delta — measured outcomes, not intentions

Numbers first, because this field runs on advocacy and the advocacy is not tracking the data.

**Replication (new data, same protocol → same conclusion).**
- SCORE (DARPA-funded, 7 years, 865 researchers, ~3,900 papers 2009–2018 across 62 journals
  in 11 social/behavioural fields). Results published in *Nature*, April 2026. Replication
  succeeded for **151/274 claims (55.1%)** and **49.3% of papers** when weighted for multiple
  claims per paper. Sourcing caveat: I read the *Nature* news write-up, Karolinska's summary
  and *Science*'s news piece, not the three primary papers (paywalled at time of writing).

**Computational reproducibility (same data + same code → same numbers — a far weaker bar).**
- General computational research: ~**26%** of articles computationally reproduce.
- Hydrology: **0.6–6.8%** reproducible from available data/code.
- Ecology: only **27%** of eligible articles even *had* code attached.
- NeurIPS 2019: code availability self-reported at **38.8%** at submission, **27.7%** when
  reviewers actually checked. The 11-point gap is the entry fee for trusting self-report.
- 2015 study: **32.3%** of code-backed papers could be obtained and built within 30 minutes.
- Another: 40% of papers had artifacts × 44% of those ran ⇒ ~**18%** end-to-end.

**Artifact evaluation / badging — the null result that matters most.**
- A large-scale study across four top security conferences found that introducing Artifact
  Evaluation Committees produced **no statistically significant improvement** in artifact
  availability or functionality. Badging is optional, declinable without penalty, and runs
  *after* accept/reject at most venues, so it cannot affect the decision it would need to
  affect.

**Institutional fragility.**
- Papers with Code — the most successful "science as code" artifact ML ever had (~18k papers,
  9,327 leaderboards, 79,817 paper↔code links, 5,628 datasets, CC-BY-SA) — was sunset by Meta
  on **24–25 July 2025 with no prior notice**. The raw data dump survives on GitHub, frozen;
  **the leaderboards did not survive**. Hugging Face took over "trending papers" only.

## The synthesis

**1. Every failed intervention shares one mechanism: the party who benefits from the claim
also produces the evidence for it.** Badges, checklists, availability statements and
"reproducibility statements" are all self-report with a rubber stamp. That is why they show
null effects, and it is why the NeurIPS self-report/reviewer-check gap is 11 points. The
diagnosis is not "researchers are lazy"; it is that no mechanism obliges a *disinterested*
party to look.

**2. Therefore the missing FAIR letter is not E (Executable), it is V (Verified by someone
other than you).** The E-agenda has the most tooling of any branch — containers, Binder,
RO-Crate, Whole Tale, workflow provenance — and computational reproducibility is still ~26%.
Execution is not the binding constraint. Disinterested attention is. CODECHECK is the only
initiative whose design admits this: a *named third party* re-runs the code and signs a
time-stamped certificate. Its scale (~25 reproductions) is the honest price of the mechanism
that actually works, because the cost is human attention, not Docker.

**3. Three bars are routinely conflated, and conflating them is how a weak result gets sold
as a strong one.** Keep them separate always:
- *re-executable* — same code+data reproduces the numbers. Machine-checkable. Cheap.
- *replicable* — new data, same protocol, same conclusion. Expensive. ~50% in social science.
- *correct* — the inference is valid. **Not checkable by re-running anything.**
Containers and attestation attack bar 1 only. Badging attacks bar 1 and mostly fails.

**4. Machine-checked proof is the only artifact in this landscape that attacks bar 3 and is
simultaneously checkable without trusting the producer.** A Lean/Rocq development can be
re-checked by a kernel the reader controls; no trust in the author, no trust in a host, no
trust in a hosted platform. Its scope is brutally narrow — deductive claims only, nothing
empirical — but *within that scope* it is strictly stronger than everything else here, and
this is under-argued in the reproducibility literature, which is almost entirely written by
and for empirical fields. Documented instances of formalization catching real defects in
published work: Voevodsky–Kapranov (1989 proof, disproved by Simpson 1998), Tao's own 2023
Maclaurin-type inequality paper (non-trivial bug found while formalizing), Scholze/Clausen
(Lean settled the step Scholze was unsure of, 2021). Buzzard's stated motivation is exactly
this: as a referee he could not determine whether an argument was rigorous.

**5. Cryptographic attestation ("nonrepudiable results", arXiv 2605.08586, Sigstore/in-toto
lineage) is solving a narrower problem than its framing implies.** It proves *that a
computation ran and produced this output*. It does not show the computation was the right
one, that the data was not selected, or that this was the 40th run. Against p-hacking and
the garden of forking paths — the actual drivers of the 50% replication rate — it does close
to nothing. It is genuinely useful against one thing: post-hoc alteration of results, i.e.
outright fraud. Adopt it for that and do not let it be described as reproducibility.

**6. Design for the death of your host.** Any verification scheme depending on a hosted third
party inherits that party's mortality; Papers with Code is the proof and EOSC's own governance
documents are openly about survival past the current funding framework. A verification
artifact should be a self-contained repository that survives its host. A git repo containing
proofs + a machine-readable catalogue does. A results database on someone's platform does not.

## One-line answer usable elsewhere

Open science has spent twenty years making results *easier to check* and almost no effort
making them *obligatorily checked by someone who does not benefit* — which is why the tooling
branch has the best funding and the worst measured return.
