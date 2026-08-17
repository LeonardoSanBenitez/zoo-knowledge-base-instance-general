<!--kb
id: airflow-docker-image
labels: area:core, area:dev-env, area:helm-chart, kind:feature, kind:bug, topic:image, topic:deployment
triggers: apache/airflow:3.3.0, docker image, Dockerfile, AIRFLOW_UID, 50000, /opt/airflow,
          AIRFLOW_EXTRAS, prod_image_installed_providers, extending the image,
          customizing the image, apt-get install, airgapped, air-gapped, odbc, odbcinst.ini,
          unixODBC, pyodbc, libtdsodbc.so, tdsodbc, FreeTDS, msodbcsql18, "Can't open lib",
          IM002, "Data source name not found", mysqlclient, mssql, driver not found
verified: 2026-08-05 @24c00690ab (Dockerfile) + live containers, see ticket d71116 logs
-->

# What the official `apache/airflow` image actually contains

From the root `Dockerfile` at this commit (`kb_evidence/collect_repo_facts.log`, section
"production Dockerfile"):

| ARG | value at 3.3.0 |
|---|---|
| `AIRFLOW_VERSION` | `3.3.0` |
| `AIRFLOW_HOME` | `/opt/airflow` |
| `AIRFLOW_UID` | `50000` |
| `INSTALL_MYSQL_CLIENT` / `INSTALL_MSSQL_CLIENT` / `INSTALL_POSTGRES_CLIENT` | all `true` |
| `AIRFLOW_PIP_VERSION` / `AIRFLOW_UV_VERSION` | `26.1.2` / `0.11.29` |
| `DEV_APT_DEPS` / `RUNTIME_APT_DEPS` | **empty** — extra OS packages are opt-in at build time |

`AIRFLOW_EXTRAS` baked in: `aiobotocore, amazon, async, celery, cncf-kubernetes,
common-io, common-messaging, docker, elasticsearch, fab, ftp, git, google, google-auth,
graphviz, grpc, hashicorp, http, ldap, microsoft-azure, mysql, odbc, openlineage,
opensearch, pandas, postgres, redis, sendgrid, sftp, slack, snowflake, ssh, statsd, uv`.

Providers preinstalled (`prod_image_installed_providers.txt`): amazon, celery,
cncf.kubernetes, common.compat, common.io, common.messaging, common.sql, docker,
elasticsearch, fab, ftp, git, google, grpc, hashicorp, http, microsoft.azure, mysql, odbc,
openlineage, opensearch, postgres, redis, sendgrid, sftp, slack, smtp, snowflake, ssh,
standard. **Everything else — 105 provider distributions exist — is not in the image.**

## The project's own position on "the image is missing X"

Long-standing and repeatedly restated by the PMC (e.g. discussion #23561, 2022, `potiuk`):
**the images are convenience packaging with no guarantees; customising/extending them is
the supported path.** So a "please add package X to the default image" request is a
legitimate feature request, but the default answer is "extend the image", and the burden
is to show why X is different (widely needed, tiny, no alternative). Note the asymmetry to
argue honestly: the Python extra can already be installed (`odbc` extra ships `pyodbc`)
while the **OS-level** piece cannot be pip-installed — that is the real gap in this class
of request.

## The ODBC / native-driver class of ticket (worked end to end, d71116)

Verified live in `apache/airflow:3.3.0`; scripts and raw logs:
`.claude/memory/lucas/communities/airflow/tickets/d71116/`.

- The image ships `pyodbc` + unixODBC + Microsoft's **`msodbcsql18`** (under
  `/opt/microsoft/...`), but **no FreeTDS driver**. `freetds-bin` provides CLI tools and
  **no shared library**; the driver `libtdsodbc.so` lives in Debian's `tdsodbc` package
  (1.3.17+ds-2), 498 kB installed, no extra dependencies, ~+0.8 MB on the image.
- Against a real Sybase ASE 15.7 server: stock image → `Can't open lib 'FreeTDS'`; with
  `tdsodbc` installed → full DDL/DML round trip, including through Airflow's `OdbcHook`.
  The image's own `msodbcsql18` **fails** against that server with `Protocol error in TDS
  stream` — i.e. the bundled driver is not a substitute.
- **The workaround that fits an airgapped deployment**: the `.so` works when *mounted into
  the unmodified image* and referenced by absolute path (`DRIVER=/path/to/libtdsodbc.so`
  in the connection string / `odbcinst.ini`). No rebuild, no `apt`.

### The generalisable trap (cost me a wrong claim)

**unixODBC has no driver search path.** It loads whatever absolute path `odbcinst.ini`
names. So "directory `/usr/lib/x86_64-linux-gnu/odbc/` does not exist" proves *nothing*
about whether a driver is installed — the image's own working driver lives under
`/opt/microsoft`. The convention is real (four Debian ODBC driver packages install there)
but it is only a convention.

The evidence that does hold is **asking the driver manager itself**:

```
python -c "import pyodbc; print(pyodbc.drivers())"   # what odbcinst.ini registers
pyodbc.connect("DRIVER={...};SERVER=...")            # then read the actual error
```

`Can't open lib '<name>'` = registered but the file is missing/unloadable.
`Data source name not found ... no default driver specified (IM002)` = not registered at
all. A connection error like FreeTDS `20009` (server unavailable) is *success* for the
driver-loading question — the driver loaded and got as far as the network. Distinguishing
those three is the whole diagnosis, and it generalises to any native-library ticket:
**ask the component, don't inspect around it.**

## Practical notes for reproductions

- `docker run --rm apache/airflow:3.3.0 <cmd>` is the fastest verification loop available
  on a machine without Breeze, and it is honest evidence as long as the version is stated.
- The container runs as UID 50000; `apt-get` inside it needs `--user root`.
- Docker Hub carries released tags only. At 2026-08-05, `3.3.0` was the newest published
  image even though `main`'s docs already referenced 3.4.0 — **check the tag exists before
  telling anyone to pull it.**
- For arch-specific claims (`arm64`), this machine cannot emulate arm64; check package
  availability in the Debian archive instead of asserting from a local pull.
