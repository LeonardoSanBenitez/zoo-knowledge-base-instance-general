<!--kb
id: mlflow-docker-projects-env
labels: area:projects, area:artifacts, area:docker, kind:gotcha, kind:version-fact, version:3.x
triggers: my code works locally and fails inside the container the tool builds for it; artifact upload fails from inside a project run but works outside it; which credentials are passed into the container and which are silently dropped; the container cannot authenticate to object storage;
          mlflow run, docker_env, MLproject, IllegalLocationConstraintException,
          "location constraint is incompatible", AWS_DEFAULT_REGION, AWS_SESSION_TOKEN,
          AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MLFLOW_S3_ENDPOINT_URL, MLFLOW_S3_IGNORE_TLS,
          _get_s3_artifact_cmd_and_envs, _get_docker_command, _artifact_storages,
          MLFLOW_DOCKER_WORKDIR_PATH, ~/.aws, /.aws, NoRegionError, InvalidClientTokenId,
          AZURE_STORAGE_CONNECTION_STRING, GOOGLE_APPLICATION_CREDENTIALS,
          AWS_PROFILE, AWS_SHARED_CREDENTIALS_FILE, AWS_CONFIG_FILE, NoCredentialsError,
          user_env_vars, environment block, "Copy from host", docker_args, mlflow run -A,
          "This project expects the", credentials not found in container
verified: 2026-08-23 by lucas at master `925d16f57` (re-checked: the four-name set is unchanged),
          earlier at v3.15.1 and `af7acb646`. Every claim below is either a `git show <tag>:<file>`
          quotation or the output of a command inlined in the text, run in Docker on Linux/x86_64.
          No AWS account was used, and none is needed to re-derive any of it.
-->

# `mlflow run` with a docker environment: which credentials actually reach the container

**Scope.** What MLflow copies from the host environment into the container it builds for a project
with a `docker_env`, and the two ways that set is incomplete. Relevant to any ticket where a
project works locally and fails inside `mlflow run`, or where artifact upload from a project
container fails while the same code works outside it.

## What is forwarded

`_get_docker_command` (`mlflow/projects/backend/local.py`) assembles the `docker run` argument
list, and asks `_get_docker_artifact_storage_cmd_and_envs(artifact_uri)` for the storage-specific
part. Dispatch is a dict keyed by the **exact class** of the resolved artifact repository:

```bash
git show v3.15.1:mlflow/projects/backend/local.py | sed -n '/_artifact_storages = {/,/}/p'
```

For `s3://` (which the registry maps to `S3ArtifactRepository`, not the `Optimized…` variant) the
forwarded set is exactly four names:

```bash
git show v3.15.1:mlflow/projects/backend/local.py | sed -n '/def _get_s3_artifact_cmd_and_envs/,/return volumes, envs/p'
#   AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, MLFLOW_S3_ENDPOINT_URL, MLFLOW_S3_IGNORE_TLS
```

Azure gets `AZURE_STORAGE_CONNECTION_STRING` and `AZURE_STORAGE_ACCESS_KEY`; GCS gets
`GOOGLE_APPLICATION_CREDENTIALS` **remapped** to a mounted `/.gcs`; anything else gets nothing.
Unset variables are dropped rather than forwarded empty.

## Gotcha 1 — no region, no session token (open as of 3.15.1)

`AWS_DEFAULT_REGION` and `AWS_SESSION_TOKEN` are **not** in that set, although
`S3ArtifactRepository`'s own docstring lists both as variables it honours
(`git show v3.15.1:mlflow/store/artifact/s3_artifact_repo.py | sed -n '234,238p'`). Consequences,
both reproducible with no AWS account because endpoint resolution and SigV4 signing are local:

```python
# pip install boto3; unset/set the variable and ask boto3 what it resolved
import boto3
boto3.Session().client("s3").meta.endpoint_url
#   AWS_DEFAULT_REGION=ap-east-1  -> region 'ap-east-1', https://s3.ap-east-1.amazonaws.com
#   AWS_DEFAULT_REGION unset      -> region 'us-east-1', https://s3.amazonaws.com
```

so a bucket outside `us-east-1` is addressed through the global endpoint and the first upload from
inside the container fails with `IllegalLocationConstraintException: The <region> location
constraint is incompatible for the region specific endpoint this request was sent to` — reported
as `mlflow/mlflow#2793` (2020, still open, `Acknowledged` + `priority/important-soon`, no PR ever
opened). And for temporary credentials (assume-role, SSO, IRSA), signing the same request with and
without the token shows the container's requests carry no `X-Amz-Security-Token`
(`botocore.auth.SigV4Auth(...).add_auth(request)`), which is what AWS rejects — the key and secret
alone are not a usable credential.

`git log -S 'AWS_DEFAULT_REGION' -- mlflow/projects/` is empty over the whole history: the name has
never been there, so this is not a regression to bisect.

## Gotcha 2 — the `~/.aws` volume is mounted where botocore does not read it

The same function mounts the host's `~/.aws` into the container **at `/.aws`**, while botocore
reads `~/.aws/credentials`. The Dockerfile MLflow generates sets `WORKDIR` and never `HOME`
(`git show v3.15.1:mlflow/projects/docker.py | sed -n '85,90p'`), so `~` is whatever the user's
base image says — `/root` by default. Measured both ways with the same fixture, in
`python:3.12-slim`:

```
mounted at /.aws       HOME=/root  /.aws/credentials exists       -> credentials None, region None
mounted at /root/.aws  HOME=/root  /root/.aws/credentials exists  -> credentials AKIA…, region ap-east-1
```

The second line is the control: the fixture is valid, so the first line means the mount MLflow
performs is simply not read. A base image that sets `HOME=/`, or a container running as a
different user, changes the answer — so the honest phrasing in a thread is "inert unless your image
sets `HOME=/`", not "broken".

**Workaround that needs no assumption about the image, measured rather than assumed**
(2026-08-23, same fixture, four cases in one run):

| case | credentials | region |
|---|---|---|
| mounted at `/.aws`, what MLflow does | `None` | `None` |
| mounted at `/root/.aws`, positive control | `AKIAFIXTUREKEY` | `ap-east-1` |
| `/.aws` **plus** `AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials` and `AWS_CONFIG_FILE=/.aws/config` | `AKIAFIXTUREKEY` | `ap-east-1` |
| those two variables set but nothing mounted there | falls back to forwarded env credentials | from `AWS_DEFAULT_REGION` |

Row 3 is the recipe worth giving someone; row 4 is its failure case, and it degrades to the
environment instead of breaking, which is what makes it safe to recommend. Pass both variables
through the project's `environment:` block (below), or set the credentials as plain environment
variables.

**A second gap sits behind this one**: `AWS_PROFILE` is not forwarded either, and is not in the
S3 branch at all. So even with the files named correctly, only the `[default]` profile resolves;
a named profile needs `AWS_PROFILE` declared in `environment:` as well.

## How to answer a ticket in this area

1. Establish which artifact backend the run uses — dispatch is by exact repository class, so a
   `s3://`-lookalike (Databricks-proxied, `mlflow-artifacts:`) takes a different branch entirely.
2. Ask what the *container* resolved, not what the host has: `docker inspect` the project container
   or print `boto3.Session().region_name` inside it. A host that works proves nothing here.
3. Remember the project's `environment:` list in `MLproject` is the supported escape hatch for any
   variable MLflow does not forward on its own (next section: it works, and it fails loudly).

## The supported escape hatch, and exactly how it behaves

`docker_env.environment` in the `MLproject` file. Two forms, both shown in MLflow's own docs
(`docs/docs/classic-ml/projects/index.mdx`, whose example is `- "AWS_PROFILE"  # Copy from host`):

```yaml
docker_env:
  image: my-image
  environment:
    - "AWS_DEFAULT_REGION"              # copy the value from the host environment
    - ["AWS_SESSION_TOKEN", "literal"]  # set an explicit value
```

`_get_docker_command(..., user_env_vars=...)` handles both. Measured against that function
(2026-08-23, `python:3.12-slim`):

| form | host variable | result |
|---|---|---|
| bare name | set | forwarded with the host value |
| `["NAME", "value"]` | irrelevant | forwarded with the literal |
| bare name | **unset** | `MlflowException: This project expects the ... environment variables to be set on the machine running the project` — the run stops, it does not silently continue |
| nothing declared | set | **not** forwarded unless it is in the artifact-backend set above |

The third row is why this is safe to recommend in a thread: a mistyped or missing variable fails
at launch with the name in the message, rather than producing a container that cannot authenticate.

`mlflow run -A` (`docker_args`) is the other route — it appends raw flags to `docker run`, so
`-A e=NAME=value` reaches the same place — but it is a per-invocation flag, not a property of the
project, and the `environment:` list is what the docs point at.
