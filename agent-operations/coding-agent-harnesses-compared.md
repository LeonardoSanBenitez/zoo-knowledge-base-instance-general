# Coding-agent harnesses compared: Claude Code, Codex, Antigravity, Mistral Vibe, Claude Science, and others

```toml
schema  = "zoo-topic-entry/typed/0.1"
id      = "coding-agent-harnesses-compared"
kind    = "version-fact"
status  = "active"
areas   = ["agent-operations"]
authors = ["maria"]
created = 2026-11-12
updated = 2026-11-12
verified = 2026-11-12
verify_by = 2027-01-12
confidence = "reported"  # one row measured here: Codex Windows sandbox (2.2)
triggers = [
  "what is the difference between claude code and codex",
  "claude code vs codex vs antigravity vs mistral vibe",
  "how does claude science differ from claude code",
  "which coding agent has a real sandbox on windows",
  "does the codex sandbox work on windows 10",
  "does claude code sandbox commands on native windows",
  "which agent harness can run with local models only",
  "is an auto-approve classifier a sandbox",
  "can a command allowlist be bypassed",
  "which agents read AGENTS.md",
  "persistent python kernel in an agent",
  "keep a python process alive between agent tool calls",
  "mistral vibe permission bypass cve",
  "why do environment variables not persist between agent shell calls",
  "how do agents undo file changes checkpoints shadow git",
  "agent client protocol acp app-server agent sdk",
  "gemini cli replaced by antigravity cli",
]
```

**Scope.** This entry covers the engineering mechanisms only: how code runs, what isolates it, what decides
whether it may run, what persists, and how you extend or embed each harness. It leaves out benchmark
quality and marketing claims.

**Method.** Each statement comes from the vendor's own documentation or repository, read raw on 2026-11-12
(`.md` twins or `llms.txt` indexes fetched with curl, plus GitHub API metadata). Press coverage and
fetch-and-summarise tools were used only to find those pages. The fetch commands are in "Sources" below.
`confidence = "reported"` means a vendor states it and nobody here re-measured it. The few facts measured on
this host are marked **[verified here]**.

**Shelf life is short.** These products ship weekly, and Codex CLI cut a release the day before this was
written. Re-check the claim you need before you rely on it (see "Re-verify").

Versions at time of reading:

| product | version | source / licence | language |
|---|---|---|---|
| Claude Code | 2.1.322 **[verified here]** | proprietary ("All rights reserved", Commercial ToS); the sandbox library `anthropics/sandbox-runtime` is Apache-2.0 | TypeScript (npm), native binary |
| OpenAI Codex CLI | rust-v0.167.2 (2026-11-11) | Apache-2.0, `openai/codex` | Rust |
| Google Antigravity | App v2.5+, CLI `agy` 1.2-1.4.x | licence not stated in the docs read | n/a (SDK is Python, `google-antigravity`) |
| Mistral Vibe | v3.1.2 (2026-11-10) | Apache-2.0, `mistralai/mistral-vibe`, **does not accept PRs** | Python 3.12+ (a `vibe/cli-rust/` tree exists) |
| Claude Science | beta, 0.1.7x builds | proprietary | n/a |
| Gemini CLI | v0.68.0 (2026-11-10), still active | Apache-2.0 | TypeScript |
| OpenCode | v1.19.5 (2026-10-28), repo now `anomalyco/opencode` | MIT | TypeScript |
| Aider | v0.86.0 (2025-08-09), last push 2026-05 | Apache-2.0 | Python |

---

## 1. The shared skeleton, and where the differences actually live

Every one of these is the same machine: **a model in a loop, a tool set, context management, and a policy
layer that decides whether a tool call may run.** Claude Code's docs name this layer the "agentic harness".
Model quality aside, all real differences sit on eight axes:

1. **Execution model.** What state survives between two tool calls.
2. **Isolation.** What the OS enforces: filesystem, network, per platform.
3. **Approval policy.** Who decides when isolation is crossed: user, rules, or a classifier.
4. **Instruction and config discovery.** Which files are read, and whether repo-supplied config is trusted.
5. **Extension.** MCP, skills, hooks, plugins, subagents.
6. **Persistence and undo.** Transcripts, checkpoints, provenance.
7. **Embedding.** Headless mode, SDK, wire protocol.
8. **Model binding.** Which models and providers, and whether local models work.

## 2. Comparison by axis

### 2.1 Execution model: what survives between calls

| harness | model | detail |
|---|---|---|
| Claude Code | **a new process per command** | `cd` carries over if it stays inside the project or added dirs; **env vars do not** (`export` is lost; use `CLAUDE_ENV_FILE` or a SessionStart hook). Shell aliases and functions are captured once at session start. Default timeout 2 min, max 10 min; `run_in_background` for long jobs; `Monitor` streams a background command's lines back as events. The no-persistence behaviour is measured on this host in `silent-corruption-in-the-command-path.md` **[verified here]**. |
| Codex | **resumable processes** | `features.unified_exec` is stable and on for every platform ("user opt-outs are ignored"). A process can stay alive and receive input through `write_stdin`, polled for up to 5 min by default (`background_terminal_max_timeout`). `shell_snapshot` caches the shell environment between commands. This is the closest any CLI comes to a live interpreter: `python -i` can be kept alive and fed. |
| Claude Science | **persistent Python/R kernel per session** | Variables stay in memory between cells. The kernel ends after ~30 min idle, on a package install that restarts the environment, or at session end. Shell commands (PowerShell on Windows) are separate. Each cell, its output and its environment are recorded in the session's Notebook. |
| Antigravity | per-command terminal, plus **sidecars** | Sidecars are background processes declared in `sidecar.json` under `~/.gemini/config/sidecars/`. Antigravity launches them and restarts them on crash; the only `builtin` is `schedule`. The App also renders and runs notebooks (`.ipynb`, nbformat v3/v4). |
| Mistral Vibe | per-command (`bash`, `git_bash`, `windows_shell` tools) | Also a "managed shell" implementation (`docs/managed-shell-tools.md`). |

### 2.2 Isolation: the OS-enforced boundary

| harness | macOS | Linux | Windows native | network |
|---|---|---|---|---|
| Claude Code | Seatbelt | bubblewrap + socat; optional seccomp filter (blocks Unix sockets) | **none: "On native Windows, Claude Code runs commands unsandboxed"**. Use WSL2. | Deny-by-default proxy; allowed domains **start empty**. **Off by default**, and it **covers shell commands only** (Bash, PowerShell, Monitor and their children): "Claude's file tools, MCP servers, and hooks run outside it". |
| Codex | Seatbelt | bubblewrap (first `bwrap` on PATH; falls back to a bundled helper that needs unprivileged user namespaces) | three implementations: **`mxc`** (Microsoft Execution Containers, Windows 11 24H2 build 26100.9278 / 25H2 build 26200.9278+), **`elevated`** (admin-approved setup, extra accounts and firewall rules), **`unelevated`** (weaker network isolation, no denied-read paths). **[verified here, Windows 10 19045, codex-cli 0.167.2, 2026-11-12]:** MXC refuses ('native MXC is unavailable on this executor'); `unelevated` with the `:workspace` profile allowed a write inside the workspace, BLOCKED a write to the user profile ('Zugriff verweigert'), allowed reading a home dotfile, and BLOCKED an HTTPS request (curl 000). The same probe unsandboxed: all four succeed | `workspace-write` plus `network_access` switch; the proxy has a domain allowlist. **App/connector traffic does not go through the sandbox proxy** (config reference). |
| Antigravity | Seatbelt (`sandbox-exec`, SBPL) | kernel namespaces (fs, pid, net) | **AppContainer** "inside a process security environment", needs **Windows 11 24H2 + the August 2026 update**. Windows 10 is named as "sandbox not available". | No network by default; domains allowed under `read_url` are added to the allowlist. |
| Claude Science | OS sandbox (mechanism not named) | bubblewrap ≥ 0.8.0 + socat, unprivileged user namespaces | supported on Windows 11 x64; mechanism not named. **With `--dangerously-no-sandbox`, code cells do not run at all on Windows.** | Local proxy; allows package managers, Featured-connector databases, and approved hosts. |
| Gemini CLI | Seatbelt with 4 profiles (`permissive-open` default … `restrictive-proxied`) | Docker / Podman / gVisor (`runsc`) / LXC container, or a custom `.gemini/sandbox.Dockerfile` | "Windows Native" mode: `icacls` sets **Low Mandatory Integrity Level** on paths | depends on profile or container |
| Mistral Vibe | **no local OS sandbox** | **none** | **none** | n/a. Only Vibe Code Web runs in "a managed sandbox". |
| OpenCode | none found in the permission docs read | — | — | — |
| Aider | none; it edits files and runs your lint/test commands as you | — | — | — |

The convergence is striking. On macOS everyone uses Seatbelt; on Linux nearly everyone uses
bubblewrap/namespaces. **Windows is where they diverge.** The newest Windows sandboxes need Windows 11 (Codex MXC, Antigravity
AppContainer). But **Codex's `unelevated` fallback works on Windows 10**, measured here: writes outside the
workspace and network are blocked, reads are not. [CORRECTED 2026-11-12: an earlier version of this paragraph said
'every serious Windows sandbox ... needs Windows 11', and section 4 said no vendor's sandbox supports Windows 10.
Both came from docs, and the first measurement contradicted them.] Gemini CLI's integrity-level approach also has a
mechanism that exists on older Windows (inference; untested).

### 2.3 Approval policy: the layer above the sandbox

All of them now have the same three tiers. Only the names differ:

| tier | Claude Code | Codex | Antigravity | Vibe | Claude Science |
|---|---|---|---|---|---|
| ask for everything | `manual` / `default` | `approval_policy=on-request` + `read-only` | Request Review | `ask` | permission cards |
| pattern rules | `permissions.allow/ask/deny`, e.g. `Bash(npm run *)` | Starlark `prefix_rule(...)` in `~/.codex/rules/*.rules`, with inline `match`/`not_match` tests | `command(git push)`, `command(regex:...)` | per-tool permissions | scope: once / conversation / project / global |
| **model classifier** | `auto`: built-in starting mode for interactive sessions since v2.1.283; the classifier runs client-side or, on newer versions, as a server-side review attached to the model request | `approvals_reviewer = "auto_review"` (a reviewer agent) | Auto: "safe, reversible" commands outside the sandbox | `smart-approve`: separate model call per tool call, defaults to a small Mistral model | auto mode; needs the sandbox ON ("with the sandbox off, auto mode approves nothing") |
| everything | `bypassPermissions` ("isolated containers and VMs only") | `danger-full-access` + `never` | Turbo | `auto-approve` / `--yolo` | `--dangerously-skip-approvals` |

**Finding 1 — a classifier is not a boundary, and neither is a string matcher.** Mistral's own docs say it
plainly: *"Smart approve is a classifier, not a sandbox. A call that it judges safe runs with the same access
as your user account."* The pattern layer is no stronger. Mistral advisory **MAI-2026-003** (2026-09-14,
severity High) fixed **six CVEs (CVE-2026-87983..87988) in Vibe's shell permission checks**: quoted absolute
paths, redirection targets, ANSI-C quoting, incomplete parsing, environment assignments, and allowlist/path
gaps. Each one let a crafted command run without the expected prompt; prompt-injected content could trigger
it. Several bugs went unfixed across many releases (1.3.4 → 2.25.4).

Every harness whose rules match command *strings* (`Bash(npm run *)`, `prefix_rule`, `command(regex:)`) is in
the same class. The difference is that Claude Code, Codex, Antigravity and Claude Science put an OS sandbox
**under** the rules, so a bypassed rule still hits a wall. Vibe has no such wall. Codex at least ships tests
inside the rule (`match` / `not_match`).

**Finding 2 — the sandbox changes what the approval layer means.** In Claude Code a command that runs inside
the sandbox is auto-approved with no prompt; prompts appear only for `excludedCommands` and unsandboxed
retries (`dangerouslyDisableSandbox`, which can be disabled with `allowUnsandboxedCommands: false`).
Antigravity's Default preset works the same way ("allowed in sandbox; ask outside"). Remove the sandbox and
the same preset means something else entirely.

### 2.4 Instruction files and trust of repository config

- **Claude Code.** `CLAUDE.md` hierarchy, plus auto-memory (`MEMORY.md`: first 200 lines or 25 KB loaded). It
  "can read" `AGENTS.md` in place of a CLAUDE.md. **A `-p` (headless) session shows no workspace-trust dialog
  and runs the project's `.claude/settings.json` hooks and `.mcp.json` servers "even in a folder you've never
  trusted"**; `--bare` skips that discovery and is "the recommended mode for scripted and SDK calls".
- **Codex.** `AGENTS.md` (or `AGENTS.override.md`): global `~/.codex`, then from the git root **down** to the
  cwd. Files are concatenated root-first, so nearer files win by appearing later, and **truncated at 32 KiB
  total** (`project_doc_max_bytes`). Non-managed hooks "must be reviewed and trusted before they run".
- **Antigravity.** `GEMINI.md` and `AGENTS.md`, global `~/.gemini/GEMINI.md`; workspace skills in
  `.agents/skills/`, MCP in `.agents/mcp_config.json` (key `serverUrl`, not Gemini CLI's `url`/`httpUrl`).
  `agy plugin import gemini` converts Gemini CLI extensions to plugins.
- **Vibe.** Trusted folders (`~/.vibe/trusted_folders.toml`). Untrusted `.vibe/`, `.agents/skills/` and
  `AGENTS.md` are **ignored**. Programmatic mode never prompts for trust, so it needs `--trust` explicitly.
  Note the asymmetry with Claude Code `-p` above.
- **Convergence.** `AGENTS.md` is read by Codex, Antigravity and Vibe, and optionally by Claude Code;
  `.agents/skills/` by Antigravity and Vibe. Skills follow one pattern everywhere: the description is in
  context, the body loads on use.

### 2.5 Extension

MCP is universal. Hooks exist in Claude Code (the richest set: PreToolUse can block, plus PermissionRequest,
Pre/PostCompact, SubagentStart/Stop, Stop, StopFailure, Worktree*, Task*…; handlers can be shell, HTTP, MCP
tool, prompt or subagent), Codex (adds `PreModelRequest`/`PostModelRequest`; matching hooks run
**concurrently**, so one cannot stop another from starting) and Antigravity. Subagents exist in all the
major ones. Claude Code adds agent teams, cross-session `SendMessage`, and a `Workflow` tool that scripts many
subagents. Antigravity adds `/teamwork` and `/swarm`. Codex subagents spawn only when asked or when
AGENTS.md/skills tell them to. Plugins and marketplaces exist in Claude Code and Antigravity.

### 2.6 Persistence, undo, provenance

| harness | transcript | undo of file edits | provenance of outputs |
|---|---|---|---|
| Claude Code | JSONL per session in `~/.claude/projects/`; resume/continue keep the session ID; `--fork-session`/`/branch` copy to a new ID | **checkpoints**: file snapshot before each edit, separate from git; skip symlinked/hard-linked files; nothing remote is undone | none beyond the transcript |
| Codex | "rollout files" on disk (`--ephemeral` skips them) | (not examined) | none |
| Gemini CLI | conversation saved with each checkpoint | **shadow git repo** in `~/.gemini/history/<project_hash>`; `/restore` reverts files, restores the conversation and re-proposes the tool call | none |
| Aider | — | **real git commits** in your repo, one per change | git history *is* the record |
| Antigravity | conversations, `/fork <project_id>` | review-before-apply diffs | "artifacts" (plans, walkthroughs, screenshots, browser recordings) are **communication**, not provenance |
| Claude Science | local DB under `~/.claude-science` | artifact versions on same-name save | **per artifact version: messages, reconstructed script, execution log, environment (packages + versions), review findings.** Complete *because the harness owns the only execution path*. Limits: the script is reconstructed ("if the Code tab and the log disagree, trust the log"); no input-file hashing is documented; non-artifact files are deleted hours after the session; Delete removes all versions. |

### 2.7 Embedding: headless mode, SDKs, protocols

- **Claude Code.** `claude -p` with `--output-format` json/stream-json. The **Agent SDK** (CLI, Python,
  TypeScript) "gives you the same tools, agent loop, and context management that power Claude Code".
- **Codex.** `codex exec`: progress goes to stderr, only the final message to stdout. **App-server**:
  JSON-RPC, can listen on `ws://`, and the TUI can attach remotely (`codex --remote`). `@openai/codex-sdk`
  (TypeScript, Node ≥ 18) starts and resumes threads. `codex mcp-server` has been **removed**.
- **Antigravity.** Headless CLI mode; `agy acp` speaks the **Agent Client Protocol** (JSON-RPC over
  stdin/stdout, launched by the editor: Zed, JetBrains…). Python SDK `google-antigravity` (`Agent`,
  `LocalAgentConfig`); a managed REST/gRPC "Antigravity Agent" exists in the Gemini API.
- **Vibe.** `vibe --prompt` (programmatic: denies anything needing approval unless `--auto-approve`). ACP
  binary (`vibe-acp.spec`) and an app-server.
- **Claude Science.** `claude-science serve` runs a background program on `127.0.0.1:8000` with a nonce
  login link; HTML previews come from a separate origin port; `--detached`, `status` (JSON), `logs --tail`.

ACP is becoming the editor↔agent protocol (Antigravity, Vibe, and Zed as client). It is a subprocess
JSON-RPC protocol, unrelated to MCP, which connects an agent to tools.

### 2.8 Model binding (matters for the arena's local-models-only rule)

| harness | models | local models |
|---|---|---|
| Claude Code | Claude (Anthropic, Bedrock, Agent Platform, Foundry) | not documented in the pages read |
| Codex | `model_provider` / `model_providers` (default `openai`) | **yes**: `--oss` with `oss_provider = "ollama" \| "lmstudio"` |
| Antigravity | Gemini 4 Carbon/Argon, Gemini 3.x Flash, Claude Sonnet/Opus 5.5, GPT-OSS-120b (some removed 2026-11-18) | **SDK only**: `LiteRTAgentConfig` (on-device `.litertlm`, e.g. Gemma 4 26B A4B, ≥ 24 GB recommended) or `LocalOpenAIAgentConfig` (Ollama, LM Studio, vLLM) |
| Vibe | Mistral API; custom `[[providers]]` with `api_base` (e.g. OpenRouter) | via an OpenAI-compatible `api_base` (inference from the provider schema) |
| OpenCode, Aider | any provider (Aider via LiteLLM) | yes |
| Claude Science | Claude models of your plan, plus tool models (BioNeMo etc.) and HTTP model servers you connect | scientific models only, not the reasoning model |

## 3. Per-product notes: what is distinctive, mechanically

- **Claude Code.** The widest tool surface (`Monitor`, `Workflow`, worktrees, Cron/scheduled tasks, LSP via
  plugins, `PowerShell` tool, deferred MCP tools loaded through `ToolSearch`). Compaction is automatic; output
  above ~30k chars goes to a file plus a 2k preview. A command that exits 1 counts as failure except for a
  fixed list (`grep`, `rg`, `find`, `diff`, `test`, `git diff`…). Sandbox is off by default (`/sandbox` or `sandbox.enabled`),
  wraps shell commands only (not the Read/Edit/Write tools, MCP servers or hooks), and is **absent on native
  Windows**.
- **Codex.** The only Rust harness, with resumable processes, Starlark exec-policy rules with built-in tests,
  an approval *reviewer* that is a separate role (`approvals_reviewer`), three Windows sandboxes, and a
  JSON-RPC app-server as the integration surface. `untrusted` approval policy retired.
- **Antigravity.** A product family (App = "agent manager", CLI `agy`, IDE, extensions for 6 IDEs, Python
  SDK, Remote Agents in Google-managed environments). It absorbs Gemini CLI's config (migration tool), though
  Gemini CLI itself is still released. Distinctive: browser-in-the-loop with recordings, sidecars, and
  multi-vendor models in one picker.
- **Mistral Vibe.** The smallest and the most open (Apache-2.0, Python, readable permission code in
  `vibe/core/tools/builtins/_shell_command_policy.py` and `_shell_permission_analysis.py`). That is why its
  failure mode is publicly documented: approval enforced by parsing shell syntax, with no OS boundary.
  "Agents" in Vibe are config overrides (prompt + tools + approval rules), not processes.
- **Claude Science.** Not a coding agent with a science skin. It is a different execution architecture: a
  captive kernel path, so its provenance is complete by construction. It adds conda/micromamba environments
  (pip **wheels only**, no git/URL/local installs into persistent environments, no apt/sudo), SSH/Slurm job
  submission (`sbatch`, 30-min default timeout, outputs > ~100 MB stay remote; **remote jobs run outside the
  sandbox**), Modal, and a reviewer that checks claims against the execution log without re-running.
  Requirements: macOS 13+, **Windows 11 x64**, Linux x64 glibc. Comparison with this zoo's own provenance
  practice: see "Relation to the zoo" below.
- **Gemini CLI.** The most sandbox *choices* (Seatbelt profiles, Docker, Podman, gVisor, LXC, Windows
  integrity levels), shadow-git checkpoints, and a TOML policy engine with priorities and tiers.
- **Aider.** The pre-agentic design: no tool-calling loop over a shell. A **repo map** (tree-sitter symbols
  ranked by a graph algorithm, fitted to `--map-tokens`, default 1k), edit formats, a git commit per change.
  The last release was 2025-08; treat it as maintained slowly.
- **OpenCode.** MIT, provider-agnostic. Built-in `build` (full access) and `plan` (read-only) agents plus a
  `general` subagent; permissions as `{action, resource, effect: allow|ask|deny}` rules.

## 4. Relation to the zoo

- This host is Windows 10 (build 19045) running Claude Code with `bypassPermissions`. **Claude Code has no
  native-Windows sandbox** (Antigravity's needs Windows 11 too, and says so). Every boundary in the zoo's Claude Code
  sessions comes from process (gates, tooling), not from the OS. Claude Science would not install either (Windows 11
  required). **Corrected 2026-11-12, measured:** Codex's `unelevated` sandbox DOES work on this Windows 10 host. It
  blocks writes outside the workspace and network, and leaves reads open (probe in section 2.2). So an OS-level write
  boundary is available on this machine today, though not through Claude Code.
- The engineering lesson from Claude Science applies to us without adopting it: **provenance is complete
  only where the harness owns the only execution path.** `dev-science-ops/paper-retrospective-reproducibility`
  enforces at the *claim* (no receipt from `tools/measured_run.py`, no execution claim) and is stronger on
  input identity (SHA-256 before the run, plan hash bound before execution, write-once `SEAL.json`). Claude
  Science enforces at *execution* and records everything, but hashes nothing documented. These are
  complementary, not competing.
- The Vibe CVEs are a caution for any guard we write that inspects command strings. Prefer guards that check
  artefacts and state (what our gating and state-machine tools do) over guards that parse shell.

## 5. Not established (do not quote as fact)

- Whether Claude Science is built on the Claude Agent SDK. Its Linux sandbox uses the same components as
  Claude Code's (bubblewrap + socat), which suggests shared code but does not prove it.
- Antigravity's licence and implementation language; whether any Antigravity source is public.
- Codex's undo/checkpoint mechanism (not examined).
- OpenCode's isolation beyond its permission rules; only the permissions page was read.
- Whether any of the classifiers (Claude auto, Codex auto_review, Antigravity Auto, Vibe smart-approve) has a
  published false-negative rate. None was found in the pages read.
- Whether Gemini CLI's integrity-level sandbox works on Windows 10 (the mechanism exists there; the vendor
  states no version).

## Re-verify

Each vendor publishes machine-readable docs. Fetch them raw; never through a summariser.

```sh
curl -sL https://code.claude.com/docs/llms.txt                         # Claude Code index; pages: /docs/en/<slug>.md
curl -sL https://claude.com/docs/llms.txt | grep claude-science        # Claude Science pages: /docs/claude-science/<slug>.md
curl -sL https://developers.openai.com/codex/llms.txt                  # Codex index -> learn.chatgpt.com/docs/<slug>.md
curl -sL https://antigravity.google/llms.txt                           # Antigravity; pages: /docs/<slug>.md
curl -sL https://docs.mistral.ai/llms.txt | grep -i vibe               # Vibe; pages: /vibe/code/<slug>.md
gh api repos/<owner>/<repo>/releases/latest --jq '.tag_name,.published_at'   # versions
claude --version
```

## Sources (all read 2026-11-12)

- Claude Code: `how-claude-code-works.md`, `sandboxing.md`, `tools-reference.md`, `permission-modes.md`,
  `hooks.md`, `headless.md` under https://code.claude.com/docs/en/ ; licence: https://github.com/anthropics/claude-code (LICENSE.md)
- Claude Science: `overview`, `core-concepts.md`, `tools-and-environments.md`, `artifacts.md`, `the-reviewer.md`,
  `remote-compute-clusters.md`, `command-line-settings.md`, `auto-mode.md`, `get-started.md` under https://claude.com/docs/claude-science/
- Codex: `sandboxing.md`, `windows/windows-sandbox.md`, `agent-configuration/rules.md`, `agent-configuration/agents-md.md`,
  `agent-configuration/subagents.md`, `hooks.md`, `non-interactive-mode.md`, `codex-sdk.md`, `app-server.md`,
  `sandboxing/auto-review.md`, `config-file/config-reference.md` under https://learn.chatgpt.com/docs/ ; https://github.com/openai/codex
- Antigravity: `overview.md`, `sandbox.md`, `models.md`, `artifacts.md`, `sidecars.md`, `jupyter-notebooks.md`,
  `cli/modes.md`, `cli/acp.md`, `cli/gcli-migration.md`, `sdk/overview.md`, `sdk/local-models.md` under https://antigravity.google/docs/
- Mistral Vibe: https://github.com/mistralai/mistral-vibe (README, tree); `vibe/code/safety-approvals-permissions.md`,
  `vibe/code/cli/configuration.md`, `vibe/code/choose-cli-vscode-web-sessions.md`,
  `resources/security-advisories/MAI-2026-003.md` under https://docs.mistral.ai/
- Gemini CLI: `docs/cli/sandbox.md`, `docs/cli/checkpointing.md`, `docs/reference/policy-engine.md` in https://github.com/google-gemini/gemini-cli
- Aider: README and https://aider.chat/docs/repomap.html ; OpenCode: README and https://opencode.ai/docs/permissions/
