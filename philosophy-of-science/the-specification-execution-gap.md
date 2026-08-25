<!--kb
id: the-specification-execution-gap
labels: measurement, construct-validity, epistemology, meta-research, instruments
triggers: my instrument measures what people were told to do not what they did; does a requirements file tell me the environment; prescription versus state; protocol fidelity measures the manual; a badge says the artifact was checked once; declared versus executed; why do cheap measures cluster on one side; is my measure of the process a measure of the outcome; text-based measure of a mental practice; the crosswalk rows are untested causal hypotheses; what would change if the specification were followed perfectly and the result were still wrong; instruction space versus state space
verified: 2026-08-25
-->

# The instrument measures the specification, and the field reads it as the execution

Status: active. Author: maria. Written 2026-08-25, out of noticing the same
structure in two fields I work in that share no literature, no method and no
people.

---

## The claim

Between the **specification** of a process and its **execution** there is always
a gap. Instruments that are cheap to apply live almost entirely on the
specification side, because a specification is a document and an execution is an
event. Documents can be read at scale; events have to be caught happening.

So the cheap measure measures the specification. And then the field reports it as
though it had measured the execution, usually without anyone deciding to.

**The gap is not noise around the measurement. It is the object most of these
fields actually care about.**

## Two instances that share nothing

I found this in one field and then, weeks later, walked into it in another. They
have no authors, no methods and no citations in common, which is the only reason
I trust the pattern — see `independence-the-hidden-premise-of-agreement.md`.

**Contemplative science.** A text-based measure of a meditation practice scores
the *instruction*: what the teacher said, how constrained the attention target
is, whether an object is named. Lutz et al.'s (2015) seven-axis matrix is a
*phenomenological* space — its coordinates are properties of experienced states.
The two are different spaces, and every mapping between them is an untested
causal hypothesis (*instruction X produces state Y*) that nobody can have tested,
because one side has never been measured at scale. The field reads instruction
scores as state descriptions. Detail:
`psychology-of-meditation/lutz-taxonomy-and-cat.md`.

**Computational reproducibility.** A `requirements.txt` is a *declaration* of an
environment, not an environment. Every population-scale study of whether research
code runs measures declared environments — and reports the result as a fact about
whether the science re-executes. When you look for the execution side, it is
missing in the same way:

- a **Dockerfile** is a recipe, not an image. It rebuilds 72% of the time under
  two years, which nobody had measured until 2026 (`malka2026-docker-reproducibility`);
- an **archive node** is a pointer when its files come from a provider add-on.
  It answers HTTP 200 with a title and a wiki long after the repository it points
  at is deleted (`laurinavichyute2022-share-the-code`);
- a **badge** records that someone checked once, in their own environment.
  AJPS runs mandatory third-party verification and 29.1% of its R files
  re-execute in a clean container.

- **"open access" itself.** Unpaywall reports `is_oa: true` for Artner et al.
  (2021) and gives exactly one location: a KU Leuven bitstream path that returns
  **404**, because the repository migrated to a new discovery system and the
  index still holds the pre-migration deep link. The *specification* of openness
  is intact and indexed; the *execution* — can a reader get the bytes — fails.
  Found 2026-08-25 while trying to verify a cost figure, and the figure is still
  unverified because of it.

Two more instances the pattern predicts and which I have not checked:
**protocol-fidelity instruments** in clinical trials score the manual, and
**preregistration** scores the plan.

## Why the cheap measure always lands on the wrong side

Not conspiracy and not laziness. Three ordinary forces, all pushing one way:

1. **A specification is durable and an execution is not.** The manual is still
   there in ten years; the session is not. Whatever survives is what gets
   measured.
2. **A specification is countable.** You can score a thousand documents. Catching
   a thousand executions means instrumenting a thousand events.
3. **The specification side is where compliance lives.** Policies, mandates and
   badges can only require things that can be checked, so they require documents,
   and then the documents become the evidence base.

Hardwicke's *Cognition* result is this in one line: a mandatory open-**data**
policy moved data availability to ~99% and moved analysis-script sharing from
8.7% to 6.0%. **Mandates get you what they ask for**, and what they ask for is
always the checkable thing.

## The diagnostic

One question, and it is cheap:

> **What would change in my measurement if the specification were followed
> perfectly and the outcome were still wrong?**

If the answer is *nothing*, the instrument measures the specification. That is
often fine — but it must then be reported as such, and it must not be pooled with
measures of the outcome.

A second question for anyone building a crosswalk between a specification space
and an outcome space:

> **Has anyone ever measured the other side?**

If not, every row of the crosswalk is a hypothesis, not a translation. Writing it
as a table makes it look like a translation. That is a presentation problem with
epistemic consequences.

## What follows, practically

- **Say which side you measured, in the sentence that carries the number.** Not
  in limitations. "34% of papers reproduced" and "34% of papers whose declared
  materials permitted an attempt reproduced" are different claims and only one is
  true.
- **Do not pool across the gap.** A rate about declarations and a rate about
  executions are not two measurements of one quantity, however similar the words.
- **When you must work on the specification side, say what the causal step is.**
  Then it is a hypothesis with a name rather than a silent identification.
- **Expect the two sides to disagree most exactly where the field is most
  confident**, because confidence is what stops people checking the other side.

## The residue I have not resolved

Whether the gap is a defect to be closed or a permanent feature. In contemplative
science it looks permanent: instruction text cannot in principle carry attentional
*stability*, because a static instruction is precisely what produces unstable
attention in a novice. That is a boundary, not an incompleteness.

In reproducibility it looks closable in principle — you *can* run the code — and
it stays open because running it is expensive, and expensive checks are the ones
that get replaced by cheap proxies. Which suggests a third question I do not know
how to answer: **when a field substitutes a specification measure for an execution
measure, does it know it has done so?** In both fields I looked at, the
substitution is not argued anywhere. It is simply what the available instrument
did, and the interpretation followed the instrument.
