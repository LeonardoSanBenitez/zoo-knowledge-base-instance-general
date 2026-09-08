<!--kb
id: mlflow-release-map
labels: area:server-infra, kind:version-fact, version:3.x
triggers: the reporter gave me a version and I need to know if it is before or after the fix; a tag is missing and I cannot tell if the feature was absent or just unreleased; when did this release come out;
          mlflow version, 3.9, 3.10, 3.11, 3.11.1, 3.12, 3.13, 3.14, 3.15, 3.15.1,
          "invalid object name", git tag --contains, requires-python, python 3.9, python 3.10,
          which release, fixed in, upgrade, release date, changelog, regression window
verified: 2026-08-17 by lucas, clone at 9355281ca, via
          .claude/memory/lucas/communities/mlflow/kb_evidence/collect_release_timeline.py
          (the raw output is quoted below, so it is checkable without that file)
-->

# MLflow 3.x release map — for locating a reporter's version

**Why.** Every ticket starts with a version, and the first move is almost always "when did this
change, and is this reporter before or after it". Two traps make that harder than it looks:
release numbering here is not contiguous, and an absent tag looks exactly like absent code.

**How to refresh.** `git -C <clone> for-each-ref --format='%(refname:short) %(creatordate:short)'
'refs/tags/v3.*'`, or re-run the script named in the header and diff its log.

## The tags, as of 2026-08-17 (clone `9355281ca`)

| release | date | `requires-python` |
|---|---|---|
| v3.0.0 | 2025-06-11 | >=3.9 |
| v3.1.0 (…v3.1.4) | 2025-06-11 … 2025-07-23 | >=3.9 |
| **v3.2.0** | 2025-08-05 | **>=3.10** (floor raised here) |
| v3.3.0 (…v3.3.2) | 2025-08-19 … 2025-08-27 | >=3.10 |
| v3.4.0 | 2025-09-17 | >=3.10 |
| v3.5.0, v3.5.1 | 2025-10-16, 2025-10-22 | >=3.10 |
| v3.6.0 | 2025-11-11 | >=3.10 |
| v3.7.0 | 2025-12-04 | >=3.10 |
| v3.8.0, v3.8.1 | 2025-12-21, 2025-12-26 | >=3.10 |
| v3.9.0 | 2026-01-29 | >=3.10 |
| v3.10.0, v3.10.1 | 2026-02-20, 2026-03-05 | >=3.10 |
| **v3.11.1** | 2026-04-07 | >=3.10 |
| v3.12.0 | 2026-05-04 | >=3.10 |
| v3.13.0 | 2026-05-29 | >=3.10 |
| v3.14.0 | 2026-06-17 | >=3.10 |
| v3.15.0 | 2026-07-31 | >=3.10 |
| v3.15.1 | 2026-08-03 | >=3.10 |

**The numbering trap: there is no `v3.11.0` tag.** The 3.11 line exists and shipped, but only as
`v3.11.1`. So `git show v3.11.0:some/file.py` fails with *"invalid object name"* — and that is a
statement about the tag, not about the code. Reading it as "the feature was not there yet" is a
mistake I made and had to correct: **before concluding anything from a failed `git show`, check
the tag exists** (`git tag | grep '^v3\.11'`). Same rule as any other empty result: it is not
evidence until the check could have succeeded.

Cadence for planning purposes: roughly a minor release every 3–5 weeks through 2026, patches
within days of a minor. A fix merged today is typically in a release within a month — which is
why "fixed on master" is rarely the useful answer, and "first released in vX.Y.Z" is.

## Landmarks — the first release containing each change we have verified

Only changes we actually established while working a ticket. Do not add guesses; add a row when a
ticket teaches it, with the commit.

| commit | merged | first release | what changed |
|---|---|---|---|
| `2e0adcfe2` (#20657) | 2026-02-10 | **v3.10.0** | workspaces (multi-tenant isolation) |
| `6624f695e` (#22721) | 2026-04-22 | **v3.12.0** | RBAC data model: roles + `role_permissions` |
| `1094ec1cf` (#22722) | 2026-04-23 | **v3.12.0** | RBAC REST API, permission resolution, client |
| `fc45c72e1` (#23337) | 2026-05-18 | **v3.13.0** | legacy per-resource permission endpoints **removed** |
| `ef409cab8` (#23379) | 2026-05-18 | **v3.13.0** | `default_permission` becomes a floor; workspace `USE` stops folding into resource lookups |
| `8edd5b032` (#22773) | 2026-04-25 | **v3.13.0** | filesystem backend (`./mlruns`) raises unless `MLFLOW_ALLOW_FILE_STORE` |
| `b567ee381` (#24214) | 2026-07-07 | **v3.15.0** | auth proxy resolves the experiment id under a `workspaces/` prefix (fixes 403 on artifact upload) |

Detail on the auth rows: `mlflow-auth-rbac.md`. Detail on the file-store row and the rest of the
2.x→3.x delta: `mlflow-2026-snapshot.md`.

## The method, in three commands

```bash
git -C <clone> log --format='%h %ad %s' --date=short -S '<exact code string>' -- <path>   # when
git -C <clone> tag --contains <sha> | grep -E '^v3\.[0-9]+\.[0-9]+$' | sort -V | head -1  # shipped where
git -C <clone> show <tag>:<path> | sed -n '<line>p'                                        # what it looked like
```

**A tag proves the code changed; it does not prove the user's behaviour changed.** Run the
reporter's scenario on both releases before saying "upgrade fixes it" — and when two releases
differ by a hundred commits, the way to attribute the change to *one* of them is to move that one
line in both directions (patch it into the old release, revert it in the new) rather than to
compare the releases and infer.
