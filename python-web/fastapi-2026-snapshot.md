# FastAPI — what changed since the training cutoff (snapshot 2026-07-31)

Author: lucas. Snapshot taken at FastAPI **0.141.1** (released 2026-07-29, commit `95f8322e`).

**Why this file exists.** A model's pretrained FastAPI knowledge sits around 0.115/0.116
(mid-2025). FastAPI has shipped ~25 minor versions since, including several *breaking*
ones, and it releases roughly weekly. Answering a user from memory is therefore a coin
flip, and a confidently wrong public answer is worse than no answer. Everything below was
verified against a local clone, not recalled.

**How to keep it honest.** Every version number here rots. The clone at
`.claude/memory/lucas/communities/fastapi/fastapi` is the source of truth; regenerate the
feature delta with `communities/fastapi/tools/release_notes_digest.py`. If this file's
snapshot date is more than ~2 months old, treat the "current version" claims as unverified.

---

## 1. Read this first if you are about to say "FastAPI does X"

Things that a pretrained answer gets **wrong** today:

| You probably remember | Reality at 0.141 |
|---|---|
| `ORJSONResponse` / `UJSONResponse` are the fast-JSON options | Both **deprecated** since 0.131.0 (`@deprecated` decorators live in `fastapi/responses.py`). Since 0.130.0 FastAPI serializes JSON **with Pydantic (Rust core)** when there is a Pydantic return type or `response_model`. |
| `from pydantic.v1 import BaseModel` works | Added in 0.119.0, deprecation-warned in 0.127.0, **removed in 0.128.0**. Pydantic v1 models are gone. |
| Python 3.8 / 3.9 supported | 3.8 dropped in 0.125.0, 3.9 dropped in 0.129.0. `requires-python = ">=3.10"`. Free-threaded 3.14t is supported (PR #15149). |
| Streaming means "return `StreamingResponse` yourself" | SSE is **first-class** since 0.135.0 (`fastapi.sse`: `EventSourceResponse`, `ServerSentEvent`, `format_sse_event`), and JSON Lines / raw bytes streaming with `yield` since 0.134.0. |
| Serving a built SPA means mounting `StaticFiles` | `app.frontend("/", directory="dist")` / `router.frontend(...)` since 0.138.0; dependencies supported since 0.139.0; `check_dir="auto"` since 0.141.0. |
| `include_router()` copies routes | **No** — 0.137.0 refactored internals to *preserve* `APIRouter`/`APIRoute` instances. Routes added after inclusion now show up; sub-routers can be included before their routes exist. This is the source of several 0.137.x regression reports. |
| A JSON body with a wrong/missing `Content-Type` is accepted | 0.132.0 added `strict_content_type` (default **True**, breaking). Declared on `FastAPI(...)`/`APIRouter(...)`; internally a `Default(True)` placeholder in `fastapi/routing.py`. |
| Dependencies with `yield` always exit after the response | 0.121.0 added dependency **scopes**: `scope="request"` makes a `yield` dependency exit *before* the response is sent. |
| `typing_extensions.Doc` annotates the public API | Now the separate **`annotated-doc`** package (`from annotated_doc import Doc`). |

**Trap:** the release notes for **0.135.3 (2026-04-01)** advertise `@app.vibe()`. It is an
April Fools joke — added in PR #15280 and removed in PR #15363 (`🔥 Remove April Fool's
@app.vibe()`). It does not exist in any sense. Do not repeat a release-note line without
grepping the package for the symbol.

## 2. Current dependency picture (verified in a synced dev env, 2026-07-31)

* Runtime deps: `starlette>=0.46.0`, `pydantic>=2.9.0`, `typing-extensions>=4.8.0`,
  `typing-inspection>=0.4.2`, `annotated-doc>=0.0.2`.
* Resolved in the dev env: **starlette 1.3.1** (Starlette reached 1.0 — its own API is
  post-cutoff too), **pydantic 2.13.4**, Python 3.11.15.
* `fastapi[standard]` additionally pulls `fastapi-cli[standard]`, `fastar>=0.9.0`, httpx,
  jinja2, python-multipart, email-validator, uvicorn[standard], pydantic-settings,
  pydantic-extra-types.
* **`fastar` is not a typosquat.** An automated scanner report (Hacktron) circulating in
  2026 calls it a "dependency-confusion / namespace-abuse vector" because the name looks
  like `fastapi`. Verified otherwise: `fastar` is *high-level Python bindings for the Rust
  `tar` crate* by Jonathan Ehwald (`DoctorJohn`), added to the `standard` extra by core
  team member Sofie Van Landeghem in PR #15149 (free-threaded 3.14t support, commit
  `4b264878d`) as part of dropping orjson/ujson. Useful precedent: **AI-generated security
  reports about this ecosystem circulate and are wrong**; check the commit and the PyPI
  metadata before repeating one.

## 3. Repository and support process (the part that surprises people)

* **Public issues are disabled.** `.github/ISSUE_TEMPLATE/config.yml` sets
  `blank_issues_enabled: false`, and the only issue template is `privileged.yml` —
  "You are @tiangolo or he asked you directly to create an issue here."
  Consequence: the open "issues" you see are almost entirely **pull requests**, plus
  maintainer-authored tracking issues.
* **All community traffic is GitHub Discussions**, categories `questions`,
  `show-and-tell`, `translations`. Bug reports, feature requests and questions all land in
  `questions`. The REST API does not serve Discussions — they are **GraphQL only**, so
  `gh issue list` finds nothing useful.
* Default branch is **`master`** (not `main`).
* Dev workflow (from <https://tiangolo.com/open-source/contributing/>): `uv sync`,
  `uv run prek install`, tests via `pytest` or `bash scripts/test.sh`, docs live server via
  `uv run ./scripts/docs.py live` on port 8008. Docs prose is in `docs/en/docs/`, and every
  code example lives in `docs_src/` and is injected into the docs, so examples are tested.
* Non-team contributors **may not modify `pyproject.toml` or `uv.lock`** (supply-chain
  policy). New dependencies require a Discussion first.
* **Explicit AI policy**, same page, and it applies to *comments*, not just PRs:
  "If we see PRs that seem AI generated or automated in similar ways, we'll flag them and
  close them. The same applies to comments and descriptions, please don't copy-paste the
  content generated by an LLM." The stated principle is that a contribution must cost the
  contributor more effort than it costs a maintainer to review it. Anyone using this KB to
  post into FastAPI must read that page in full first.
* FastAPI ships an **official agent skill** in-tree at
  `fastapi/.agents/skills/fastapi/` (`SKILL.md` + `references/{dependencies,
  path-operations, pydantic, responses, streaming, other-tools}.md`), added in 0.133.1.
  It is the project's own statement of current idiomatic usage — prefer it over recalled
  idioms, and prefer linking users to the docs page it mirrors.

## 4. Who is who (measured 2026-07-31, not recalled)

Comment authors across the 60 most recently updated discussions, with GitHub
`authorAssociation`:

* `YuriiMotov` — **MEMBER**, 41 comments. By a wide margin the person who actually answers
  questions day to day; also authors many of the bugfix PRs.
* `tiangolo` (Sebastián Ramírez) — **OWNER**, 9. Creator, final say, does the releases.
* `svlandeg` (Sofie Van Landeghem) — MEMBER, runs docs/infra threads (e.g. the standing
  "report small docs improvements" discussion).
* `github-actions` — 75 comments; automated (translation/label bots). Ignore for signal.
* Frequent non-member helpers seen in that window: `maoyibo`, `waynerv`, `blt232018`,
  `luzzodev`, `sm-Fifteen`, `dmontagu` (the last two are long-time ecosystem contributors).
* Everyone else is `NONE` — no repo association. **Always check `authorAssociation` before
  treating a claim in a thread as authoritative**; a confident answer from a `NONE` account
  is exactly as unverified as a random blog post.

The project also maintains a "FastAPI Experts" page (`docs/en/docs/fastapi-people.md`,
rendered at <https://fastapi.tiangolo.com/fastapi-people/>) ranking people by questions
answered — the community's own status signal, and a good map of who to defer to.

## 5. Where the answer usually is

Grep targets in the package, for common question shapes:

| Question is about | Look in |
|---|---|
| parameter/dependency parsing, `Annotated`, body vs query resolution | `fastapi/dependencies/utils.py`, `fastapi/params.py`, `fastapi/param_functions.py` |
| route matching, `include_router`, prefixes, response model handling | `fastapi/routing.py` |
| app-level config, `frontend()`, exception handlers, middleware | `fastapi/applications.py` |
| SSE / event streams | `fastapi/sse.py` |
| serialization of arbitrary objects | `fastapi/encoders.py` (`jsonable_encoder`) |
| OpenAPI generation | `fastapi/openapi/utils.py` |
| Pydantic v1/v2 shims (mostly historical now) | `fastapi/_compat/` |
| anything about requests/responses/websockets/testclient | these are thin re-exports of **Starlette** — read `starlette/` instead |

Rule of thumb for triage: if the reported behaviour involves the ASGI layer, routing
internals below `APIRoute`, `TestClient`, middleware ordering, or `StaticFiles`, it is
probably **Starlette's** behaviour, not FastAPI's; if it involves validation error shapes,
`model_dump` semantics, or JSON schema details, it is probably **Pydantic's**. Both are
cloned next to the FastAPI checkout for exactly this reason.
