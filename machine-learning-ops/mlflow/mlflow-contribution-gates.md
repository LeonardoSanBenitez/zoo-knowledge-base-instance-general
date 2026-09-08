<!--kb
id: mlflow-contribution-gates
labels: area:process, kind:gotcha, kind:policy, version:3.x
triggers: my pull request to this project was closed by a bot; will an outside contribution here even be looked at; which label does an issue need before a fix for it is accepted; what does this project's automation require of a first time contributor;
          ready label, auto-close, auto-close-pr.js, issue-warning, "may be automatically closed",
          "was automatically closed", "missing the ready label", "does not follow the PR template",
          PR template, pull_request_template, DCO, Signed-off-by, "sign your work",
          Co-Authored-By, CLAUDE.md, AGENTS.md, ISSUE_POLICY, ISSUE_TRIAGE, "I would like to work on this",
          assign this issue to me, mlflow contributing, first pull request mlflow
verified: 2026-08-23 by lucas. Bot behaviour read from `.github/workflows/auto-close-pr.js` at
          master `925d16f57`; the cutoff and the skip are quoted below with line numbers. The
          live demonstration is mlflow/mlflow#25280, closed by the bot at 2026-08-23T08:45.
-->

# Contributing to MLflow: the gates that decide whether a pull request survives

**Scope.** Not how to write MLflow code — how the project's automation and its issue conventions
decide whether an outside contribution is looked at at all. Written after a sweep of the tracker
for an issue worth a pull request, where these rules eliminated most candidates before any
technical judgement was involved.

## The `ready` label is the gate, with one large exception

`.github/workflows/auto-close-pr.js` closes a pull request from outside the team when the issue it
closes does not carry the `ready` label, is assigned to someone else, or already has a PR:

```
// Only enforces on issues/PRs created on or after 2026-03-10.
const CUTOFF_DATE = new Date("2026-03-10T00:00:00Z");   // line 14
if (new Date(issue.createdAt) < CUTOFF_DATE) { ... Skipping ... }   // line 171
```

So there are exactly two safe starting points for an outside pull request:

1. an issue **created before 2026-03-10**, which the policy skips entirely, or
2. an issue that already carries `ready` **and** has no assignee and no linked PR.

Seen live: #25280, a correct one-line chart fix by the reporter of the issue it closes, with the
PR template complete and the commit signed off, was closed 32 hours after opening with
*"This PR was automatically closed because #25269 is missing the `ready` label. Once a maintainer
triages the issue and applies the label, feel free to reopen this PR."* The branch must not be
force-pushed or deleted, or the reopen is lost.

A second bot enforces the PR **template**: a body missing the required headings is closed with the
missing sections listed. The headings are in `.github/pull_request_template.md`; the template's own
instruction is to keep every heading and tick only the boxes that apply.

## What that does to issue selection, in practice

Category 2 is thinner than it looks. On this tracker a `ready` issue that is worth fixing attracts
a comment of the form *"I'd like to work on this, could a maintainer assign it to me"* within days,
often from several people at once, and they then wait — sometimes for months — for the label or the
assignment. Four of the best recent bugs sampled on 2026-08-23 were all in that state, one with the
author reporting fix and tests already written locally.

Consequence for anyone planning a first contribution here: an **old, acknowledged, unclaimed** bug
is a far better target than a fresh one, and not because it is easier. It is the only category
where the bot is not a factor and nobody else is queued.

## What every commit must carry

Two published requirements, from different files, both enforced by bots:

* **DCO.** `CONTRIBUTING.md` "Sign your work" requires a `Signed-off-by: Name <email>` line on
  every commit. A missing one is reported by the same bot that checks the template.
* **Agent attribution.** The repo ships a `CLAUDE.md` (with `AGENTS.md` pointing at it) telling
  coding agents to add `Co-Authored-By: Claude <noreply@anthropic.com>` to commits they write.
  This is a project convention, not a courtesy; the project uses coding agents itself and has a
  `ui-review` bot of its own.

## The bar a *bug report* has to clear

`ISSUE_POLICY.md` accepts a bug report when it is a regression, documented behaviour failing, or an
exception raised by MLflow itself. The third clause is the one that bites: **a stack trace ending
in a third-party library is out of scope by their own policy**. Undocumented behaviour that never
worked fails all three clauses, however real the defect — worth checking before writing one up.

Their `ISSUE_TRIAGE.rst` describes *labelling* (process label, kubernetes-style priority, area
labels), all of which needs write access. What an outside contributor can supply is the content a
triager needs: a reproduction, a duplicate link, a version bisect, the missing author feedback.
