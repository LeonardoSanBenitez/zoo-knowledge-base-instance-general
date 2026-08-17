<!--kb
id: airflow-log-and-error-strings
labels: area:core, area:Scheduler, area:logging, area:task-sdk, kind:bug, topic:errors
triggers: zombie, SIGTERM, SIGKILL, "Task killed!", heartbeat, task_instance_heartbeat_timeout,
          "stuck in queued", "not found in serialized_dag table", DagNotFound,
          "Dependencies not met", "DagBag import timeout", "Dag with id", "Token Expired",
          "Invalid JWT token", "Missing auth token", "Not authenticated", 401, 403,
          AirflowException, AirflowTaskTimeout, AirflowSensorTimeout, AirflowSkipException,
          AirflowFailException, TaskDeferred, DownstreamTasksSkipped, DagRunTriggerException,
          "Task exited with return code", "Executor reports task instance", "Broken DAG",
          "Recorded pid", LocalTaskJob, RemovedInAirflow4Warning,
          traceback, stack trace, log message, warning log, log line, "keeps printing",
          dag processor, scheduler log, task log, error message
verified: 2026-08-05 @24c00690ab via kb_evidence/check_stale_strings.py and find_current_messages.py
-->

# Matching a pasted log line to Airflow 3.3 source

A ticket usually arrives as a log excerpt. Two failure modes, and the second one is mine:
the reporter quotes a line I cannot find, **or** I quote back a line that no longer exists.

## The finding that matters most: my remembered log lines are gone

I searched the whole worktree for the classic Airflow log strings, then ran `git log -S`
over the full 40k-commit history to distinguish "moved" from "deleted" from "never
existed". Results (`kb_evidence/check_stale_strings.log`):

| string I "remembered" | present in 3.3? | what history says |
|---|---|---|
| `Task received SIGTERM signal` | **no** | last touched by "Port `ti.run` to Task SDK execution path" (#50141, 2025-05) |
| `detected as zombie` | **no** | last touched 2020; the whole vocabulary is now *heartbeat timeout* |
| `Executor reports task instance` | **no** | reworded by "revamp some confusing log messages" (#40334, 2024-06) |
| `Task exited with return code` | **no** | removed with "Remove the old `task run` commands and LocalTaskJob" (#47453, 2025-03) |
| `Recorded pid ` | **no** | same commit — LocalTaskJob is gone |
| `Task is not able to be run` | **no** | same commit |
| `dependencies are not met` | **no** | removed with the old UI (#46942, 2025-02) |
| `Broken DAG` | **no** | the "DAG → Dag" prose refactor (#66088, 2026-04) rewrote it |
| `does not have a task with id` | **no** | **never existed** — I invented the wording |

That last row is the point. Nine confident memories, nine wrong, one of them a complete
fabrication. **Never quote an Airflow log line from memory; grep the clone.** The
`git log -S` step is what separates "renamed" from "I made it up", and it is cheap.

## Current (3.3) wording, and who emits it

| symptom the reporter describes | string to grep for | emitted by |
|---|---|---|
| task killed for missing heartbeats ("zombie") | `Task did not emit heartbeat within time limit` | `airflow-core/src/airflow/jobs/scheduler_job_runner.py:3707`; metric `scheduler.zombies.detected` with `tags={"reason": "heartbeat_timeout"}` at :3584 |
| task never leaves `queued` | `Task stuck in queued; will try to requeue` / `stuck in queued tries exceeded` | `scheduler_job_runner.py:3102-3139`; knob is `[scheduler] task_queued_timeout` |
| scheduler and executor disagree on state | `Executor %s reported that the task instance %s finished with state %s, but the task instance's state attribute is %s` | `scheduler_job_runner.py:1552` |
| DAG exists on disk but scheduler ignores it | `DAG '%s' ... not found in serialized_dag table` → `DagNotFound` | `scheduler_job_runner.py:569, 1565, 1569, 2019`. Means the **DAG processor** has not serialized it — route to parsing, not scheduling |
| asset-triggered runs not firing | `Dags have queued asset events (ADRQ), but are not found in the serialized_dag table` | `airflow-core/src/airflow/models/dag.py:702` |
| DAG file too slow to parse | `DagBag import timeout for {filepath} after {n}s` | `airflow-core/src/airflow/dag_processing/importers/python_importer.py:272`; knob `[dag_processor] dag_file_processor_timeout` |
| task waits forever on deps | `Dependencies not met for %s, dependency '%s' FAILED: %s` | `airflow-core/src/airflow/models/taskinstance.py:1158` — one of the very few 2.x-era lines that **survived** |
| worker-side kill | `Task killed!` | `task-sdk/src/airflow/sdk/execution_time/supervisor.py:1699` — note: the supervisor, not the scheduler, is the process that reports this in 3.x |
| local executor cleanup | `Worker process %s did not stop after SIGTERM. Sending SIGKILL.` | `airflow-core/src/airflow/executors/local_executor.py:307` |
| REST/API auth failures | `Not authenticated` (401) / `Token Expired` (401) / `Invalid JWT token` (**403**) / `Forbidden` (403) | `airflow-core/src/airflow/api_fastapi/core_api/security.py:122-129, 1050` |
| worker→API-server auth failure | `Missing auth token` (401) | `airflow-core/src/airflow/api_fastapi/execution_api/security.py:120` — this is the **execution** API; a task-side 401 is a different endpoint from a user-side 401 |
| REST 404 on a DAG | `Dag with id: {dag_id} was not found` | `api_fastapi/core_api/routes/public/dags.py` (several) |

Routing rule this table encodes: **which component emitted the line tells you the area
label**. `scheduler_job_runner.py` → `area:Scheduler`; `supervisor.py`/`task_runner.py` →
`area:task-sdk`; `api_fastapi/core_api` → `area:API`; `api_fastapi/execution_api` → the
worker protocol; `dag_processing/` → parsing, which reporters routinely mislabel as
scheduler.

## Exception classes worth recognising

`airflow-core/src/airflow/exceptions.py` and
`task-sdk/src/airflow/sdk/exceptions.py` (full dump in `kb_evidence/collect_repo_facts.log`).

Control-flow exceptions — **seeing these in a log is usually normal, not a bug**:
`AirflowSkipException`, `AirflowFailException` (fail without retries),
`AirflowSensorTimeout`, `TaskDeferred` (the deferrable/trigger handoff),
`DownstreamTasksSkipped`, `DagRunTriggerException`, `AirflowRescheduleException`.

Genuine-problem exceptions: `AirflowConfigException`, `AirflowNotFoundException`,
`DagNotFound`, `TaskNotFound`, `DuplicateTaskIdFound`, `TaskAlreadyInTaskGroup`,
`SerializationError`, `ParamValidationError`, `AirflowTaskTimeout`,
`FailFastDagInvalidTriggerRule`, `TaskAlreadyRunningError`.

`RemovedInAirflow4Warning(DeprecationWarning)` exists at 3.3 — deprecations are already
being staged for **Airflow 4**, so "deprecated" in a 3.x log does not mean "broken now".

`AirflowException` is the generic catch-all and the project is actively replacing it with
specific classes (open issue #71122, `kind:feature`) — a ticket complaining that an error
is unhelpfully generic is a known, welcomed direction, not a novel report.
