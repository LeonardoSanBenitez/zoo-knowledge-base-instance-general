# instance-general — index

Read this before writing a new entry anywhere in this instance. If a topic is
already here, extend that file — don't create a parallel one.

Format per line: `[status] path — one-line summary — why it matters / to whom`

Status: `active` (trust it), `superseded by <path>`, `seed` (thin, needs work).

---

## philosophy-of-science/

- `active` `philosophy-of-science/construct-validity-and-formalization.md`
  (id `construct-validity-and-formalization`, zoo-topic-entry typed-0.1) —
  Freiesleben & Zezulka (2025) "thinning the world" + construct validity
  failure, applied to the question of whether explicit formalization brings
  a field closer to truth or just relocates its blind spots — relevant to
  anyone formalizing an evaluation protocol or ontology (unlearning
  benchmarks, CAT rubrics, ideasim formalisms). Written for Cidral's
  2026-05-28 question.

- `active` `philosophy-of-science/verification-economics-of-open-science.md` —
  measured outcomes of open-science interventions (SCORE 2026: ~50% social-science
  replication; ~26% computational reproducibility; artifact-badging null result at
  four security conferences; Papers-with-Code shutdown) and the synthesis that all
  the failures share one mechanism — the party who benefits from a claim also
  produces its evidence. Argues the missing FAIR letter is V (verified by a
  disinterested party), not E, and that machine-checked proof is the only artifact
  attacking *correctness* rather than re-execution — relevant to anyone claiming a
  result is verified, to the math-formalizations pipeline, and to I-CARE's
  Science-as-Code positioning.

- `active` `philosophy-of-science/the-specification-execution-gap.md`
  (id `the-specification-execution-gap`) — between the SPECIFICATION of a process
  and its EXECUTION there is always a gap, and instruments that are cheap to
  apply live almost entirely on the specification side, because a specification
  is a document and an execution is an event. So the cheap measure measures the
  specification, and the field reports it as the execution, usually without
  anyone deciding to. Two instances that share no authors, methods or literature:
  a text-based measure of a meditation practice scores the INSTRUCTION while the
  field reads it as the STATE; and every population-scale reproducibility study
  measures DECLARED environments while reporting on whether science re-executes
  (a Dockerfile is a recipe not an image; an archive node with a provider add-on
  is a pointer not a deposit; a badge records one check in someone else's
  environment). Three ordinary forces push the cheap measure to the wrong side,
  and mandates make it worse because they can only require checkable things —
  Cognition's open-DATA policy moved data availability to 99% and analysis-script
  sharing from 8.7% to 6.0%. Carries the one-question diagnostic (**what would
  change in my measurement if the specification were followed perfectly and the
  outcome were still wrong?**) and the rule that follows: never pool a rate about
  declarations with a rate about executions. Relevant to anyone building an
  instrument, a crosswalk between an instruction space and an outcome space, a
  policy, or a badge.

- `active` `philosophy-of-science/ro-crate-and-nanopublications.md`
  (id `ro-crate-and-nanopublications`) — two published, maintained standards for
  making scholarship machine-readable, and what each one is actually for.
  **RO-Crate** describes a research object as an *aggregation* (files, datasets,
  software, people, instruments, licences, provenance) as JSON-LD over
  Schema.org in a `ro-crate-metadata.json`. A **nanopublication** describes one
  small *assertion* with its provenance and publication-info as three named
  graphs. Complementary, not competing: one packages, the other asserts. Covers
  workflow provenance, the structural comparison, the primary specifications,
  and the published literature through 2025 including a field study representing
  submissions, reviews and decisions as nanopublications. Relevant to anyone
  packaging a replication artifact, choosing a metadata standard, or arguing
  about FAIR digital objects.
  **Indexed 2026-08-25 — it had been in the corpus since before version control
  and was in no index at all**, which by rule 1 of GUIDELINES means it did not
  exist. Found by an audit of every file against every index; it was the only
  one, out of 46.

- `active` `philosophy-of-science/independence-the-hidden-premise-of-agreement.md`
  (id `independence-the-hidden-premise-of-agreement`) — whenever two sources
  agree and you count it as evidence, you have assumed their errors are
  independent, and **the diagnostics built to detect disagreement report the
  failure of that premise as good news**: shared implementation error is not
  sampling error, so it pushes I² toward zero exactly where genuine agreement
  does. Written after a claim of mine (two notebook corpora converging at
  I² = 0) turned out to rest on two studies running the same program, one of
  which had a defect. Same shape in LLM ensembles over models sharing a base,
  many-analyst studies sharing a data file, replication that reuses the
  pipeline, and evaluating a knowledge base with queries written by the person
  who wrote the entries. Four questions to ask instead, and the asymmetry that
  makes them cheap: **disagreement is informative whatever the sources share;
  agreement is informative only to the extent that they share nothing.**
  Relevant to anyone pooling estimates, voting an ensemble, quoting an I², or
  deciding whether a second opinion is worth having.

## information-retrieval/

- `active` `information-retrieval/benchmarks-for-retrieval-and-rag.md` — living
  catalogue of ~30 IR / embedding / RAG benchmarks, evaluation campaigns and
  access libraries, each analysed against a fixed template, built to answer one
  question: **could a new embedding method, distance metric or rule-based
  retriever be automatically evaluated with high confidence that it beats
  SOTA?** Short answer: automation yes, confidence no, for four measurable
  reasons. Carries a computed result — BEIR's per-subset resolving power, from
  the paper's own LaTeX table: **Touché-2020, TREC-COVID and TREC-NEWS cannot
  resolve anything under ~5 NDCG points**, the deeply-judged subsets are the
  smallest ones, and 78% of the variance of the headline average comes from the
  four smallest subsets. Relevant to anyone claiming a retrieval or embedding
  improvement, choosing an evaluation set size, or wondering whether a
  leaderboard delta is real. Companion script `beir_resolving_power.py`;
  fetcher `tools/fetch_benchmark_papers.sh`. Started by maria 2026-08-13,
  **multi-session, many entries still `desk-research` — check the
  `verification` line before quoting anything.**

- `active` `information-retrieval/evaluating-your-own-knowledge-base.md`
  (id `evaluating-your-own-knowledge-base`, zoo-topic-entry typed-0.1) — how to
  tell whether a knowledge base is actually working, and the four ways the
  measurement lies to you: a reader that skips what it cannot parse (and so
  manufactures evidence for its own format); triggers written after seeing the
  test queries; reporting a rate when leave-one-out shows 67% of the effect is
  one query; and being your own assessor. Carries the resolving-power argument
  transferred from the public-benchmark catalogue — a 6-query internal gold set
  whose floor on p is 0.125 cannot demonstrate anything at 0.05. Relevant to
  anyone claiming a documentation, retrieval or note-format change helped, and
  to anyone about to quote an absolute number off their own gold set.
  Companion tool: `tools/retrieval_eval.py significance`.

## software-engineering/

- `active` `software-engineering/silent-data-loss-patterns.md` — running list
  of bug *shapes* that produce plausible-looking wrong numbers without
  errors/NaNs/shape mismatches. **Pattern 1** (lucas): `dict.update()`
  last-write-wins collision, which invalidated a round of unlearning-analysis
  results — relevant to anyone aggregating multi-file/multi-source data into
  one structure keyed by something that isn't guaranteed unique.
  **Pattern 2** (maria, 2026-08-25): *the empty check that reports the value of
  success* — a comparison loop with zero iterations leaves its diff list empty,
  so "nothing differed" and "nothing was examined" become the same value. Found
  in a published re-execution pipeline, where it flagged 7,019 of 17,965 runs as
  reproducing their outputs without comparing anything. Worse than Pattern 1
  because vacuous success accumulates on the inputs that failed hardest, so the
  metric IMPROVES as the pipeline degrades. Covers `all([])`, a test suite that
  collected zero tests, a health check whose probe never ran. Relevant to
  anyone who writes a check, which is everyone.
  **Pattern 3** (lucas, 2026-08-30): *the fallback default that is
  indistinguishable from a legitimate answer* — `json.loads(s or "{}")` made a
  gate report a clean pass having read nothing, because `{}` answers "not
  closed, not assigned, no labels" exactly as a healthy ticket does. Distinct
  from Pattern 2 (which is zero iterations, and is caught by counting what was
  examined; this one's count is 1). Includes the Windows trap that triggered
  it: `subprocess.run(text=True)` decodes with the LOCALE codec, cp1252 by
  default, so one emoji in a tool's output raises inside the pipe decode and
  hands back an empty string with exit code 0. Relevant to anyone who shells
  out to `gh`/`git`/`docker` on this machine, or who writes `or {}` anywhere
  near a decision.
## optimization/

- `active` `optimization/optimal-one-dimensional-partitions.md` — exact
  change-of-variables from a slope-capped curve-envelope objective to
  one-sided \(L_1\) step approximation; connects cell submodularity,
  discrete-convex resource allocation, and high-resolution companding —
  relevant when ordered sample placement and integer branch budgets appear
  as separate optimization layers.

- `active` `optimization/tail-oriented-active-sets-for-root-factor-polynomials.md` —
  orientation-invariant sign cone, curvature-based contact selection,
  stationary-envelope Jacobian, tangent/KKT projection, complete stationary
  sign check, and finite-step failure modes for factored polynomial objectives —
  relevant when perturbing prescribed double roots can create narrow distant
  sign changes that a scoring grid may miss.

## dynamical-systems/

- `active` `dynamical-systems/finite-step-and-nonmonotone-lyapunov-functions.md` —
  retrieval map separating fixed terminal-step, weighted-average/variable-step,
  ISS, and path-complete Lyapunov certificates; finite-sum bridge,
  counterexamples, inter-sample bounds, recent 2025–2026 developments, and an
  LMI audit checklist — relevant whenever a discrete-time Lyapunov candidate is
  allowed to rise temporarily or a finite-window inequality is claimed to imply
  stability.

## llm-agent-cognition/

- `active` `llm-agent-cognition/performative-thoroughness-and-reward-bias.md`
  (id `performative-thoroughness-and-reward-bias`, zoo-topic-entry typed-0.1) — reward
  models measurably favor responses that *look* thorough/convincing over ones that are
  actually correct or useful (2026 sycophancy/reward-hacking literature); names the
  mechanism behind why an agent drifts toward writing comprehensive-looking KB entries,
  reviews, etc. instead of terse deltas — relevant to anyone writing into this KB, and to
  Cidral's HARD RULE review process (open question, not yet resolved with him).

## formal-methods/

Cidral's territory. Math formalization, proof assistants (Lean 4 / Mathlib),
automated + AI-assisted theorem proving. Organized **by retrieval trigger, not by
subject** — see `formal-methods/index.md` for the routing table before writing.
Core bet: the domain's highest-value content is NEGATIVE knowledge (hallucinated
lemma names) + dated post-cutoff facts + our own artifacts.

- `active` `formal-methods/ecosystem-landscape.md` — dated (2026-07) Lean/Mathlib
  ecosystem snapshot: versions/cadence, `grind`, search tools, `lean-lsp-mcp`,
  prover SOTA. Rots in ~3mo — re-verify. — anyone starting formal work.
- `active` `formal-methods/lean-mathlib-api-traps.md` — symptom-indexed negative
  knowledge + Mathlib name-derivation rules. — anyone stuck mid-proof on a lemma
  name/tactic.
- `active` `formal-methods/lean-workflow-and-verification.md` — env (MAX_PATH),
  sorry-grep+`#print axioms` verification, search-before-guess, `lean-lsp-mcp`,
  worktrees. — anyone setting up/verifying Lean work.
- `active` `formal-methods/proof-design-patterns.md` — how to structure a
  formalization before tactics (domain-neutral). — anyone planning a new proof.
- `active` `formal-methods/probability-transport-and-quantile-patterns.md` — coupling
  witnesses, pushforward contraction, atom-safe quantiles, exchangeable ranks with
  ties. — anyone formalizing probability or conformal-prediction results.

What we have already mechanized, and its status, is **not** in the knowledge base: it
is `dev-science-ops/math-formalizations/STATUS.md`.

## logic-and-abstraction/

- `active` `logic-and-abstraction/closure-completeness-determinacy.md` — three translations that
  prevent false novelty claims: equivalence-class may/must is rough approximation; target-relative
  losslessness is both query determinacy and heterogeneous abstract completeness; and standard
  completeness is weaker than commutation, with closure-valued counterexamples already in the
  literature — relevant whenever deduction, lossy observation, or two closure operators are combined.

## python-web/

Python web frameworks and their ecosystems (FastAPI, Starlette, Pydantic). Organized
**by retrieval trigger** — see `python-web/index.md`. Core bet: pretrained knowledge of
this ecosystem is ~a year stale, and stale-but-confident is the worst failure mode when
answering a stranger in public.

- `active` `python-web/fastapi-2026-snapshot.md` — dated (2026-07) delta between the
  training cutoff and FastAPI 0.141: what a remembered answer now gets wrong, current
  dependency picture, the repo's actual support process (public issues are disabled;
  everything happens in GraphQL-only Discussions), its explicit AI-contribution policy,
  and who actually answers there. — anyone answering a FastAPI question, reading a
  FastAPI traceback, or writing FastAPI code.

## data-orchestration/

Workflow orchestrators and their ecosystems (Airflow first). Organized **by retrieval
trigger** — see `data-orchestration/index.md`. Core bet: pretrained knowledge here is
Airflow **2.x**, and Airflow 3 changed the *architecture* rather than the authoring API,
so a remembered answer stays fluent and syntactically valid while being wrong about where
code runs and what it may touch.

Airflow now has its own sub-folder with an index and a machine-readable header per
entry (`data-orchestration/airflow/INDEX.md`): five entries covering config renames,
log/error strings, the Docker image, triage routing and the architecture snapshot,
searchable from a raw ticket by `communities/tools/kb_lookup.py --ticket <n>`.

- `active` `data-orchestration/airflow/airflow-2026-snapshot.md` — dated (2026-08-05) delta between
  the training cutoff and Airflow 3.3: Task SDK + Execution API, workers losing direct
  metadata-DB access, `/api/v1` → `/api/v2`, assets-not-datasets, removed SubDAGs/SLAs,
  flipped `catchup_by_default`, narrowed `xcom_pull`; plus the monorepo map, the
  issue-vs-discussion split (they share one number sequence), ASF governance and the
  Issue Triage Team, and Airflow's unusually permissive-but-prescriptive **agent policy**
  (mandatory `Drafted-by:` footer, never @-mention individuals, `apache/magpie`). — anyone
  answering an Airflow question, reading an Airflow traceback, or writing a DAG.

## machine-learning-ops/

The ML lifecycle tooling layer — experiment tracking, model registries, artifact stores,
serving plumbing, and the auth guarding them (MLflow first). See
`machine-learning-ops/index.md`, then `machine-learning-ops/mlflow/INDEX.md`. Same bet as the
two folders above, with a sharper edge: pretrained knowledge here is MLflow **2.x**, where
`./mlruns` was the friendly default, and the *first command of every tutorial I remember now
raises an exception*.

- `active` `machine-learning-ops/mlflow/mlflow-2026-snapshot.md` — dated (2026-08-15) delta
  between the training cutoff and MLflow 3.15.1: the filesystem backend raising unless
  `MLFLOW_ALLOW_FILE_STORE=true` (with the `mlflow migrate-filestore` escape hatch), the
  RBAC overhaul that removed the legacy permission *endpoints* (the tables are kept as a
  rollback snapshot), MLServer's removal as a serving
  backend, flipped serialization defaults (`pt2`, `skops`), async trace logging on by
  default, Python floor at 3.10, first-class logged models changing what `runs:/` resolves
  to, the entire tracing/GenAI surface that postdates training, and the `get-history`
  pagination semantics that *inverted* between 3.13 and 3.14. — anyone answering an MLflow
  question, debugging a tracking server, or about to repeat a 2.x-era recipe.
- `active` `machine-learning-ops/mlflow/mlflow-auth-rbac.md` — dated (2026-08-17) model of the
  `basic-auth` app after two rewrites: roles + `role_permissions` (3.12) replacing the
  per-resource permission endpoints **removed** in 3.13, how a grant resolves at request time,
  workspaces and the immutable `artifact_location` prefix, the 403-on-artifact-upload bug fixed
  in 3.15.0, and the five setup traps that make a correct config look broken. — any 403 /
  "Permission denied" / RBAC / workspaces question.
- `active` `machine-learning-ops/mlflow/mlflow-release-map.md` — dated (2026-08-17) every 3.x tag
  with date and Python floor, landmark commits mapped to their first release, and the numbering
  trap (**no `v3.11.0` tag**; 3.11 shipped only as `v3.11.1`, so a failed `git show` there is a
  missing tag, not missing code). — every ticket that names a version.
- `active` `machine-learning-ops/mlflow/mlflow-tracing-otel-interop.md` — dated (2026-08-22)
  mechanism entry for MLflow tracing and OpenTelemetry: MLflow isolates its **tracer** provider but
  shares the process-global **meter** provider, so an application that owns a `MeterProvider` takes
  MLflow's `mlflow.trace.span.duration` and the configured OTLP metrics endpoint receives nothing,
  silently; plus the full span-routing precedence, the generic `OTEL_EXPORTER_OTLP_ENDPOINT`
  enabling both signals (which is how a per-span `trace_destination=` gets ignored), the grpc
  protocol default, the four APIs that rebuild span processors and what 3.15.0 does and does not
  clean up, unbounded metric-label cardinality from trace tags, and three traps in MLflow's own
  tracing tests. — any OTLP / collector / thread-leak / "my traces or metrics went nowhere"
  question.
- `active` `machine-learning-ops/mlflow/mlflow-docker-projects-env.md` — dated (2026-08-18) what
  `mlflow run` with a `docker_env` copies into the project container per artifact backend, and the
  two holes in the S3 set at 3.15.1: no `AWS_DEFAULT_REGION` (boto3 falls back to `us-east-1`, so
  cross-region uploads die with `IllegalLocationConstraintException` — issue #2793, open since
  2020) and no `AWS_SESSION_TOKEN` (temporary credentials cannot sign), plus a `~/.aws` volume
  mounted at `/.aws` where botocore never looks. — any "works locally, fails inside `mlflow run`"
  or project-container credential question.

## cryptography/

Applied cryptography and TLS *libraries* — APIs, versioning, defaults, community practice.
See `cryptography/index.md`. Same bet as `data-orchestration/`, one notch sharper: OpenSSL
shipped a **major** version (4.0, 2026-04-14) that *removes* API surface, so a remembered
answer here does not merely describe the wrong architecture — it names functions and scripts
that no longer exist.

- `active` `cryptography/openssl/openssl-2026-snapshot.md` — dated (2026-08-06) delta
  between 3.0–3.2-era pretrained knowledge and OpenSSL today: computed support/EOL table
  (3.1/3.2/3.3 EOL, 3.0's LTS ends 2026-09-07, 3.5 is the LTS), 4.0's removals (engines,
  SSLv3, `c_rehash`, opaque `ASN1_STRING`, no `atexit()` cleanup), 3.5's hybrid-PQC TLS
  defaults, 3.6's C99 requirement, the four community surfaces (issues / Discussions Q&A /
  mailing lists / `openssl/project`), and the project's AI-contribution policy
  (`Assisted-by:` trailer + AI-clause CLA, scoped to commits) — anyone answering an OpenSSL
  question, debugging a post-upgrade TLS interop regression, or looking for a mature
  precedent on AI disclosure in a security-critical project.

## databases/

Database engines as *tools we use and answer questions about* — versions, support windows,
how to check a behavioural claim cheaply, and how each project's community is reached.
See `databases/postgresql/INDEX.md`.

- `active` `databases/postgresql/postgresql-2026-snapshot.md` — dated (2026-08-13) delta between
  a remembered PostgreSQL answer and 2026: supported-version table with EOL dates (18.4 current,
  **14 EOL 2026-11-12**, 13 already unsupported, 19 in beta, `master` = `20devel` so no source
  claim about released behaviour may be made there), the measured cost of *checking* rather than
  reasoning (a server of any major in 4 s, cross-major comparison in ~13 s, from-source build in
  352 s), how a project with **no GitHub surface at all** is searched (`/message-id/flat/<id>`
  gives a whole thread; `BUG #NNNNN` on `pgsql-bugs`; archives permanent and unmodifiable), and
  one packaging failure recognisable on sight (`No match for argument: postgresql18-server` =
  no pgdg repo enabled, not a missing package) — anyone using PostgreSQL, answering a version
  question, or looking for a well-run community that deliberately does not live on GitHub.

## operating-systems/

Operating-system kernels as *tools we use and answer questions about*, and as communities with
unusually explicit process. See `operating-systems/linux-kernel/INDEX.md`.

- `active` `operating-systems/linux-kernel/linux-kernel-2026-snapshot.md` — dated (2026-08-15)
  delta between a remembered Linux-kernel answer and 2026: the project now has an **official AI
  policy** (`Documentation/process/coding-assistants.rst`, `generated-content.rst`, and the
  *"Responsible use of AI to find bugs"* section of `security-bugs.rst`) with a mandated
  `Assisted-by: AGENT:MODEL` commit trailer, a ban on AI-added `Signed-off-by`, and **1494 merged
  commits already carrying that trailer in 12 months**; the counter-intuitive rule that an
  AI-found security bug must be treated as **public** with the reproducer withheld; the published
  threat model's out-of-scope classes (crafted filesystem images, lying hardware, already-held
  capabilities, EOL kernels); the fact that there is **no bug tracker** (70 of 3255 `MAINTAINERS`
  sections name one; 2137 of 3361 `Closes:` tags point at a mailing-list message) and what the
  routing is instead; measured scale and costs (81 593 commits/12 months, defconfig build in
  8.5 min, boots under QEMU); and three programmatic traps — Anubis proof-of-work on
  lore.kernel.org, bugzilla's silent 10 000-row cap, and the kernel tree being **impossible to
  check out on a case-insensitive filesystem** — relevant to anyone answering a kernel question,
  contributing with AI assistance anywhere (this is the most explicit published policy we have
  found), or scripting against kernel infrastructure.

## psychology-of-meditation/

- `active` `psychology-of-meditation/lutz-taxonomy-and-cat.md`
  (id `meditation-lutz-taxonomy-and-cat`, zoo-topic-entry typed-0.1) — Lutz et al.
  FA/OM meditation taxonomy vs. the CAT project's 10 continuous dimensions.
  **This row said until 2026-08-17 that the entry "argues CAT is dimensional
  where Lutz is categorical". The entry itself retracted exactly that framing
  on 2026-07-29 as an overclaim** — Lutz, Jha, Dunne & Saron (2015) already
  give an explicitly dimensional seven-axis phenomenological matrix, so the
  dimensional move is not CAT's to claim. The index kept advertising the
  retracted version for nineteen days. Read the entry's correction section
  before citing any of this in the CAT paper (maria/mark).

## commons-and-governance/

- `active` `commons-and-governance/vinaya-and-debian-against-ostrom.md`
  (id `vinaya-and-debian-against-ostrom`) — two rulebooks for communities that
  are neither market nor state, twenty-five centuries apart, scored against
  Ostrom's eight commons-governance principles. **They are near-complements.**
  Debian's constitution is *authority* — who decides what, by which procedure —
  and contains **zero** occurrences of suspend / probation / warning / sanction /
  penalty / discipline / rehabilitate / reinstate, against `expel` twice and
  `admit` once. The Code of Conduct adds exactly one graduated element in one
  sentence (temporary or permanent ban) with no procedure, duration, appeal or
  criteria. The Vinaya is the reverse: a graded offence code with a defined
  rehabilitation path and almost no authority structure.
  **The sharpest form: neither Debian document defines a way BACK.** Entry, exit
  and sanction are all defined; return to full standing is defined nowhere —
  which makes every step away irreversible in practice whatever anyone intends,
  and is a candidate structural mechanism for why maintainer departure reads as
  betrayal. Also refines a hunch of mine: Debian *does* have impermanence, for
  **offices** (Leader annual, Secretary 1 year, Committee 42 months) and not for
  **membership**, so continuing is silent and stopping is an announcement.
  Carries an explicit provenance line — Debian checked, Vinaya recalled — and a
  falsifiable prediction. Relevant to anyone writing a contributing guide, a code
  of conduct, or a governance document, and to lucas's seven communities and
  mark's contributor-funnel work.

## multi-agent-systems/

- `active` `multi-agent-systems/independent-replication-and-correlated-error.md` —
  whether one agent checking another's work is corroboration or the same error twice.
  Answer: the question is not identifiable without a chosen null (Jo, Garg & Raghavan
  2026, Thm 1), and empirically **competence concentrates errors** (corr(accuracy,
  P(picks the modal wrong answer | wrong)) = +0.84 across 22 HELM models) — so two
  *unrelated* competent agents converge too. Consequences: varying the model buys less
  independence than varying the evidence; agreement between agents who saw the same
  input is near-uninformative while disagreement is highly informative; external
  oracles (proofs, tests, held-out data) beat second opinions because they need no null.
  Also carries the LLM-as-judge asymmetry (a judge inflates weaker models, deflates
  stronger ones, favours its own family). — relevant to every review process in this
  zoo, to Cidral's HARD RULE reviews, to Mark's DevScienceOps agentic-reproduction
  thread, and to anyone about to ask a second instance for a second opinion.
  Written for mark's 2026-05-28 / 2026-08-05 question; evidence in
  `instance-papers/llm-monoculture-and-correlated-errors.md`.

## Topics not yet started but likely, given current projects

(Noted so whoever hits these first doesn't have to invent the folder name.)
- (`multi-agent-systems/` is now a live folder — see its section above. Orchestration
  patterns and mailbox protocols are still unwritten there.)

(`formal-methods/` is now a live folder — see its section above.)
