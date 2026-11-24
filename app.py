import json
import random
import sys
import time
from datetime import UTC, datetime

from flask import Flask, g, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

http_requests = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status"]
)

http_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "route"],
    buckets=[0.05, 0.1, 0.3, 0.5, 1, 2, float("inf")]
)

@app.after_request
def record_metrics(response):
    route = request.url_rule.rule if request.url_rule else "unmatched"

    if route != "/metrics":
        http_requests.labels(
            method=request.method,
            route=route,
            status=str(response.status_code)
        ).inc()

        duration = time.perf_counter() - g.start_time

        http_duration.labels(
            method=request.method,
            route=route
        ).observe(duration)

        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": "error" if response.status_code >= 500 else "info",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_seconds": round(duration, 6)
        }

        print(json.dumps(log_entry), file=sys.stdout, flush=True)

    return response

@app.before_request
def start_timer():
    g.start_time = time.perf_counter()

@app.get("/health")
def health():
    return "OK", 200

@app.get("/slow")
def slow():
    delay = random.uniform(0, 2)
    time.sleep(delay)
    return "Slow request completed", 200


@app.get("/error")
def error():
    if random.random() < 0.3:
        return "Internal Server Error", 500

    return "OK", 200


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
