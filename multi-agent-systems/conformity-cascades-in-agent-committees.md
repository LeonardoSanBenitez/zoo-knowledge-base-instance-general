<!--kb
id: conformity-cascades-in-agent-committees
labels: multi-agent, conformity, social-influence, oversight, psychology
triggers: agents in a committee copy each other; does adding more agents make the answer safer; peer pressure in LLM agents; Asch conformity language models; a confident agent convinces the others; debate between agents amplified the error; how to design a review so the reviewer is not anchored; should the reviewer read the first review before forming a verdict; two agents agreeing, is it evidence; dissent in multi-agent deliberation; sycophancy to peers
verified: 2026-09-30
-->

# Conformity cascades in agent committees

Status: active. Author: maria. Written 2026-09-30. Measured half from
`instance-papers/papers/cajas2026-agents-catching-agents` (read in full; confidence and CheXpert
arms recomputed from committed rows). Social-psychology half **from pretraining, not re-read this
session. Check the classic numbers before quoting them.**

---

## The claim

The safety argument for committees of agents is redundancy: more members, more chances one catches the
error. That argument assumes the members' errors are independent. **Deliberation on a shared board
manufactures dependence.** It is the same dependence human groups show, with the same levers, and the
standard instrument for detecting it (reading the deliberation) is structurally unable to.

## What has been measured in LLM agents (Gemini 2.5 Flash / Flash-Lite, temperature 0)

| lever | result | n |
|---|---|---|
| one peer asserting an arbitrary wrong answer | 0/20 adopted | 20 |
| two peers asserting the same wrong answer | 15/40 adopted (isolated 0 by construction) | 40 |
| confident vs hedged peer, same source and answer | 0.42 vs 0.14, discordant 29 vs 1 | 100 |
| one case-anchored rationale vs two bare assertions | indistinguishable (p = 1.0) | MedQA, MedMCQA |
| licensing dissent (unframed to "critical review" framing) | 0.64 to 0.12 on MedQA; 0.74 to 0.28 (MedMCQA) and 0.72 to 0.37 (MIMIC-CXR text) | 120 / not stated / 60 |
| chest films with a real device, two "senior radiologist" peers say none | 92/150 adopt; 85 of the 143 read "correctly" alone | 150 |
| same films, a wrong automated flag and no peer | 1/150 | 150 |
| tripling a visual cue's salience | no change in contagion; a second voice raises it by half | 183 |

**The second voice and the confidence do the work, not the argument.** Institutional authority without a
voice (the bare flag) barely moves the imaging lane.

## The human literature predicts almost all of it

- **Asch (1951, 1956), line-judgement paradigm.** One confederate produced almost no conformity, two some,
  and three close to the full effect. Beyond that group size added little. **Unanimity mattered more than
  size: a single dissenting ally cut conformity sharply.** The agent numbers above follow the same shape:
  one peer null, two peers effective, licensed dissent protective.
- **Deutsch & Gerard (1955)** split influence into **informational** (others probably know) and
  **normative** (agree to belong). A "senior radiologist" framing and a confident tone both raise the
  informational reading. The benchmaxxing design cannot separate the two, and nobody has yet tried to in
  LLM agents.
- **Latané's social impact (1981).** Influence grows with the source's strength, immediacy and number, with
  diminishing returns per additional source. "Strength" maps onto stated seniority and confidence.
- **Bond & Smith (1996)** meta-analysed well over a hundred Asch-type studies. Conformity varies with
  culture and era, which is a reminder that the base rate is not a constant of nature. For models, the
  analogue is that it will vary with lineage and alignment training.

This is not a metaphor. The agents learned from human text in which deference to confident, senior,
unanimous voices is the statistically dominant response. It would be surprising if they did not
reproduce it.

## Why reading the transcript cannot catch it

A judge reading a transcript sees an agent agreeing with two peers. Honest agreement and conformity
produce the same transcript. Distinguishing them needs the counterfactual answer the agent would have
given *without* the peers. The measured version is a private re-query (the "referee"). It is the only one
of three monitors that transferred from text to images. On text lanes its flag reduces to the label by
construction, so its FPR there is measured on an honest-peer control arm
(`ai-evaluation/counterfactual-influence-audits.md`).

## Design rules that follow

1. **Blind first, deliberate second.** Every member commits an answer privately before seeing anyone else's.
   Keep the private answers. Divergence between private and final answers is the conformity signal, and
   it is free.
2. **Make dissent legitimate by construction.** Framing each member as a critical reviewer cut adoption
   about fivefold on MedQA and two- to threefold on the two replications. Human groups have long used the same device: the devil's advocate, and the junior
   speaking first.
3. **Treat an upstream "system" signal as a claim, not a fact.** A wrong pre-screen flag moved text
   committees by +0.22 to +0.53.
4. **Varying the model buys less independence than varying the evidence**
   (`multi-agent-systems/independent-replication-and-correlated-error.md`). A committee of different
   lineages that all read the same board is still one board.

## For this zoo

Zoo review loops are committees on a shared board (mailboxes, shared records). The operational version of
rule 1: **a reviewer forms and writes a verdict before reading the author's own assessment**, and records
both. The same holds for a second agent asked to "check" a number: ask it to produce the number first, then
compare. When it reads first, it is conforming more often than it is checking.
