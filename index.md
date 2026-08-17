# instance-general — index

Read this before writing a new entry anywhere in this instance. If a topic is
already here, extend that file — don't create a parallel one.

Format per line: `[status] path — one-line summary — why it matters / to whom`

Status: `active` (trust it), `superseded by <path>`, `seed` (thin, needs work).

---

## philosophy-of-science/

- `active` `philosophy-of-science/construct-validity-and-formalization.md` —
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

## software-engineering/

- `active` `software-engineering/silent-data-loss-patterns.md` — running list
  of bug *shapes* that produce plausible-looking wrong numbers without
  errors/NaNs/shape mismatches (started with the `dict.update()`
  last-write-wins collision that invalidated a round of unlearning-analysis
  results) — relevant to anyone aggregating multi-file/multi-source data into
  one structure keyed by something that isn't guaranteed unique.
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

- `active` `llm-agent-cognition/performative-thoroughness-and-reward-bias.md` — reward
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

- `active` `psychology-of-meditation/lutz-taxonomy-and-cat.md` — Lutz et al.
  FA/OM meditation taxonomy vs. the CAT project's 10 continuous dimensions;
  argues CAT is dimensional where Lutz is categorical, with a falsifiable
  prediction for the CAT paper's Related Work section — relevant to the CAT
  paper (maria/mark) specifically.

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
