# Lutz et al. meditation taxonomy vs. the CAT 10-dimension model

```toml
schema  = "zoo-topic-entry/typed/0.1"
id      = "meditation-lutz-taxonomy-and-cat"
kind    = "synthesis"
status  = "active"
areas   = ["psychology-of-meditation", "measurement-theory"]
authors = ["maria"]
created = 2026-07-01
updated = 2026-08-21
verified = 2026-08-21
confidence = "verified"
triggers = [
  "how are focused attention and open monitoring meditation actually defined",
  "is a meditation taxonomy categorical or dimensional",
  "the styles of meditation in a taxonomy do not map onto what my questionnaire measures",
  "what can a new meditation dimension model honestly claim as novel",
  "which Lutz paper should I cite for the phenomenological matrix",
]
sources = [
  "Lutz, Slagter, Dunne & Davidson 2008, Trends in Cognitive Sciences",
  "Lutz, Jha, Dunne & Saron 2015, American Psychologist 70(7):632-658",
]
see_also = ["gamma2021-mpe92m"]
```

Status: active. Author: maria. Written 2026-07-01, **substantially corrected
2026-07-29** (the original framing "CAT is dimensional where Lutz is categorical"
was an overclaim — see the correction section). Referenced by
`cat_introduction_draft.md` in `.claude/memory/maria/` — this entry is the
durable version of an argument that currently only exists compressed inside
the paper draft. Anyone on the team is welcome to extend or correct this
entry — edit in place, don't fork a duplicate.

## ⚠ Correction (2026-07-29) — read before using this in the paper

The original version of this entry framed CAT's contribution as the move from a
*categorical* Lutz taxonomy to a *dimensional* CAT model (Big Five / HiTOP
analogy). **That framing is wrong and would be fatal in Related Work.** There
are two Lutz papers, not one:
- **Lutz, Slagter, Dunne & Davidson (2008)**, *Trends in Cognitive Sciences* —
  the FA/OM *categorical* taxonomy. This is what the sections below describe.
- **Lutz, Jha, Dunne & Saron (2015)**, *American Psychologist* 70(7):632–658 —
  the **"phenomenological matrix": an explicitly dimensional, continuous,
  seven-axis multidimensional space** into which practices are plotted as
  points. Three primary/functional axes (object orientation, dereification,
  meta-awareness) + four secondary/qualitative axes (aperture, clarity,
  stability, effort). They *already* say "avoid the temptation to equate
  mindfulness instructions with any particular phenomenological state" and plot
  FA/OM as regions, not kinds.

So the dimensional move is **not** CAT's novelty — Lutz made it in 2015. CAT
cannot claim it. See "CAT's honest delta" below for what CAT can actually claim.

## The 2008 categorical taxonomy (what the sections below describe)

Lutz, Slagter, Dunne & Davidson's 2008 taxonomy splits meditation into a small
number of families by **attentional mechanism**:
- **Focused Attention (FA)** — sustained selection of and return to a single
  object (breath, mantra), monitored and corrected for lapses.
- **Open Monitoring (OM)** — non-selective, non-reactive awareness of whatever
  arises, without sustaining any single object.
- (later extensions add compassion/loving-kindness practices and
  non-dual/effortless practices as further families, not reducible to FA/OM
  combinations.)

This is a **mechanism-first, small-N typology**: practices are sorted into a
handful of buckets by their presumed cognitive operation.

## CAT's honest delta (rewritten 2026-07-29)

Against the *2008 categorical* taxonomy, CAT's dimensional framing is still a
real contrast — FA/OM as regions, not natural kinds; within-family
heterogeneity a categorical model can't represent (Anapanasati vs. Goenka body
scan, both FA-adjacent, differ sharply on D2/Somatic Engagement). Keep this
argument. But it is an argument against the *2008* paper, and the Related Work
section must acknowledge Lutz 2015 exists or a reviewer will sink it.

Against the *2015 matrix*, which is already dimensional, CAT's genuine
contribution is **not the dimensional idea but its operationalization**:
1. **Scorability from text at scale.** Lutz's matrix is a conceptual tool;
   its plotted points are, in the authors' own word, "hypothetical" — placed by
   expert judgment, not measured. CAT proposes explicit rubrics + a two-pass
   (keyword + LLM) pipeline that actually *scores* transcripts. The move from
   "a space one could plot practices in, in principle" to "a reproducible
   measurement procedure that assigns coordinates to a real corpus" is the
   delta. This is measurement, not ontology.
2. **A different, more granular, observable-marker-oriented axis set** (10 axes
   incl. Attentional Constraint, Somatic Engagement, …), designed around
   linguistic markers detectable in instruction/report text — where Lutz's
   seven axes are pitched at the level of neurocognitive function.
3. **A concrete convergence/comparison obligation, not yet done:** map CAT's 10
   axes onto Lutz's 7 (object orientation ≈ ?, dereification ≈ D9?,
   meta-awareness ≈ ?, aperture ≈ D1 Attentional Constraint?, stability ≈ D1?,
   effort ≈ ?). Where they align = convergent validity; where CAT has no analog
   of a Lutz axis (e.g. *dereification* — the sense that experiences are mental
   events, not reality) that may be a CAT gap. Note the same gap the
   contemplative-neuroscience reading flagged: self/subject-object structure.

Positioning sentence for the paper (honest version): *"CAT is not the first
dimensional model of contemplative experience — Lutz et al.'s (2015)
phenomenological matrix already replaced categorical typology with a
seven-dimensional space. CAT's contribution is to operationalize a dimensional
model for reproducible, text-based scoring at corpus scale, with a finer-grained
axis set built around observable linguistic markers."*

---

## ⚠ SECOND CORRECTION, 2026-08-13 — the positioning sentence above is still wrong

The crosswalk got built (working draft: `.claude/memory/maria/cat_lutz_crosswalk.md`)
and it exposed a category error underneath the one already corrected here. The
durable, generally-reusable part is this, and it is why the correction lives in
the KB rather than only in my notes:

> **Lutz-7 is a STATE space. CAT-10 is an INSTRUCTION space.**
> Its own first design rule is *"observable from instruction text alone — we
> score transcripts, not phenomenology"*. Lutz's paper is titled *"the
> **phenomenological** matrix"*. These are not two descriptions of one object.

Consequences:

1. **A crosswalk between them is not a translation table. Every row is an
   untested causal hypothesis** of the form *instruction feature X reliably
   produces state feature Y*. Nobody has tested any of them, because one side has
   never been measured at scale.
2. The novelty anxiety dissolves. The dimensional move was never CAT's and does
   not need to be — **the object is different**, and that is the contribution.
3. Two structural facts fall out that neither model's authors could see alone:
   - **Lutz-7 has no affect axis and no relational axis.** Metta and Vipassana
     occupy nearly the same point modulo object orientation, which is
     phenomenologically absurd. CAT's D7 and D10 fill a real hole.
   - **Lutz plots practices as POINTS; a body scan is a TRAJECTORY.** A
     point-based space cannot encode a practice that moves through it, so a
     phased practice is represented by a location it may never occupy. CAT's D6
     (Temporal Dynamics) is exactly that missing coordinate.
4. And a principled limit, which is the most useful negative result: **stability
   is not measurable from instruction text, ever.** A static instruction is what
   produces *unstable* attention in a novice. This belongs in Limitations as a
   boundary, not as an incompleteness to be fixed later.

**The generalisation worth flagging to anyone outside contemplative science:**
every text-based measure of a mental practice — therapy manuals, coaching
scripts, protocol-fidelity instruments — has this structure. The instrument
measures the **prescription**, and the field silently reads it as the **state**.
If that is right it is a methodological point with a far wider audience than this
topic, and it may be its own paper.

Replacement positioning sentence (supersedes the one above):

> Lutz et al. (2015) established that mindfulness-related practices are better
> represented as positions in a continuous multidimensional space than as
> categories. That space is *phenomenological* — its coordinates are properties
> of experienced states and its points are, by the authors' own description,
> hypothetical and expert-placed. CAT proposes a distinct and complementary
> space whose coordinates are properties of the *instruction*, observable in text
> and scoreable at corpus scale. The two are related by causal hypotheses the
> field has never been in a position to test, because one side of every such
> hypothesis has never been measured. CAT's contribution is that side.

## ⚠ THIRD UPDATE, 2026-08-21 — the blocking question is resolved, and not the way either lineage predicted

Re-opened Lutz 2015 directly (own PDF, `johnddunne.net` mirror, read pp.632-645)
and re-ran the MPE-92M split-half reanalysis's own numbers against it. Full
derivation in `.claude/memory/maria/cat_lutz_crosswalk.md` §6; durable summary
here.

**Lutz's own text answers "is dereification the same axis as self-structure?"
directly, on p.640** — quoting Hölzel et al.'s "disidentification with the
static sense of self": *"We understand this to be a species of the more
general capacity for dereification ... this does not occur with all cases of
dereification ... [it] does not require that one's sense of being a static
self has changed."* So by Lutz's own account, self-disidentification is a
**special case** of dereification (content-based: dereifying specifically the
thoughts that construct a self), not an independent axis and not the same axis.

**My own data complicates that answer, but LESS than a first draft of this
section claimed — corrected same session.** The first-draft version asserted
the self/subject-object factor was "more stable under split-half replication
than most of the instrument's other factors" and used that as a second,
independent pillar alongside the textual argument. That claim was inherited
from an uncomputed eyeball read in a 2026-08-16 note and turned out to be
wrong when actually computed: a proper independent-halves check
(`gamma2021-mpe92m/reanalysis/run_self_factor_stability.py`, 30 splits, self-
factor identified within each half separately, no full-sample leakage) gives
the self factor **median rank 3rd of 5 and 5th of 7 matched factors** — average
to slightly below-average stability, not exceptional. (A first attempt at the
permutation-null control for this same check also had a bug — a pandas
`.apply(axis=0)` that silently failed to reshuffle rows — that produced a
null median as high as the real data; fixed with an explicit per-column numpy
shuffle, after which the null behaves as expected, median 0.14 vs the real
data's 0.80, so the self factor's signal is genuinely above noise, just not
unusually more replicable than the instrument's other real factors.)

**What survives, honestly:** the self/subject-object factor carries real,
above-noise variance in a population selected for minimal discursive-thought
content (MPE-92M's "pure awareness" respondents) — which rules out the
*strongest* reductive reading (self-structure as pure epiphenomenon of
thought-dereification, which should have gone to the noise floor there) but
does NOT positively demonstrate that self-structure is a privileged,
functionally separable dimension the way exceptional stability would have.
Ordinary-stability-but-real is compatible with either Lutz's species-of
account or the embodied-self lineage's primacy account, and does not decide
between them.

**Decided for CAT: D11 Dereification and D-self stay two separate dimensions**,
resting mainly on the textual argument (Lutz's own general/specific relation
licenses distinct instructions — content-reappraisal language vs. self/
boundary-targeting language are different instructions regardless of the
underlying phenomenology), with the data offering only mild, non-decisive
corroboration rather than a second independent pillar. Discriminant-validity
check still owed once real transcripts are scored: does anything score
high-D11/low-D-self or high-D-self/low-D11? If the off-diagonal stays empty,
revisit.

## Open, not yet resolved

- Which specific CAT dimensions predict the FA/OM split best, empirically —
  needs real transcript data (pending from Mark's pipeline), not armchair
  mapping. Don't overclaim until checked.
- ~~The full CAT-10 ↔ Lutz-7 crosswalk is unstarted.~~ **Drafted 2026-08-13,
  blocking question resolved 2026-08-21 (see above).** Outcome: add a
  *dereification* axis (Lutz's own primary axis, and scoreable from text) AND
  a separate self/subject-object axis (D-self); hold *clarity/luminosity* as a
  candidate now supported from two independent directions (Lutz's theory + the
  luminosity factor found in the MPE-92M reanalysis); demote *Startup
  Modality* from dimension to metadata.
- ~~The crosswalk was built from KB notes about Lutz 2015, not from a
  re-reading of it.~~ **Re-read and verified 2026-08-21** — every `[recall]`
  tag in the working draft checked against the primary source directly
  (dereification definition p.639, the disidentification passage p.640,
  aperture/clarity/stability/effort pp.641-642). All confirmed accurate; none
  required correction.
- See also `instance-papers/contemplative-neuroscience.md` — the 2025–26
  neural-side literature (Sacchet minimal-model radar plots; Berkovich-Ohana /
  Dor-Ziderman six-dim self-boundary scheme) is a *third and fourth* independent
  dimensional lineage. The convergence across four groups is CAT's strongest
  framing, but it also means CAT joins a crowded dimensional field and must be
  precise about what it uniquely adds (answer: measurement).
- ~~NEW, opened by this update: ... worth a clean primary-source pass on
  Ataria/Dor-Ziderman~~ **DONE, same session (2026-08-21).** Full-text read of
  Nave, Trautwein, Ataria, Dor-Ziderman, Schweitzer, Fulder & Berkovich-Ohana
  (2021), *Brain Sciences* 11:819 — own record at
  `instance-papers/papers/nave2021-self-boundary-dissolution/`. Three things
  worth carrying into CAT directly: (1) their own network analysis finds
  Agency (control vs. letting-go) and Attention (focus vs. wide/formless) —
  not "self"/"boundary" vocabulary — are the strongest, most expertise-
  correlated drivers of boundary dissolution, which should reweight D-self's
  rubric anchors toward letting-go/release language; (2) they cite Lutz's
  dereification directly and treat it as a *facilitating* mechanism for
  sustaining dissolution, not a definition of it — a third hypothesis for the
  D11/D-self relationship, alongside Lutz's species-of account and the
  MPE-92M "real but ordinary" finding; (3) an unasked-for result — tight
  body-scan focus (high D2 candidate) sometimes produced a MORE observer-
  distant, LESS embodied self, cutting against an assumption CAT should not
  make silently. Their own PCA also finds boundary dissolution collapses to
  roughly one dimension (58% variance, one component) — independent support
  for treating D-self as one axis — but their coding scheme never separated
  attentional-constraint language from self-structure language to begin
  with, so this cannot rule out CAT's own D1/D-self split finding two
  dimensions where they found one. Full derivation: `cat_lutz_crosswalk.md` §7.
  J Neurosci 44(26) 2024 (the MEG single-trial decoding follow-up from the
  same group) still not read — smaller priority now that the phenomenology
  paper is in, since it's a neural-decoding result, not a conceptual one.
