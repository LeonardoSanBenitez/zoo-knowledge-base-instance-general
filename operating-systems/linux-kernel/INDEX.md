<!--kb
id: linux-kernel-index
labels: meta
triggers:
verified: 2026-08-15
-->

# Linux kernel KB — index

Author: lucas. Snapshot point for every entry here: kernel HEAD `15ef2f78c49d` (2026-08-14),
documentation build **7.2.0-rc7**. Evidence scripts that produced the numbers:
`.claude/memory/lucas/communities/linux/kb_evidence/` — rerun them rather than retyping a figure.

**Retrieval contract.** Every entry carries a `<!--kb -->` header whose `triggers` are literal
strings a *reporter* would paste or say — an error message, a tool name, a trailer, a boot
parameter — not topic words chosen in hindsight. Lookup:
`python .claude/memory/lucas/communities/tools/kb_lookup.py --repo torvalds/linux --text <file>`
(`bugzilla.kernel.org` works as a key too; both map here).

`labels` reuse the kernel's own vocabulary where one exists; the kernel has no GitHub label set,
so they follow the `Documentation/` section names instead (`process`, `admin-guide`, `tools`).

| entry | what it is for |
|---|---|
| `linux-kernel-2026-snapshot.md` | The delta between a remembered kernel answer and 2026: the new official **AI policy** (`coding-assistants`, `generated-content`, and the AI section of `security-bugs`), the `Assisted-by:` trailer and the ban on AI-added `Signed-off-by`, the rule that an **AI-found security bug is treated as public** with the reproducer withheld, the published threat model's out-of-scope classes, the fact that there is no bug tracker and what the routing actually is, measured scale and build costs, and three traps in reading kernel infrastructure programmatically (Anubis on lore, the bugzilla 10 000-row cap, the case-insensitive-filesystem checkout failure). |

## Deliberately deferred, with reasons

* **How the kernel works** — scheduling, memory management, locking, filesystems. Pretraining
  supplies this well; writing it down is close to worthless per the KB's delta rule.
* **Per-subsystem maintainer handbooks** (netdev, tip, drm each have their own process). Large,
  and only worth capturing when a ticket touches one. Add on demand.
* **Community house rules** — the surfaces, who answers where, the disclosure block, the sweep
  order, the cost table. Those belong to the project, not to the technology, and live in
  `.claude/memory/lucas/communities/linux/CONTRIBUTING.md`. Pointer, not copy.
* **A feature delta per release (7.0, 7.1, 7.2).** The changelogs are in the clone and are
  searchable; nothing has needed a summary yet.

## Status

**Partially active.** We read the mailing lists and never write to them (decision 2026-08-15).
`bugzilla.kernel.org` is an authorized contribution surface, pending an account and API key, with
per-message approval.
