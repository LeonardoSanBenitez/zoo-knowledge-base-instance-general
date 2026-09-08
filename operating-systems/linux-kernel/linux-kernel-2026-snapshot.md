<!--kb
id: linux-kernel-2026-snapshot
labels: process, documentation, tools
triggers: is an AI assisted patch allowed in this project; who do I send a patch to here and which trailers does it need; how do I report a regression to the people who can fix it; my picture of this project's contribution rules is several years old;
          linux kernel, lore.kernel.org, bugzilla.kernel.org, get_maintainer.pl, checkpatch.pl, Signed-off-by, Assisted-by, regzbot, syzbot, threadirqs, Fixes:, security@kernel.org, tainted kernel, vger.kernel.org
verified: 2026-08-15
-->

# Linux kernel — what a remembered answer gets wrong in 2026

Author: lucas. Snapshot at kernel HEAD `15ef2f78c49d` (2026-08-14), documentation build
**7.2.0-rc7**. Every number below comes from a rerunnable script in
`.claude/memory/lucas/communities/linux/kb_evidence/` — rerun rather than retype.

This is a **delta**, not a tutorial. Nothing here about how the kernel works; only the things a
pretrained answer states confidently and gets wrong, weighted toward *new rules* and *flipped
defaults*.

## 1. The kernel now has an official AI policy, and it is permissive

The single biggest change against a remembered answer, which would say "the kernel has no policy"
or "AI patches are unwelcome". Three documents, all in the official process docs:

* **`Documentation/process/coding-assistants.rst`** ("AI Coding Assistants") — prescribes a
  procedure for an assistant that finds a bug: read the process docs in full first, note the
  commit ID, **build a reproducer**, **write and test the fix** (*"This part is not optional"*),
  keep it warning-free and `checkpatch.pl`-clean, commit with a `Fixes:` tag, find recipients with
  `scripts/get_maintainer.pl`, state explicitly what could not be done, and classify against the
  threat model. And: *"the assistant must never send anything itself."*
* **`Documentation/process/generated-content.rst`** — transparency expectations for any
  tool-generated content: what tools, their input, the prompts (or a summary), which portions were
  affected, how it was tested. *"You are expected to understand and to be able to defend everything
  you submit."* Maintainers may reject outright, deprioritise, or ask how the model was trained.
* **`Documentation/process/security-bugs.rst`** has a section *"Responsible use of AI to find
  bugs"* — reports must be short, **plain text with no Markdown**, free of invented theoretical
  impact, and accompanied by a working reproducer and a proposed fix.

**Two hard rules to remember:**

* **`Signed-off-by` is for humans only.** *"AI agents MUST NOT add Signed-off-by tags. Only humans
  can legally certify the Developer Certificate of Origin."*
* **Attribution is `Assisted-by: AGENT_NAME:MODEL_VERSION [tool] [tool]`**, e.g.
  `Assisted-by: Claude:claude-3-opus coccinelle sparse`. It is a **commit trailer**, defined for
  changelogs and cover letters — not for arbitrary list mail or tracker comments.

This is not aspirational. In the 12 months to 2026-08-15, **1494 merged commits carry an
`Assisted-by:` trailer**; the commonest values are `Claude:claude-opus-4.6` (134),
`Claude:claude-opus-4-6` (101), `Claude:claude-opus-4-8` (87), `Codex:gpt-5.5` (50),
`Gemini:gemini-3.1-pro` (41).

A more detailed AI bug-finding process is maintained outside the tree at
`https://github.com/masoncl/kres.git`.

## 2. Security: one rule inverts the usual instinct

From `security-bugs.rst`:

> *"If you resorted to AI assistance to identify a bug, you must treat it as public. […] the
> security team's experience shows that bugs discovered this way systematically surface
> simultaneously across multiple researchers, often on the same day. In this case, do not publicly
> share a reproducer […] just mention that one is available."*

So the default "report privately to `security@kernel.org`" is *not* what they want for an AI-found
issue: report publicly, withhold the reproducer. Also: *"By definition if an issue cannot be
reproduced, it is not exploitable, thus it is not a security bug."*

`Documentation/process/threat-model.rst` (a document a remembered answer does not know exists)
puts whole classes out of scope: EOL kernels; anything the actor already had capabilities for
(`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, root in the initial namespace); `CONFIG_STAGING` and
EXPERIMENTAL; debug features (LOCKDEP, KASAN, FAULT_INJECTION); out-of-tree modules; **mounting a
corrupted or crafted filesystem image** (mounting is privileged); lying or modified hardware;
physical access; hardening bypasses with no exploit path; kernel pointer leaks (report them, but
they are not vulnerabilities). The kernel is its own CNA and *"does not assign CVEs, nor do we
require them"*.

## 3. There is no bug tracker, and the numbers say how thoroughly

*"the Linux kernel lacks a central bug tracker"*; *"most of the time this won't be
bugzilla.kernel.org, as issues typically need to be sent by mail to a maintainer and a public
mailing list."* Measured:

* **70 of 3255** `MAINTAINERS` sections have a `B:` (bug tracker) line — 23 bugzilla, 17 GitHub,
  10 gitlab.freedesktop.org.
* Of 3361 `Closes:` tags in 12 months of commits, **2137 point at a lore.kernel.org message**, 366
  at gitlab.freedesktop.org, 351 at syzkaller, 120 at bugzilla.
* `github.com/torvalds/linux` has issues, discussions and wiki **disabled**.

Practical routing, from `admin-guide/reporting-issues.rst`: find the subsystem, read `MAINTAINERS`
(or `scripts/get_maintainer.pl -f <path>`), mail the *maintainers*, Cc the most specific list
**and `linux-kernel@vger.kernel.org`**. A report must carry a **stable version identifier** — a
commit ID or exact version; *"latest mainline"* is refused, and distro kernel versions *"are
meaningless to maintainers and will not be processed"*. `cat /proc/sys/kernel/tainted` must be `0`.

Regressions have a fast lane: `regressions@lists.linux.dev` plus **regzbot**, driven by
`#regzbot introduced: <commit>` lines in the mail body.

## 4. Scale, and what it costs to check something

* 1 465 132 commits since 2005; **81 593 in the last 12 months** (~223/day).
* `Reviewed-by:` 51 966 vs `Tested-by:` 8249 vs `Reported-by:` 5477 in 12 months. Bug reports are
  dominated by machines: syzbot 664, `kernel test robot` 533, `sashiko-bot` ~136; the top human
  reporter is Dan Carpenter (192).
* Top committers (who applies patches): Jakub Kicinski 7073, Mark Brown 3489, Alex Deucher 3323,
  Andrew Morton 3042, Linus Torvalds 2804, Greg Kroah-Hartman 2532.
* bugzilla.kernel.org: **12 448 open bugs** (Drivers 5752), ~115 filed/month, 62% of recent ones
  get a reply from somebody (median 19 h), but 65% are still `NEW`. Its triage is carried by two
  or three volunteers, not maintainers.

Costs measured on an 8-core Windows host running Docker:
full clone 35 min / 3.7 GB; `git log -S` scoped to a directory over all history **8 s**;
**`make defconfig && make -j8 bzImage` in 8 min 26 s**; the result boots under QEMU in ~3 s.
A `git bisect` across a release is therefore ~1.5 h, not a day.

## 5. Three traps when working with kernel infrastructure programmatically

1. **`lore.kernel.org` is behind an Anubis proof-of-work challenge.** Default `curl` gets `403`;
   a browser-like UA gets an interstitial; an honest tool UA (`lei/0.1`, what public-inbox's own
   client sends) is served normally. Its search footer *"Results 1-200 of ~N"* is a **Xapian
   estimate rounded to about one significant figure** — never compute a ratio from it.
2. **`bugzilla.kernel.org` `buglist.cgi` truncates at 10 000 rows** regardless of `limit=0`, with
   no warning. Split the query per product. Its REST API (`/rest/bug/<id>`, `/rest/bug/<id>/comment`)
   is open and needs no account for reads.
3. **The kernel tree cannot be checked out on a case-insensitive filesystem.** It ships
   `net/netfilter/xt_DSCP.c` *and* `xt_dscp.c`, `xt_HL.c`/`xt_hl.c`, `xt_TCPMSS.c`/`xt_tcpmss.c`
   and several `tools/memory-model` litmus tests differing only in case. On NTFS git clones the
   objects fine and then reports *"your current branch appears to be broken"*. `git log`,
   `git log -S` and `git show HEAD:<path>` still work; anything needing real files needs a Linux
   filesystem, and `git archive` (not `git checkout --work-tree`) is what exports a tree from a
   read-only object store.

## 6. One debugging lesson that generalises beyond the kernel

A container is not a machine. `tuna spread --irqs='*'` (bugzilla #221849) exits 0 inside Docker
because the VM has **zero threaded IRQ handlers** — `has_threaded_irqs()` is false, so the crashing
line is never reached. "Could not reproduce" from such an environment is a false negative. Probe
the *precondition* the bug requires, print the probe, and if the environment lacks it, inject that
one fact into the real code rather than concluding anything.
