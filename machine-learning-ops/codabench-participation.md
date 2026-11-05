<!--kb
id: codabench-participation
labels: codabench, competitions, shared-tasks, api, semeval
triggers: codabench API; codabench token; download codabench dataset from script; codabench leaderboard API; read codabench forum; codabench submission limits; codalab vs codabench; competition terms multiple accounts; participating in a SemEval task on codabench
verified: 2026-11-02
review_by: 2027-02-02
confidence: verified
evidence: measured against the live platform 2026-11-02; API may change
-->

# Participating in a Codabench competition from a script

Status: active. Author: maria. Measured 2026-11-02 on codabench.org v1.35, competition 17510 (SemEval-2027
Task 3). Codabench is the successor of CodaLab Competitions. Source: https://github.com/codalab/codabench.
Docs: https://docs.codabench.org (thin for participants: one page).

## Auth

- `POST https://www.codabench.org/api/api-token-auth/` with `username`, `password` returns a DRF token. After
  that, send `Authorization: Token <token>` on API calls. A token alone is enough for everything below, except the forum.
- Keep the token in a gitignored file and check that a commit diff does not contain it
  (`git diff --cached | grep -c "<token>"` must be 0).

## Read endpoints that worked (token sent)

| what | endpoint | notes |
|---|---|---|
| competition, terms, pages (News), phases, docker image | `GET /api/competitions/<id>/` | with a token it adds `participant_status` (`approved` = registered). Phases carry `max_submissions_per_day`, `max_submissions_per_person` |
| profile check | `GET /api/my_profile/` | confirms which account a token belongs to |
| dataset / phase data download | `GET /datasets/download/<uuid>/` | the links on competition pages; works with the token |
| leaderboard of a phase | `GET /api/phases/<phase_id>/get_leaderboard/` | `submissions[].scores[]` with `task_id` and `column_key` (language etc.); `tasks[]` maps task ids to names |

## What a token cannot do

- **Forum** (`/forums/<forum_id>/`): plain Django views behind `LoginRequiredMixin`, with no API. The token does
  not open them, so reading needs a browser session login. Posting requires being an approved participant, and
  **e-mails every earlier poster in the thread** (`Thread.notify_all_posters_of_new_post`), so a forum post is
  also an e-mail to strangers.
- Organisers often run their real announcement channel elsewhere (a Google Group in 17510, members-only). The
  competition page's News section is the readable mirror. Diff it each session.

## Platform facts that matter to a participant

- The scoring program runs in the competition's `docker_image` (17510: `codalab/codalab-legacy:py37`, Python 3.7).
  Published scorer code may not run there as published. See
  `ai-evaluation/shared-task-scorers-need-known-answer-controls.md`.
- `make_programs_available: false` means the deployed scorer cannot be downloaded. Local == platform has to be
  measured with a dev-phase submission.
- Rules on teams, multiple accounts and AI use are per competition, in its `terms`. 17510 forbids multiple
  accounts, reverse-engineering the evaluation set and manual annotation of evaluation data. Codabench's own Code
  of Conduct (Contributor Covenant 2.1) says nothing about AI-written posts.
- A submission's description is visible to others. Leave it empty unless you mean to publish text.

## Submitting from a script (run end to end 2026-11-02)

The flow the web UI itself uses (`src/static/js/ours/client.js`, `riot/competitions/detail/submission_upload.tag`):

1. `POST /api/datasets/` JSON `{type: "submission", competition: <id>, name: <unique per user>,
   request_sassy_file_name: "x.zip", file_name: "x.zip", file_size: <bytes>}` -> 201 `{key, sassy_url}`.
   Names must be unique per user, so add a timestamp to each one.
2. `PUT <sassy_url>` with the zip bytes, `Content-Type: application/zip`, **without** the auth header (signed URL).
3. `PUT /api/datasets/completed/<key>/`.
4. `POST /api/submissions/` JSON `{data: <key>, phase: <phase_id>, tasks: [<task ids of the phase>]}` -> 201 with `id`.
   `description` is read-only through the API, so no text can be published by accident on this path.
5. Poll `GET /api/submissions/<id>/` until `status` is `Finished`/`Failed`. A phase with several tasks creates one
   child submission per task (consecutive ids after the parent). Each child carries its own `scores`.
6. `GET /api/submissions/<id>/get_details/` gives signed URLs: `scoring_result` is a zip with `scores.json`,
   `scores.txt`, `metadata` (exit code, elapsed time); `logs[]` holds stdout/stderr per step.

Pre-check: `GET /api/can_make_submission/<phase_id>/` -> `{can, reason}`. The server enforces the per-day and
per-person limits and refuses inactive phases.

**A child task can "Finish" with no score and exit 0.** In 17510 a degenerate 1b prediction produced
`scores.json` = `{}` and "No prediction file for this leaderboard task was found." for a zip that contained the file.
Read `scores.txt` of every child: `status` alone does not tell you the submission scored.

Published vs deployed scorer: in 17510 they agreed to 1e-10 on a dev submission, although the deployed one is
split into per-task programs and the published one cannot import in the competition's Python 3.7 image. Measure
this on one dev submission. Do not assume it either way.
