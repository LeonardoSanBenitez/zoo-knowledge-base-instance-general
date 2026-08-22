<!--kb
id: mlflow-tracing-otel-interop
labels: area:tracing, kind:mechanism, kind:gotcha, version:3.x
triggers: OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
          OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL,
          OTEL_EXPORTER_OTLP_TRACES_PROTOCOL, OTEL_EXPORTER_OTLP_METRICS_PROTOCOL,
          MLFLOW_ENABLE_OTLP_EXPORTER, MLFLOW_USE_DEFAULT_TRACER_PROVIDER,
          MLFLOW_TRACE_ENABLE_OTLP_DUAL_EXPORT, MLFLOW_ENABLE_ASYNC_TRACE_LOGGING,
          mlflow.tracing.set_destination, MlflowExperimentLocation, context_local,
          mlflow.tracing.reset, mlflow.tracing.disable, mlflow.tracing.enable, trace_disabled,
          trace_destination, _initialize_tracer_provider, _get_span_processors,
          _TracerProviderWrapper, OtelSpanProcessor, BaseMlflowSpanProcessor, OtelMetricsMixin,
          _setup_metrics_if_necessary, mlflow.trace.span.duration,
          "Overriding of current MeterProvider is not allowed",
          "A shutdown MeterProvider can not provide a Meter", MeterProvider, NoOpMeterProvider,
          PeriodicExportingMetricReader, set_meter_provider, get_meter_provider,
          metric reader thread, span processor thread, thread leak, BatchSpanProcessor,
          x-mlflow-experiment-id, x-mlflow-run-id, reset_tracing, metric_reader fixture,
          opentelemetry-exporter-otlp-proto-grpc, "gRPC OTLP exporter is not available"
verified: 2026-08-22 by lucas. Source claims are `git show v3.15.1:<file>` quotations, each with
          the command inlined. Behavioural claims were measured in Docker on Linux/glibc/x86_64,
          Python 3.12, opentelemetry-sdk 1.44.0, http/protobuf, on 2026-08-19 (release 3.15.1)
          and 2026-08-22 (master at 627d1ebd0); each carries its own date. No cloud account and
          no MLflow server are needed to re-derive any of it.
-->

# MLflow tracing and the OpenTelemetry SDK: two providers, one of them shared

**Scope.** How MLflow 3.x decides where a span goes, where the span-duration metric goes, and what
it does to the OpenTelemetry global state of the process it is running in. This is the entry to
read before answering anything labelled `area/tracing` that mentions OTLP, a collector, an
exporter, a thread count or a MeterProvider. It is a mechanism entry, not a tutorial: the API
surface is in MLflow's docs, and none of what follows is.

Why it exists at all: tracing postdates the training cutoff entirely, it is roughly half of the
issue tracker's traffic, and its interaction with a host application's own OpenTelemetry setup is
the part nobody can guess. Worked tickets: #24209 and its fix #24267 (span side), #25206 and its
PR #25258 (metrics side, open as of 2026-08-22).

---

## 1. The asymmetry that explains most surprises

MLflow keeps **its own tracer provider** and **shares the process-global meter provider**.

The tracer side is deliberate and documented in the code:

```bash
git show v3.15.1:mlflow/tracing/provider.py | sed -n '/class _TracerProviderWrapper/,/def __init__/p'
#   "MLflow uses an isolated tracer provider instance managed by MLflow. This is the default
#    behavior such that MLflow does not break an environment where MLflow and OpenTelemetry SDK
#    are used in different purposes."
```

The metrics side has no equivalent. `OtelMetricsMixin._setup_metrics_if_necessary` calls
`opentelemetry.metrics.set_meter_provider()` and then `metrics.get_meter("mlflow.tracing")`, both
of which act on the OTel **global** singleton:

```bash
git show v3.15.1:mlflow/tracing/processor/otel_metrics_mixin.py | sed -n '60,80p'
```

Consequences, all measured (2026-08-19, release 3.15.1, and confirmed 2026-08-22 at `627d1ebd0`):

| the application has... | spans | `mlflow.trace.span.duration` |
|---|---|---|
| no OpenTelemetry of its own | MLflow's isolated provider | MLflow's provider, exported to `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` |
| its own global `TracerProvider` | unaffected, MLflow still uses its own | — |
| its own global `MeterProvider` | unaffected | **the application's readers.** MLflow's provider is refused on the first call and its OTLP metrics exporter is never used: 0 POSTs at the configured endpoint over a 6 s window at a 1 s interval |

The last row is the one that costs people time: the endpoint is configured, the docs say metrics
go there, and nothing arrives, with nothing logged. It is not a bug in the sense of a crash, it is
the OTel set-once rule meeting a component that does not check.

### The naming trap

`MLFLOW_USE_DEFAULT_TRACER_PROVIDER` (default `True`) means **use MLflow's own isolated
provider**, not "use OTel's default global provider". Setting it to `False` is what makes MLflow
share the global tracer provider, which is what you want when you need MLflow spans and
auto-instrumentation spans in one trace.

```bash
git show v3.15.1:mlflow/environment_variables.py | grep -n 'MLFLOW_USE_DEFAULT_TRACER_PROVIDER' -B 4
```

In that shared mode MLflow *adds its processors to* an existing provider rather than replacing it,
and it tracks initialization with its own `Once` flag rather than OTel's, precisely so that a
library that got there first is not clobbered (`_initialize_tracer_provider`, same file).

---

## 2. Where a span actually goes

The whole routing decision is one function, and reading it settles most "my traces went to the
wrong place" questions without running anything:

```bash
git show v3.15.1:mlflow/tracing/provider.py | sed -n '/^def _get_span_processors/,/^def /p'
```

Precedence, highest first:

1. **A destination set with `mlflow.tracing.set_destination(...)`** (or a Unity Catalog location
   resolved from the active experiment). This wins outright: OTLP is skipped entirely *unless*
   `MLFLOW_TRACE_ENABLE_OTLP_DUAL_EXPORT=true` (default `False`).
2. **OTLP**, if `should_use_otlp_exporter()` is true, which needs both a traces endpoint and
   `MLFLOW_ENABLE_OTLP_EXPORTER` (default `True`).
3. **The default MLflow processor** for the tracking URI (or the inference-table processor inside
   Databricks model serving).

Two endpoint rules from `mlflow/tracing/utils/otlp.py`, worth knowing because they make one
variable behave like two:

* `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` is used as-is; otherwise the generic
  `OTEL_EXPORTER_OTLP_ENDPOINT` gets `/v1/traces` appended. Same shape for metrics with
  `/v1/metrics`.
* So **the generic variable turns on both signals at once**, and that flips step 2 above. Setting
  only `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` leaves spans with MLflow while still enabling the
  metrics path. This is the single most useful knob when reproducing a metrics-side bug without
  redirecting the traces too.

Measured consequence for the per-span form (2026-08-19, 21 traces each): with the generic
endpoint set, `mlflow.start_span(..., trace_destination=MlflowExperimentLocation(...))` routed
**0 of 21** traces to the experiments addressed, silently, because the OTLP processor is what is
installed; with only the metrics endpoint set, **21 of 21** arrived.

### Protocol default is grpc

`_get_otlp_protocol` and `_get_otlp_metrics_protocol` default to **`grpc`**, not http/protobuf:

```bash
git show v3.15.1:mlflow/tracing/utils/otlp.py | sed -n '/def _get_otlp_protocol/,/^def /p'
```

So an endpoint configured without a protocol needs `opentelemetry-exporter-otlp-proto-grpc`
installed, and raises `MlflowException` with *"gRPC OTLP exporter is not available"*
(`RESOURCE_DOES_NOT_EXIST`) if it is not. A reproduction environment should install both exporter
packages and set the protocol explicitly.

### MLflow is also an OTLP receiver

`build_otlp_headers` stamps `x-mlflow-experiment-id` (and `x-mlflow-run-id`) on outgoing OTLP
requests and adds `Authorization` from the resolved MLflow credentials, basic or bearer; the
server side decompresses gzip/deflate OTLP bodies in `decompress_otlp_body`. So "export to an
OTel collector" and "export to an MLflow tracking server over OTLP" are the same code path with a
different URL, and an auth failure there looks like a tracing failure.

---

## 3. Where the metric goes, and what it is labelled with

`mlflow.trace.span.duration` (unit `ms`) is recorded by `OtelMetricsMixin`, which **both**
processor families inherit, so metrics are not tied to the OTLP path:

```bash
git grep -n 'OtelMetricsMixin' v3.15.1 -- 'mlflow/*'
#   base_mlflow.py:176  class BaseMlflowSpanProcessor(OtelMetricsMixin, SimpleSpanProcessor)
#   otel.py:20          class OtelSpanProcessor(OtelMetricsMixin, BatchSpanProcessor)
```

Each processor is constructed with `export_metrics=should_export_otlp_metrics()`, i.e. gated only
on a metrics endpoint being configured, and in dual-export mode only one of the two records, to
avoid double counting.

**Cardinality trap.** The attribute set is `root`, `span_type`, `span_status`, `experiment_id`
*plus every trace tag as `tags.<key>` and every trace metadata key as `metadata.<key>`*:

```bash
git show v3.15.1:mlflow/tracing/processor/otel_metrics_mixin.py | sed -n '/attributes = {/,/self._duration_histogram.record/p'
```

Any per-request tag (session id, user id, request id) therefore becomes a metric label, and on a
Prometheus-style backend that is unbounded cardinality generated by application code that looks
harmless. Worth flagging on any ticket where someone tags traces per request and then asks about
collector memory.

---

## 4. The rebuild path, and what is cleaned up

Four public entry points rebuild the span processors, all of them funnelling into
`_initialize_tracer_provider()` (line numbers at v3.15.1): `set_destination` L542, with
`context_local=True` on the same call, `disable()` L942, `enable()` L983, `reset()` L1058. Anything
that fires per request in a multi-tenant service is calling one of these repeatedly.

What is cleaned up on a rebuild, and what is not:

* **Span processors: retired since 3.15.0.** `_TracerProviderWrapper.set()` calls
  `_retire_current_batch_processors()`, which flushes and shuts down the outgoing
  `BaseMlflowSpanProcessor` and `OtelSpanProcessor` instances and deliberately leaves external
  processors on a shared provider alone. That is the fix for #24209, shipped in PR #24267.
  Measured: span processor threads stay at 1 across 20 rebuilds.
* **The meter provider: not retired, and until #25258 not reused either.** Each rebuilt processor
  is a fresh mixin whose `self._duration_histogram` is `None`, so the per-instance guard cannot
  fire across rebuilds, and each one built a `MeterProvider` plus a
  `PeriodicExportingMetricReader`. Only the first is ever installed. Measured on 3.15.1 and at
  `627d1ebd0`: **21 providers and 21 reader threads after 20 iterations**, identically for all
  four entry points. One thread per request until the container dies. That is issue #25206.
* `trace_disabled` is the exception that proves the rule: it uses `_swap_raw`, which installs a
  provider *without* retiring the outgoing one, precisely so the batch thread is not rebuilt on
  restore. It is serialized by `_trace_disabled_lock` with a depth counter, because overlapping
  frames used to leave a NoOp provider installed permanently (#24209 again).

### Why the span-side fix cannot be mirrored for metrics

Shutting down the retired `MeterProvider`, the move that works for span processors, breaks metrics
for the rest of the process. Measured 2026-08-19 in pure OpenTelemetry, no MLflow: after
`provider_1.shutdown()`, `set_meter_provider(provider_2)` is still refused (*"Overriding of
current MeterProvider is not allowed"*), the global provider is still the shut-down one, and it
answers `get_meter()` with *"A shutdown MeterProvider can not provide a Meter"*. Nothing recorded
afterwards is exported. The first provider MLflow builds **is** the installed one, so retiring it
on the next rebuild would silence metrics.

The shape that does work, and what #25258 proposes (open as of 2026-08-22, not merged), is to
not build one at all when an SDK provider is already installed, and to shut ours down if it was
refused anyway.

---

## 5. OpenTelemetry global-state facts that bite here

Not MLflow-specific, but each one has produced a wrong conclusion in this codebase at least once
(all measured against `opentelemetry-sdk` 1.44.0):

* **`set_meter_provider()` is set-once and silent about it** beyond one warning log. There is no
  supported uninstall. Tests that install one leak it into every later test in the session.
* **`NoOpMeterProvider` is not an `opentelemetry.sdk.metrics.MeterProvider`.** Any "is one already
  installed?" check written as `isinstance(..., MeterProvider)` treats an application that
  deliberately switched metrics *off* as an empty slot. Measured: that case leaked one provider
  per call until the refusal was also handled.
* **Registering the same instrument twice is deduplicated, quietly.** Reusing an installed
  provider across rebuilds calls `Meter.create_histogram` once per rebuild, but 20 calls produced
  exactly **one** live instrument and one per-reader view-storage entry, with no duplicate-
  instrument warning (measured 2026-08-22 with a call counter as the positive control). So
  provider reuse does not trade a thread leak for an instrument leak.
* **A `PeriodicExportingMetricReader` thread is named after its class**, which is what makes the
  observation recipe below possible without a profiler.

---

## 6. Observing any of this in ten lines

No debugger, no profiler; a gc scan and the thread table are enough.

```python
import gc, threading
from opentelemetry.sdk.metrics import MeterProvider

def counts():
    gc.collect()
    return {
        "meter_providers": sum(1 for o in gc.get_objects() if isinstance(o, MeterProvider)),
        "reader_threads": sum(
            1 for t in threading.enumerate() if "PeriodicExportingMetricReader" in t.name
        ),
        "span_proc_threads": sum(
            1
            for t in threading.enumerate()
            if "SpanRecordProcessor" in t.name or "BatchSpanProcessor" in t.name
        ),
    }
```

Call it after each iteration of whatever rebuilds the provider. A growing `reader_threads` with a
flat `span_proc_threads` is the #25206 signature. To see whether the configured endpoint is
actually reached, point `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` at a `ThreadingHTTPServer` on
loopback and set `OTEL_METRIC_EXPORT_INTERVAL=1000`; counting POSTs is the only way to separate
"the exporter exists" from "the exporter is the installed one".

---

## 7. Testing MLflow tracing, in MLflow's own suite

Three traps, all found the hard way, all still true at `627d1ebd0`:

* **`tests/conftest.py::reset_tracing` resets the tracer provider between tests, not the meter
  provider.** So the second test in a session to install a `MeterProvider` is silently refused and
  reads the first test's, by then shut down. Any metrics test that is not first in its session is
  testing the wrong object. There is no public uninstall; the working reset is
  `opentelemetry.metrics._internal._METER_PROVIDER_SET_ONCE._done = False` plus
  `_METER_PROVIDER = None`, which is ugly enough that it belongs in a fixture and not in a test.
* **The `metric_reader` fixture in `tests/tracing/processor/test_otel_metrics.py` installs a
  provider before MLflow traces anything.** Every unmocked test in that file therefore exercises
  the "somebody else owns the provider" branch, never the branch where MLflow installs the first
  provider itself, which is the configuration in the bug report. A fixture is a configuration
  choice, and here it chose the case that hid the defect for a release.
* **Patching a class that the code under test also uses in an `isinstance` check makes the check
  fail, and the assertion pass for the wrong reason.** `mock.patch(...MeterProvider)` to count
  constructions breaks `isinstance(get_meter_provider(), MeterProvider)` in the same function, so
  a "was not called" assertion goes green while nothing was exercised. Patch the *reader* class
  with `wraps=`, or assert on the symptom (provider identity and thread counts) instead.

---

## 8. Not verified here

Say so rather than extrapolating:

* **grpc transport.** Everything above was measured over http/protobuf. The routing and provider
  logic is transport-independent by inspection, but no grpc run was made.
* **Dual export** (`MLFLOW_TRACE_ENABLE_OTLP_DUAL_EXPORT=true`) is read from source only; no run.
* **Databricks paths** (UC table destinations, model-serving inference tables) are unreachable
  from here and are described only as branches of `_get_span_processors`.
* **An observation not yet filed anywhere** (2026-08-19, unconfirmed against master): on 3.15.1 a
  trace addressed to a **deleted** experiment is accepted through OTLP (`POST /v1/traces` → 200)
  while the v3 trace API refuses it (400); on 2.21.3 it is not accepted. Treat as a lead, not a
  fact about current master.
