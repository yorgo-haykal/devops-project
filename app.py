import json
import random
import sys
import time
from datetime import UTC, datetime

from flask import Flask, Response, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status"],
)
HTTP_DURATION = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "route"],
    buckets=[0.05, 0.1, 0.3, 0.5, 1, 2],
)


def _route_label():
    return request.url_rule.rule if request.url_rule else "unknown"


@app.before_request
def start_timer():
    request._start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    route = _route_label()
    duration = time.perf_counter() - request._start_time

    HTTP_REQUESTS.labels(request.method, route, response.status_code).inc()
    HTTP_DURATION.labels(request.method, route).observe(duration)
    response.headers["X-Response-Time"] = f"{duration:.3f}s"

    print(
        json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": "error" if response.status_code >= 500 else "info",
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        ),
        file=sys.stdout,
        flush=True,
    )
    return response


@app.get("/health")
def health():
    return "OK", 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/slow")
def slow():
    time.sleep(random.uniform(0, 2))
    return "slow OK", 200


@app.get("/error")
def error():
    if random.random() < 0.3:
        return "internal error", 500
    return "error OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
