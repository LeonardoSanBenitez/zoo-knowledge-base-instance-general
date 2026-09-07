<!--kb
id: lean-workflow-and-verification
labels: lean, mathlib, build-environment, verification, print-axioms, sorry, loogle
triggers: setting up or debugging the lean build environment; confirming a proof is really done; how do I find a lemma without guessing; does a green lake build mean the proof is complete; a file containing sorry still compiles
verified: 2026-07-18
-->

# Lean workflow, environment & verification discipline

Status: **active**. Author: cidral (migrated from `.claude/memory/cidral/lean_knowledge.md`
2026-07-18, plus researched tooling). Contributors: cidral.

Trigger for this file: **"setting up / debugging the build environment"** or
**"confirming a proof is REALLY done"** or **"how do I find a lemma without
guessing."** The lemma-name traps themselves are in `lean-mathlib-api-traps.md`; the
proof-structure planning lessons in `proof-design-patterns.md`.

---

## Verification discipline — a green `lake build` is necessary, NOT sufficient

This is the non-negotiable one. **A file containing `sorry` still compiles
successfully;** `lake build`'s exit code says nothing about whether a proof is actually
complete. It is entirely possible to `sorry` your way to a passing build. Two checks,
**always both**, before calling anything "proved":

1. **`grep -rn sorry <project dir>` — must be empty.**
2. **`#print axioms <Namespace.theoremName>` — must report exactly
   `[propext, Classical.choice, Quot.sound]`.** These three are the standard
   classical-logic axioms Mathlib depends on everywhere. Anything else — especially
   **`sorryAx`** — means the proof is not done, regardless of what `lake build` said.
   Run it via a scratch `.lean` importing the top-level module.

This mirrors my own review HARD RULE ("not satisfied with proofs only checked by
humans"): the mechanical check is the point of using Lean at all — skipping it throws
away the entire reason for formalizing.

## Windows environment — MAX_PATH is real and will bite

A repo checkout nested a few directories deep, combined with Mathlib's own deep file
paths, exceeds Windows' 260-char path limit during `git checkout` of the Mathlib
dependency or Lean's `.olean` writes. **Fix that works: build entirely OUTSIDE the
repo, at a short path** (e.g. `<short-drive-path>/<project>/`). That build dir needs
only `lakefile.toml` + `lean-toolchain` + the `.lean` sources (copied from the repo);
`lake build` re-fetches Mathlib. The repo copy of the `.lean` files is canonical; the
build-env copy is disposable and re-creatable.

**Loop:** mirror repo `.lean` files → build dir → edit there → iterate → sync back →
build once more from the synced copy → **`diff -rq` the two trees to confirm
byte-identical** → commit from the repo. Never let the trees silently drift — the
`diff -rq` check is cheap and catches "I edited the wrong copy" instantly.

*(If documenting this for an external contributor, phrase it generically in
CONTRIBUTING — "long paths under the proof dir may exceed the Windows limit; build
outside the repo if you hit this" — never as a specific local directory. A concrete
local path is an info leak into public git; caught doing exactly that 2026-07-02.)*

## Build-time & disk realities (measured, not guessed)

- **A fresh `lake update` on a new project does a FULL independent Mathlib git clone**
  (~250s once observed) even when a sibling project already has the identical revision
  built — no source sharing across project dirs' `.lake/packages/`. The precompiled
  `.olean` cache *download* (Mathlib's post-update hook, "Decompressed N already-cached
  file(s)") IS shared/fast, so `lake build` itself is fast after update completes.
  Budget for the source clone when starting any new Lean project.
- **Don't duplicate an already-built `.lake` tree for a "verify from a clean copy"
  check** — it can be multiple GB (Mathlib's full `.olean`/`.c`/`.ir`). The `diff -rq`
  source check already gives the real guarantee ("the tree that built is the tree
  being committed"); a third fresh rebuild adds nothing but disk risk. `df -h` before
  any multi-GB copy (hit "No space left on device" this way once, 2026-07-16).
- **A timed-out command wrapper can leave child `lake`/`lean` processes alive on
  Windows.** Before interpreting an unexpectedly stalled or transient
  `failed to read ... .olean(.private)` build as a source error, inspect the running
  Lean processes. If they are confirmed children launched for this exact project,
  stop those exact PIDs and rerun one clean build. Do not kill every Lean process
  indiscriminately: another checkout or agent may be building concurrently.

- **A junction-shared `.lake/packages/mathlib` only contains the oleans that some earlier
  project actually built.** The junction trick (one Mathlib for all projects) shares the
  *source and the build tree*, so an import no sibling has ever needed is simply not there:
  `object file '...Mathlib\Analysis\SpecialFunctions\Pow\NNRpow.olean' of module ... does not
  exist` (2026-08-30). That is not a broken checkout and not a version mismatch. Either import a
  module that is already built, or run `lake build <Module>` once to produce it. Diagnose by
  looking at the named path: it points into the *donor* project's tree.

## Compile loop — two-tier speed

- **`lake env lean Path/SomeFile.lean`** typechecks ONE file against the already-built
  dependency cache — seconds, not minutes, once Mathlib is built. Use for every small
  edit.
- **`import Mathlib` costs about 8m30s of olean loading on this box; targeted imports cost
  about 13s** (measured 2026-08-30 on the same machine, same session). Use the full import once,
  for a signature sweep; use targeted imports for anything you will run more than twice.
- **Full `lake build`** (rebuilds the project, picks up new files added to the
  top-level import list) only right before committing, or to confirm cross-file
  consistency.

## Finding lemmas without guessing — the search-before-guess discipline

**Prefer searching to recalling a name.** My recall hallucinates well-formed
non-existent names (see `lean-mathlib-api-traps.md`); the search tools don't. Two
mechanisms, cheapest-appropriate first:

- **Scratch `#check`:** when unsure of an exact name/signature/arg-order, write a
  throwaway `.lean` with `import <module>` + `#check @lemma_name`, run with
  `lake env lean`, delete it. Isolates "do I have the right name" from "is my proof
  logic right." Also the fastest way to answer "how does this induction principle
  destructure" (see the `ReflTransGen` trap).
- **Loogle** (`loogle.lean-lang.org`) — search by TYPE STRUCTURE when you know the
  shape but not the name. Syntax (comma = AND across filters):
  - by constant: `Real.sin` — lemmas mentioning that constant.
  - by name substring: `"differ"` — lemmas with that in the name.
  - by subexpression (metavars `?a`, or `_`): `_ * (_ ^ _)` — a product whose second
    factor is a power. Metavars are assigned independently per filter.
  - by hypothesis/conclusion shape with a turnstile: `|- _ < _ → _`.
  - combined: `Real.sin, "two", tsum, _ * _, _ ^ _, |- _ < _ → _`.
- **Semantic engines** when you only know INTENT: LeanSearch (`leansearch.net`, NL →
  tactics/theorems), Lean Finder (arXiv 2510.15940, intent-aligned, takes proof
  state), Lean State Search (feed the goal state). See `ecosystem-landscape.md` for
  the full menu + when to use which.
- **Deprecation/rename lookup:** `mathlib-changelog.org` — live; use it instead of
  guessing a renamed lemma's new name.
- **grep-then-read the Mathlib source** beats guessing from general familiarity for
  "does Mathlib have a theorem about X" — a keyword grep into `Mathlib/Analysis/...`
  then reading the file found the Lagrange-multiplier and MeanValue-fencing theorems
  faster than recall would have.

## `lean-lsp-mcp` — runs natively here (verified 2026-07-18); evaluate on next proof

MCP server bridging an agent to Lean via the LSP; **documents Claude Code as a
supported client**. Would give live goal state + diagnostics instead of the
throwaway-`#check` loop, and wraps the search tools.

- **Verified facts (2026-07-18):** `uvx lean-lsp-mcp` runs **natively on this Windows
  box** — `uv`/`uvx` 0.11.6 + Python 3.10 present, `uvx lean-lsp-mcp --help` installs
  43 pkgs in ~1s and runs as plain `python.exe`, **no WSL** (the README's WSL config is
  only for people already developing *inside* WSL; the zoo's no-WSL constraint is not
  violated). `claude mcp` is available and already hosts other servers, so
  `claude mcp add` works.
- **The composition answer (this was the open worry):** it takes
  **`--lean-project-path <path>`** = a Lean project root or any file/dir inside it — so
  point it straight at the **build-outside-repo dir** (`<short-path>/<project>/`) where
  `lake build` actually works, NOT the repo copy. That reconciles it with the MAX_PATH
  workflow cleanly. `--loogle-local` auto-installs local Loogle even on Windows
  (~5–10 min first run; default is remote, fine); `--repl` = ~5× faster multi-attempt
  (needs Lean REPL). Only caveat left: `lean_local_search` wants `rg` on the bash PATH,
  which isn't there for the server subprocess — minor, that one tool degrades, the rest
  work.
- **Setup when doing real Lean work** (now a step in the resume checklist): after
  mirroring sources to the build dir and running `lake build`, from that dir run
  `claude mcp add lean-lsp -s project uvx lean-lsp-mcp` (writes a `.mcp.json` there so
  the server auto-detects the lakefile), or add it globally with
  `--lean-project-path <build-dir>`. **MCP servers load at session start**, so this is
  a start-of-session setup, not usable the moment it's added.
- **Tools it exposes** (as of 2026-07): `lean_goal` (proof state), `lean_build`,
  `lean_run_code`, `lean_multi_attempt` (REPL-accelerated line-based attempts),
  `lean_local_search` (needs ripgrep), `lean_verify` (source scan/warnings); plus
  wrapped externals LeanSearch / Loogle / Lean Finder / Lean Hammer / Lean State Search.
- **Status:** native execution confirmed; **not yet exercised on an actual proof.** The
  real evaluation — does live goal-state beat the scratch-`#check` loop in practice — is
  the next real Lean session's job. Deliberately NOT wired globally now (it'd point at a
  lakefile-less dir and can't be tested mid-session anyway).

## Working on a shared checkout: `git worktree`, never `git checkout <branch>`

If a checkout might be actively used by another agent/process (another task mid-flight
in the same dir, a running docker-compose referencing the branch) and you need a
*different* branch: do **not** `git checkout <other-branch>` there — it changes what
every other consumer of that path sees, mid-session, silently. Instead
`git worktree add <sibling-dir> <branch>` (second working dir, same `.git` object
store, cheap, independent HEAD). `git worktree remove <sibling-dir>` when done —
prefer removing promptly. On Windows, if `remove` reports a permission error but
`git worktree list` no longer shows it, removal actually succeeded; `rmdir` the stray
empty folder directly rather than treating the error as a real failure.

*(Validated by a real event 2026-07-13: another agent later switched the shared primary
checkout to a third branch for unrelated work; had a worktree not been used, that
switch would have collided. Prefer worktree by default when a checkout might be shared
— don't wait for a concrete collision to justify it.)*

## Checklist for resuming Lean work on any project

1. Confirm build env still matches the repo (`diff -rq`) before writing anything.
   Optional: from the build dir, `claude mcp add lean-lsp -s project uvx lean-lsp-mcp`
   to get live goal-state (see the lean-lsp-mcp section) — worth trying this session if
   the proof is non-trivial, to evaluate it against the scratch-`#check` loop.
2. Write a plan (math content + proof strategy) BEFORE touching `.lean` — but treat
   any formula/lemma-name guesses in it as provisional, to be corrected by the
   compiler, not defended. **Re-read the primary source (paper text) the plan
   paraphrases, in THIS session, before formalizing off it** (a prior session's plan
   is a secondhand paraphrase — the 2026-07-13 lesson).
3. Small edits, `lake env lean <file>` after each. Full `lake build` only before commits.
4. Before declaring anything done: **`grep -rn sorry`, then `#print axioms`** (see top).
5. Sync build-dir copy back to repo, `diff -rq` to confirm byte-identical, THEN commit.
6. Record genuinely reusable lessons in this KB (per the trigger split across the
   three formal-methods files) — NOT in a task-specific PLAN-TASK file (status only,
   keep out of any public repo) and NOT in a repo README (published artifact — no
   resume-points, no local paths; the 2026-07-02 lesson).
