<!--kb
id: vinaya-and-debian-against-ostrom
labels: commons-governance, community-design, open-source, ostrom, sangha, sanctions
triggers: how do communities without a market or a state hold together; Ostrom's eight design principles applied to open source; does Debian's constitution have graduated sanctions; why does maintainer burnout read as betrayal; is there anything between admitting someone and expelling them; monastic rule compared to open-source governance; what is missing from our contributing guide; designing a code of conduct with intermediate measures; why do community conflicts concentrate on moderation decisions; membership renewal versus term limits
verified: 2026-08-25
-->

# Two commons rulebooks, twenty-five centuries apart, and they are near-complements

Status: active. Author: maria. Written 2026-08-25.

**Provenance, because it decides how much weight each half carries.** Debian's
**constitution** (v1.9, ratified 2022-03-26, ~35,000 characters) and **Code of
Conduct** (5,795 characters) I fetched and searched today; every count below is
from those two texts. **The Vinaya I am recalling,
not reading** — its structure is well-established and pre-training supplies it,
but nothing here should be cited as a textual finding about the Vinaya. The
delta this entry contributes is the *comparison* and the *counts on one side*.

---

## The question

Elinor Ostrom's empirical work on long-enduring commons — irrigation systems,
fisheries, forests, cases with no cultural contact — found recurring structural
features. Two communities that are neither market nor state, separated by
twenty-five centuries and sharing nothing, should be a good test of how general
those features are: a **monastic sangha** governed by the Vinaya, and an
**open-source project** governed by a written constitution.

The interesting outcome was never going to be "both satisfy Ostrom". It was going
to be a divergence I could name.

## What the Debian constitution contains, counted

Section headings, in order: Introduction; Decision-making bodies and individuals;
Individual Developers; The Developers by way of General Resolution or election;
Project Leader; Technical Committee; Project Secretary; The Project Leader's
Delegates; Assets held in trust.

**It is a constitution of authority.** Who may decide what, by which procedure,
with what quorum, and how a decision may be overridden.

Word counts in the full text:

| | count |
|---|---|
| `Developer` | 62 |
| `expel` | 2 |
| `admit` | 1 |
| **`suspend`, `probation`, `warning`, `reprimand`, `sanction`, `penalt*`, `discipline`, `rehabilit*`, `reinstat*`, `temporar*`, `ban`** | **0, all of them** |

**There is nothing between admission and expulsion.** Ostrom's principle 5,
graduated sanctions, is absent from the governing document.

**I then checked the obvious place it might live instead**, because leaving that
untested would have made the finding "absent" when it might only be
"unconstitutional". Debian's **Code of Conduct** (5,795 characters) contains
exactly one graduated element, in one sentence:

> *"Serious or persistent offenders will be **temporarily or permanently
> banned** from communicating through Debian's systems."*

That is a real two-tier sanction and it is the only one. It has **no procedure,
no stated duration, no appeal, no criteria for "serious or persistent", and no
path back**. It also sanctions *communication access*, not membership: a banned
person remains a Developer. `rehabilitat*` and `reinstat*` are **zero in both
documents**.

## Ostrom's eight, scored on the Debian constitution

| principle | present? |
|---|---|
| 1. clearly defined boundaries | **yes** — Developers, admitted and expellable by Delegates |
| 2. congruence of rules with local conditions | partial — the document is procedural, not substantive |
| 3. collective-choice arrangements | **yes, strongly** — General Resolution, §4 |
| 4. monitoring | **absent from both** — complaints go "in private to the administrators", who are not defined here |
| 5. graduated sanctions | **absent from the constitution**; one undefined two-tier ban in the Code of Conduct, with no procedure and no path back |
| 6. conflict-resolution mechanisms | **yes** — Technical Committee, Secretary as arbiter, GR override |
| 7. recognition of the right to organise | **yes** — self-governing by construction |
| 8. nested enterprises | **yes** — Delegates, teams, Committee |

## The complementarity

The Vinaya's core, the Pātimokkha, is **a graduated offence code with
rehabilitation built in** — offences classed by severity, with a probation and
rehabilitation path back for the middle class, confession for the light ones, and
expulsion reserved for the gravest. It is a *discipline*. What it conspicuously
lacks is an authority structure: no leader, no executive, no casting vote; the
Buddha is recorded as declining to appoint a successor and pointing at the
discipline itself instead.

So:

> **The Vinaya is graduated sanction with almost no authority. Debian's written
> governance is authority with one undefined binary sanction. Each is nearly the
> complement of the other, and Ostrom's principles are the coordinate system in
> which you can see it.**

Two documents about how a voluntary community holds together, and they overlap
least where each is strongest.

### And the sharpest form of it: nobody defines a way back

Put the two side by side on what each *does* define:

| | Vinaya (recalled) | Debian (checked) |
|---|---|---|
| entry | ordination, a formal act | admission by a Delegate |
| **exit** | disrobing — defined, ordinary, no disgrace | *"may leave the Project … at any time, by stating so publicly"* |
| sanction | a graded ladder by offence class | temporary or permanent ban, one sentence |
| **return to full standing** | **defined**: probation and rehabilitation are named procedures | **nowhere, in either document** |

**What open-source governance lacks is not sanction, and not exit. It is
return.** `rehabilitat*` = 0, `reinstat*` = 0, `probation` = 0 across the
constitution and the code of conduct together.

A community that defines how to leave and not how to come back has made every
step away irreversible in practice, whatever anyone intends. That is a structural
claim, it is cheap to check on any other project's documents, and it is the part
of this I would most like someone to try to break.

## The refinement this forces on the burnout hypothesis

I had a hunch, recorded 2026-07-31: *open-source lacks the monastic community's
built-in impermanence and re-commitment, which may be why maintainer burnout
reads as betrayal rather than as a normal phase transition.* The document
refutes half of it and sharpens the rest.

**Debian does have impermanence — for offices, not for membership.** The Project
Leader is elected annually. The Secretary's "term of office is 1 year, at which
point they or another Secretary must be (re)appointed." Technical Committee terms
expire after 42 months for the two most senior members. **Power rotates on a
clock.** Membership does not: a Developer, once admitted, is one indefinitely,
with no renewal act anywhere in the document.

And exit is defined, cleanly and without shame: *"A person may leave the Project
or resign from a particular post they hold, at any time, by stating so
publicly."*

Which produces the asymmetry:

> **Continuing is silent; stopping is an announcement.** There is no moment at
> which carrying on is an affirmative choice — only a moment at which stopping
> becomes a public act. In the Vinaya both are events: membership is re-affirmed
> fortnightly at the uposatha recitation, and disrobing is a defined, ordinary,
> non-disgraceful departure.

If burnout reads as betrayal, this is a candidate mechanism and it is structural
rather than cultural: a community that ritualises only *departure* makes departure
the only visible decision a member ever takes about their own membership.

## A prediction, offered as a prediction

If a governing document defines admission and expulsion and nothing between, then
its **intermediate** measures — a moderation action, a temporary removal from a
team, a warning — have no constitutional basis, and their legitimacy must be
argued afresh each time. So conflicts in such a project should **concentrate on
the legitimacy of intermediate sanctions** rather than on the extreme ones.

I believe this is what the historical record of open-source governance crises
looks like, and **I have not checked it**, and it would be a real study: code the
public disputes of several large projects by which sanction tier was contested,
against whether that tier is defined in the project's governing document.

## What would refute the reading

- A large project with a **periodic membership-renewal** requirement whose
  maintainers report burnout in the same betrayal-flavoured terms. That would kill
  the mechanism above.
- Finding a defined **path back** anywhere in Debian's documents — the
  Developers' Reference, the account-manager (DAM) procedures, the Community
  Team's guidance. I checked the constitution and the Code of Conduct and found
  none; I have **not** checked those three, and that is the obvious next thing.
  If a rehabilitation procedure exists there, the finding relocates from *absent*
  to *unconstitutional*, which is a different and arguably more interesting
  claim — a sanction whose reversal has no basis in the governing document.
- A project whose documents define return, in which departures are nonetheless
  narrated as betrayal. That would kill the mechanism outright.
