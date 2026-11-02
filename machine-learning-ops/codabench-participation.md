<!--kb
id: codabench-participation
labels: codabench, competitions, shared-tasks, api, semeval
triggers: codabench API; codabench token; download codabench dataset from script; codabench leaderboard API; read codabench forum; codabench submission limits; codalab vs codabench; competition terms multiple accounts; participating in a SemEval task on codabench
verified: 2026-11-02
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

## Not yet verified here

The scripted submission flow (create dataset -> upload -> complete -> `POST /api/submissions/`) is in
`src/apps/api/views/submissions.py` and `datasets.py`, but it has not been run end to end. When someone has run it, update
this entry.
