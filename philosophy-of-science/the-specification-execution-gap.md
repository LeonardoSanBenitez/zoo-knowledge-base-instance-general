<!--kb
id: the-specification-execution-gap
labels: measurement, construct-validity, epistemology, meta-research, instruments
triggers: my instrument measures what people were told to do not what they did; does a requirements file tell me the environment; prescription versus state; protocol fidelity measures the manual; a badge says the artifact was checked once; declared versus executed; why do cheap measures cluster on one side; is my measure of the process a measure of the outcome; text-based measure of a mental practice; the crosswalk rows are untested causal hypotheses; what would change if the specification were followed perfectly and the result were still wrong; instruction space versus state space; does the URL resolving mean the file is there; the check passed and the artifact is dead; git lfs pointer 404; osf link returns 200 but nothing is there; artifact presence versus artifact sufficiency; how do I know my link checker is measuring anything
verified: 2026-09-08
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

## A third instance, at the smallest possible scale: one HTTP request (added 2026-09-08)

The two instances above are whole fields. The same structure appears inside a
single check, and there it can be *measured with a control*, which the field-scale
instances cannot.

**The specification side:** does the identifier resolve? **The execution side:**
does the thing it points at hold the bytes the paper depends on?

A project in this house (`dev-science-ops/paper-retrospective-reproducibility`)
had already noticed this and wrote the deciding question into its check:

> Not "does the DOI resolve" but "does the thing it points at still hold bytes".

**It is still on the wrong side, and two archives show it in different ways.**

**OSF.** Four identifiers were fetched on 2026-09-08 — one live deposit, one the
authors had deleted, and two GUIDs invented as controls:

| GUID | `osf.io/<guid>` | `api.osf.io/v2/guids/<guid>/` |
|---|---|---|
| `xerhg` — live | HTTP 200, 4,207 B | **200**, `size: 1301939` |
| `gb76x` — deleted | HTTP 200, 4,207 B | **410 Gone** |
| `zzzz9` — invented | HTTP 200, 4,207 B | **404** |
| `qqqqq` — invented | HTTP 200, 4,207 B | **404** |

All four responses are **byte-identical**, same sha256. OSF serves a
client-rendered single-page application, so the shell is the same whether or not
the resource exists. A resolution check on OSF has *zero* discriminating power —
not weak, zero — and the two invented GUIDs are what proves it.

**GitHub, via Git LFS.** A repository's headline data file, 335 MB by its own
declaration, is a 134-byte pointer whose object is gone:

| endpoint | result |
|---|---|
| `raw.githubusercontent.com/.../<path>` | **HTTP 200, 134 bytes** — the pointer |
| `media.githubusercontent.com/media/.../<path>` | **HTTP 404** — the object |
| GitHub tree API `size` | **134** |

**The target holds bytes. They are the wrong bytes.** A pointer is present,
non-empty, hashable and useless, and every LFS-using repository on GitHub has
this shape.

### What this instance adds that the field-scale ones could not

**(a) A control is available, and it costs one line.** *Run your check against an
identifier you invented.* If the invented one passes, the check measures nothing.
Two fabricated GUIDs demolished a check that had been trusted for a month. At
field scale nobody can fabricate a paper; at request scale the null case is free.
This is the cheapest instance of the general rule in
`the-null-is-a-modelling-choice.md`: **write down what a false pass looks like,
and then produce one.**

**(b) A partial answer to the residue below — and it is not the comforting one.**
The closing question of this entry asks whether a field *knows* it has substituted
a specification measure for an execution measure. Here it did know. The
substitution was explicitly argued against, in the source file, in the imperative
mood, by the person who then wrote the check. It happened anyway.

The mechanism is worth naming, because it is not carelessness: **the deciding
question is host-specific and the wording of a check is host-agnostic.** "Does it
hold bytes" is a genuine execution-side question in the abstract. Whether a given
request answers it depends on how *that* host behaves when the answer is no — an
SPA shell, an LFS pointer, a soft-404 landing page, a login wall returning 200.
So the specification-side check is not the one someone lazily wrote instead; it is
what the execution-side question *degrades into* the moment it is expressed
portably.

**Consequence: an execution-side check is only execution-side on hosts where
someone has looked.** A check written once and applied to *n* archives is a
specification measure on every archive but the one it was written against.

**(c) Presence and sufficiency are different properties, and only presence is ever
checked.** The LFS case has a second half. Everything *derived* from the dead file
survives — the pair-level tables, the code, the figures — so the paper can be
**re-executed**. What cannot be done is anything item-level: changing the null
model, recomputing with a different baseline, deciding whether the deposited table
is the exact run behind the paper. **The cheap bar passes and the expensive one is
blocked**, and no badge, validator or availability policy distinguishes them.
Concretely, in that package four of eight printed numbers reproduce only to the
last digit, the discrepancy is real and small, and *the artifact that would decide
it is the one that 404s.*

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
