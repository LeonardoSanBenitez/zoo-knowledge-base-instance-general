<!--kb
id: airflow-config-2to3
labels: area:core, area:Scheduler, area:API, area:logging, area:upgrade, kind:bug, topic:config
triggers: my config file stopped working after the major upgrade; the option I set is being ignored and I cannot tell if it was renamed or removed; which settings changed name between the two major versions; how do I check a config file against the release I am on;
          airflow.cfg, airflow config lint, AIRFLOW__, sql_alchemy_conn, dag_concurrency,
          scheduler_zombie_task_threshold, zombie_detection_interval, min_file_process_interval,
          parsing_processes, max_threads, dag_dir_list_interval, web_server_port, base_url,
          secret_key, expose_config, worker_refresh_interval, check_slas, catchup_by_default,
          create_cron_data_intervals, enable_xcom_pickling, task_runner, statsd_on,
          worker_pods_pending_timeout, stalled_task_timeout, task_adoption_timeout,
          session_lifetime_days, auth_backend, webserver section, kubernetes_executor section,
          "Unknown section", "option is not recognized", "has been removed"
verified: 2026-08-05 @24c00690ab via kb_evidence/extract_config_changes.py
-->

# Airflow config: what moved, vanished or flipped between 2.x and 3.x

**Source of truth**: `airflow-core/src/airflow/cli/commands/config_command.py`, the table
behind `airflow config lint`. 161 `ConfigChange` entries at this commit: **97 renamed,
60 removed, 4 default changes.**

## Use it like this

A large share of "upgraded to 3 and X broke" reports are a config move, not a bug. Before
anything else:

> `airflow config lint` reports exactly this, per-deployment. Pointing a reporter at that
> command is often the whole answer, and it is the answer a maintainer would give.

Two structural moves explain most of the 97 renames, and knowing them beats memorising
rows:

1. **`[webserver]` is gone as a concept.** It split by *responsibility*: serving concerns
   → `[api]` (the FastAPI API server), authentication/branding/session concerns → `[fab]`
   (now a provider). So `web_server_port → [api] port`, `base_url → [api] base_url`,
   `secret_key → [api] secret_key`, `cookie_secure → [fab] cookie_secure`.
   *This is why an OAuth redirect breaks on upgrade: auth routes are now under `/auth`.*
2. **Parsing moved out of the scheduler into `[dag_processor]`.** `max_threads →
   [dag_processor] parsing_processes`, `min_file_process_interval`, `print_stats_interval`,
   `stale_dag_threshold`, `file_parsing_sort_mode`, and `dag_dir_list_interval →
   [dag_processor] refresh_interval` all moved. A "my DAG changes take forever to appear"
   ticket where the user tuned `[scheduler]` is tuning a section nobody reads any more.

Two more clusters: DB settings `[core] sql_alchemy_* → [database] sql_alchemy_*`, and
metrics `[scheduler] statsd_* → [metrics] statsd_*` (then `statsd_allow_list →
metrics_allow_list`).

## Renames that most often produce a *silent* wrong behaviour

| 2.x | 3.x | why it bites |
|---|---|---|
| `[scheduler] scheduler_zombie_task_threshold` | `[scheduler] task_instance_heartbeat_timeout` | "zombie" is no longer the vocabulary; a user grepping docs for zombie finds nothing |
| `[scheduler] zombie_detection_interval` | `[scheduler] task_instance_heartbeat_timeout_detection_interval` | same |
| `[scheduler] local_task_job_heartbeat_sec` | `[scheduler] task_instance_heartbeat_sec` | LocalTaskJob itself was deleted (#47453, 2025-03-07) |
| `[celery] stalled_task_timeout`, `[celery] task_adoption_timeout`, `[kubernetes_executor] worker_pods_pending_timeout` | all three → `[scheduler] task_queued_timeout` | three executor-specific knobs collapsed into one core one; "tasks stuck in queued" tickets land here |
| `[scheduler] processor_poll_interval` | `[scheduler] scheduler_idle_sleep_time` | perf-tuning advice from blog posts is stale |
| `[core] dag_concurrency` | `[core] max_active_tasks_per_dag` | renamed back in 2.2; still pasted in tickets |
| `[core] dataset_manager_class` | `[core] asset_manager_class` | Datasets → Assets rename, everywhere |
| `[api] auth_backend(s)` | `[fab] auth_backends` | only applies if FAB provider is installed at all; default auth manager is SimpleAuth |
| `[webserver] session_lifetime_days` | `[fab] session_lifetime_minutes` | **unit changes** — a copied value is off by 1440× |
| `[triggerer] default_capacity` | `[triggerer] capacity` | |
| `[admin] sensitive_variable_fields` | `[core] sensitive_var_conn_names` | masking questions |
| `[scheduler] child_process_log_directory` | `[logging] dag_processor_child_process_log_directory` | "where are the parser logs" |

Full list: `kb_evidence/extract_config_changes.log`, section `RENAMED`.

## Removed outright (60) — the ones worth recognising

- `[core] check_slas` — **the SLA feature is gone in 3.0**, replaced by Deadline Alerts. A
  ticket asking why SLA callbacks never fire is not a bug.
- `[core] enable_xcom_pickling`, `[core] task_runner` — XCom pickling and the pluggable
  task runner are both gone; task execution is the Task SDK supervisor now.
- `[core] hostname`, `[operators] allow_illegal_arguments`,
  `[scheduler] allow_trigger_in_future`, `[scheduler] dependency_detector`,
  `[scheduler] dag_stale_not_seen_duration`.
- `[logging] log_filename_template` and `[logging] log_processor_filename_template`, plus
  `[elasticsearch] log_id_template` — **custom log-path templating is no longer
  configurable**. Recurrent source of "my remote logs 404 after upgrade".
- `[email] email_backend`, `[smtp] smtp_user`, `[smtp] smtp_password` — credentials moved
  into the `smtp_default` **connection**; config-file SMTP creds are ignored.
- `[logging] enable_task_context_logger` — replaced by the Log table.
- ~30 `[webserver] *` UI knobs (`analytics_*`, `audit_view_*`, `default_ui_timezone`,
  `expose_stacktrace`, `worker_refresh_interval`, `show_trigger_form_if_no_params`, …).
  The React UI simply does not read them. Expect these as "the setting has no effect"
  reports; the honest answer is that the option no longer exists, and a *feature request*
  for the React UI is the right venue.

`[core] parallelism` and `[core] strict_dataset_uri_validation` appear as removals with a
value-validity note rather than a plain deletion — read the source row before quoting.

## Defaults that flipped (these change behaviour with no config error at all)

| option | 2.x | 3.x | consequence |
|---|---|---|---|
| `[core] executor` | `SequentialExecutor` | `LocalExecutor` | SequentialExecutor no longer exists |
| `[scheduler] catchup_by_default` | `True` | `False` | "my DAG didn't backfill on unpause" — expected now |
| `[scheduler] create_cron_data_intervals` | `True` | `False` | a bare cron string now builds `CronTriggerTimetable`, **not** `CronDataIntervalTimetable`; `data_interval_start/end` and every `ds`/`ts` template derived from them shift, and `run_id` no longer tracks `logical_date` the old way (see open #71187) |
| `[scheduler] create_delta_data_intervals` | `True` | `False` | same shape, for `timedelta` schedules |

`create_cron_data_intervals` is the highest-value item on this page: it appears in
3 of 185 recent open issue titles, and it changes *values users compute with* while
raising no error.

## Caveats

- The table is the **2.x→3.0 lint table**; it is not a changelog of 3.1→3.3 changes.
  For those, read `airflow-core/newsfragments/` and `RELEASE_NOTES.rst`.
- Provider config sections (`[celery]`, `[kubernetes_executor]`, `[fab]`, `[smtp]`) live
  in provider packages, so the *option* may exist or not depending on installed providers
  — always ask which providers and versions are installed before declaring an option gone.
- Environment-variable form is `AIRFLOW__<SECTION>__<OPTION>`, uppercased: a rename
  invalidates the env var too, and env vars fail *silently* (no unknown-key warning).
