<!--kb
id: mlflow-auth-rbac
labels: area:server-infra, area:tracking, area:artifacts, kind:version-fact, kind:howto, version:3.x
triggers: the permissions endpoint I remember returns 404; how do I give a user read only access to one experiment; a correct looking auth configuration behaves as if it were ignored; how does this tracking server decide who may see what;
          basic-auth, --app-name basic-auth, mlflow.server.auth, basic_auth.ini, default_permission,
          MLFLOW_AUTH_CONFIG_PATH, admin_username, password1234, grant_default_workspace_access,
          "Permission denied", 403, RBAC, role_permissions, roles/create, roles/permissions/add,
          roles/assign, users/permissions/grant, users/permissions/get, experiments/permissions/create,
          registered-models/permissions, CREATE_EXPERIMENT_PERMISSION, NO_PERMISSIONS,
          READ USE EDIT MANAGE, WORKSPACE_GRANTABLE_PERMISSIONS, resource_pattern, resource_type,
          workspaces, MLFLOW_ENABLE_WORKSPACES, --enable-workspaces, X-MLFLOW-WORKSPACE,
          "mlflow-artifacts:/workspaces/", artifact_location, mlflow-artifacts proxy,
          MLFLOW_FLASK_SERVER_SECRET_KEY, "static secret key needs to be set",
          "Invalid Host header", MLFLOW_SERVER_ALLOWED_HOSTS,
          "Password must be a string longer than 12 characters",
          "You are not authenticated"
verified: 2026-08-17 by lucas — every claim below was either read at a release tag in a full clone
          (v3.9.0 … v3.15.1) or produced by running the servers named in §6 in Docker. Commands are
          inlined so anyone can re-derive them without access to the author's scripts.
-->

# MLflow basic-auth and RBAC — the model changed twice, and remembered answers are wrong

**Scope.** MLflow's built-in `basic-auth` app: how permissions are expressed, how they resolve at
request time, and the operational traps that make a correct configuration look broken. Companion
to `mlflow-2026-snapshot.md`, which covers the rest of the 3.x delta.

**Why this exists.** A pretrained answer about MLflow auth describes the 2.x/early-3.x model:
per-resource permission tables and endpoints like
`POST /api/2.0/mlflow/experiments/permissions/create`, with `READ`/`EDIT`/`MANAGE`/`NO_PERMISSIONS`
attached directly to a user. **That API no longer exists**, and repeating it to someone on 3.13+
sends them to a 404.

---

## 1. The two changes, with dates

| what | commit | first release |
|---|---|---|
| RBAC data model — roles, `role_permissions`, store CRUD | `6624f695e` (#22721), 2026-04-22 | **v3.12.0** |
| RBAC REST API + permission resolution + client | `1094ec1cf` (#22722) | **v3.12.0** |
| Legacy per-resource permission methods **and endpoints removed** | `fc45c72e1` (#23337), 2026-05-18 | **v3.13.0** |
| `default_permission` becomes a floor; workspace `USE` stops folding into resource lookups | `ef409cab8` (#23379), 2026-05-18 | **v3.13.0** |
| Workspaces (multi-tenant isolation) merged | `2e0adcfe2` (#20657), 2026-02-10 | **v3.10.0** |

Note there is **no `v3.11.0` tag** — the 3.11 line shipped as **`v3.11.1` (2026-04-07)** only.
A `git show v3.11.0:…` therefore returns "invalid object name", which is silence, not evidence:
it means the tag is missing, not that the code is absent, and not that 3.11 never existed. Full
tag list and dates: `mlflow-release-map.md`.

Migration `e5f6a7b8c9d0` backfills the old per-resource tables into `role_permissions` under a
synthetic `__user_<id>__` role per `(user, workspace)` pair. The legacy tables are deliberately
**not dropped** — they remain as a rollback snapshot, and a later migration
(`f6a7b8c9d0e1`, tracked by issue #23087) will retire them. After the backfill,
`role_permissions` is the only table the auth server reads.

## 2. The model as of 3.14–3.15

A grant is a row: **`(role, resource_type, resource_pattern, permission)`**, and a user gets
grants by being assigned roles. Roles are **per workspace**.

* `permission` ∈ `READ` < `USE` < `EDIT` < `MANAGE` (`NO_PERMISSIONS` still exists internally as
  the "no presence in this workspace" signal, but **cannot be granted on a resource** any more).
* `resource_type` ∈ `experiment`, `registered_model`, `prompt`, `scorer`, `gateway_secret`,
  `gateway_endpoint`, `gateway_model_definition`, `mcp_server`, and the special `workspace`.
* `resource_pattern` is a concrete id or `*`.
* **`resource_type='workspace'` accepts only `USE` or `MANAGE`** (`WORKSPACE_GRANTABLE_PERMISSIONS`).
  This is the two-tier workspace model: `USE` = member (may enter the workspace and create
  resources), `MANAGE` = workspace administrator. `READ`/`EDIT` at workspace scope are no longer
  expressible.

Resolution order at request time (`_get_role_permission_or_default`):

1. collect the user's roles **in the workspace that owns the resource**;
2. a `('workspace','*')` row folds into a resource-type query **only if it is `MANAGE`** — since
   #23379, workspace `USE` does not confer anything on individual resources;
3. otherwise match `resource_type` and `resource_pattern in ('*', <id>)`, taking the max;
4. `default_permission` from `basic_auth.ini` (default `READ`) is a **floor**, not a fallback —
   it is max'd in, except when the answer is the workspace-boundary deny.

**Two consequences people get wrong.** A user with `workspace:* USE` + `experiment:* MANAGE` is a
perfectly ordinary "data scientist" shape — the workspace grant only lets them in. And
`default_permission = READ` means *every* authenticated user can read every resource in a
workspace they belong to; tightening that is a config change, not a grant change.

## 3. The REST surface (3.12+), which is what replaced the removed endpoints

All under `/api/3.0/`, admin-authenticated, JSON bodies:

```
POST /api/3.0/mlflow/roles/create              {"name", "workspace"}
POST /api/3.0/mlflow/roles/permissions/add     {"role_id", "resource_type", "resource_pattern", "permission"}
POST /api/3.0/mlflow/roles/assign              {"username", "role_id"}
GET  /api/3.0/mlflow/roles/list | /roles/permissions/list | /users/roles/list
POST /api/3.0/mlflow/users/permissions/grant   {"username", "resource_type", "resource_id", "permission"}
GET  /api/3.0/mlflow/users/permissions/get     ?username=&resource_type=&resource_id=
```

`users/permissions/{grant,revoke}` are convenience wrappers that write to the user's synthetic
`__user_<id>__` role. **`users/permissions/get` is the diagnostic tool worth knowing**: it resolves
the effective permission through the same path a real request takes, so it answers "what does the
server think this user can do" without reproducing the failure. It returns
`{"allowed": <can_use>, "permission": "<name>"}` — note `allowed` mirrors `can_use`, so a `READ`
grant reports `allowed:false`.

User management stayed on `/api/2.0/`: `users/create`, `users/list`, `users/update-password`,
`users/update-admin`, `users/delete`.

## 4. Workspaces, and the one thing that is immutable

Workspaces are **off by default** (`MLFLOW_ENABLE_WORKSPACES`, default `false`; CLI
`--enable-workspaces/--disable-workspaces`). When on:

* every request must carry the workspace — header `X-MLFLOW-WORKSPACE: <name>`, or
  `MLFLOW_WORKSPACE` / `mlflow.set_workspace()` on the client;
* a **newly created experiment stores** `artifact_location = mlflow-artifacts:/workspaces/<ws>/<id>`
  (`SqlAlchemyWorkspaceStore._get_artifact_location`) — **including in the `default` workspace**;
* that string is written once, at creation, and never recomputed. Experiments created before
  workspaces were enabled keep `mlflow-artifacts:/<id>` forever, and experiments created while
  they were enabled keep the prefixed form **even after workspaces are turned off again**.

That immutability is the root of a whole class of confusing behaviour: the proxied artifact URL a
client builds comes from this stored string, so "is workspaces on right now" is the wrong question
to ask about an artifact problem. The right one is *what does this experiment's `artifact_location`
say* (`GET /api/2.0/mlflow/experiments/get`).

## 5. Worked failure — 403 on artifact upload with a correct-looking grant

On **3.14.0**, a user with `workspace:* USE` + `experiment:* MANAGE` can create runs and log params
and metrics, but every `log_artifact` returns **403 Permission denied**, while
`users/permissions/get` cheerfully reports `MANAGE`.

Mechanism: the proxied upload goes to
`PUT /api/2.0/mlflow-artifacts/artifacts/workspaces/default/<exp>/<run>/artifacts/<file>`, and the
auth validator extracts the experiment id from that path with `^(\d+)/`. The workspace prefix means
no match, so the experiment grant is never consulted and resolution falls back to the workspace
tier — `USE`, whose `can_update` is false. Params and metrics are unaffected because those routes
read `experiment_id` from the request **body**, not from a path.

Fixed by #24214 (`b567ee381`, regex widened to `^(?:workspaces/[^/]+/)?(\d+)/`), first released in
**v3.15.0**. Established by moving that one line in both directions on installed packages: patched
into 3.14.0 the upload succeeds; reverted into 3.15.1 the 403 returns. Reported twice — #24210
(non-default workspace) and #24430 (default workspace) — and the second was filed because #24210's
writeup claimed the `default` workspace was unaffected, which is false for experiments created after
workspaces were switched on.

Two workarounds for anyone pinned to 3.14.0, both measured: upgrade **only the server** (a 3.14.0
client against a 3.15.0 server uploads and downloads byte-identical files, with a local artifact
store); or grant `workspace:* MANAGE`, which restores writes at the cost of making that user a
workspace administrator — measured, they can then create roles, create users, and list every user
with their permissions.

## 6. Operational traps — each one cost a debugging cycle

Reproducing anything auth-related takes this, and every item below made a correct setup look broken:

```bash
pip install "mlflow[auth]==3.14.0"                      # the [auth] extra is required (Flask-WTF)
export MLFLOW_FLASK_SERVER_SECRET_KEY=any-non-empty     # else the server refuses to start
mlflow server --app-name basic-auth --enable-workspaces \
  --backend-store-uri sqlite:///mlflow.db \
  --artifacts-destination ./mlartifacts --serve-artifacts \
  --host 127.0.0.1 --port 5000
```

1. **`MLFLOW_FLASK_SERVER_SECRET_KEY` is mandatory** for the basic-auth app — without it startup
   dies with *"A static secret key needs to be set for CSRF protection"*, inside a uvicorn worker
   traceback that does not obviously point at auth.
2. **Passwords must be ≥ 12 characters** (`_validate_password`, `mlflow/utils/validation.py`).
   The error message says *"longer than 12 characters"* but the check is `len(password) < 12`, so
   exactly 12 is accepted. A short password fails the `users/create` call with a 400 that is easy
   to miss if the response is not checked — the rest of the script then fails confusingly on a
   user that does not exist. (Raised from 8 to 12 in #15287.)
3. **With workspaces enabled, a request without the workspace header answers
   `You are not authenticated`** even with correct credentials — an authorization problem wearing
   an authentication error's clothes.
4. **`MLFLOW_SERVER_ALLOWED_HOSTS`**: the server validates the `Host` header (DNS-rebinding
   protection) and rejects anything but the bound host with
   *"Invalid Host header - possible DNS rebinding attack detected"*. Reaching a server by container
   name or service name needs this set.
5. **The shipped defaults are `admin` / `password1234`** in `mlflow/server/auth/basic_auth.ini`,
   and the server logs a warning while happily continuing. Point `MLFLOW_AUTH_CONFIG_PATH` at your
   own copy to change `default_permission`, the admin credentials, or
   `grant_default_workspace_access`.

## 7. What is NOT covered here

Not verified, so not claimed: OIDC/SSO or any third-party auth plugin (`authorization_function`
can point anywhere); anything about permissions on remote artifact stores, where the proxy is not
in the path at all; and the Admin UI, which we do not exercise.
