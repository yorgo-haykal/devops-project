# DevOps Lab 4 — Observability, Alerting and Incident Response

## Part 1 — Instrument the Application

### 1.2 Test endpoints (`/slow` and `/error`)

Evidence: [evidence/lab4/lab4-part1-1.2.txt](../evidence/lab4/lab4-part1-1.2.txt)

### 1.3 Metrics endpoint (`/metrics`)

Evidence: [evidence/lab4/lab4-part1-1.3.txt](../evidence/lab4/lab4-part1-1.3.txt)

### 1.4 Build, tag and push

Local Docker build and run evidence: [evidence/lab4/lab4-part1-1.4.txt](../evidence/lab4/lab4-part1-1.4.txt)

### Q1. Why is it a problem to use a user ID or a full URL containing IDs as a metric label?

Later on in the lab we will need to use Prometheus in order to monitor. A label such as a user ID or a URL like `/users/48291` has an unbounded number of possible values, so each new user or each new ID creates a new series. This is a cardinality explosion.

The consequences are:
- Prometheus memory usage grows with the number of active series, which can lead to the process being killed (OOM).
- Queries become slow and dashboards may time out.
- Disk usage grows for nothing.
- It can be a security hazars (anyone calling random URLs can create series at will and overload prometheus).


### Q2. Why log to stdout in JSON rather than to a file in plain text?

JSON is preferred over plain text because it is structured:
- Each line is one event with named fields (`timestamp`, `level`, `method`, `path`, `status`, `duration_ms`), so log tools can parse it without fragile regular expressions.
- Logs can be filtered and aggregated by field more easily.
- Fields can be correlated with metrics and with other services, and new fields can be added without breaking existing parsers.

The evidence in `lab4-part1-1.2.txt` and `lab4-part1-1.4.txt` shows one JSON line per request written to stdout, both locally and inside the Docker container.
