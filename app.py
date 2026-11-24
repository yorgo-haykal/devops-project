
from flask import Flask, Response, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import json
import logging
import random
import time
from datetime import datetime, timezone

app = Flask(__name__)

# Prometheus metrics
http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status"]
)

http_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"]
)

# Structured JSON logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

@app.before_request
def start_timer():
    request.start_time = datetime.now(timezone.utc)

@app.after_request
def log_request(response):
    duration = (
        datetime.now(timezone.utc) - request.start_time
    ).total_seconds()

    route = request.url_rule.rule if request.url_rule else request.path

    http_requests.labels(
        request.method, route, response.status_code
    ).inc()

    http_duration.labels(
        request.method, route
    ).observe(duration)

    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "error" if response.status_code >= 500 else "info",
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_seconds": duration
    }

    logger.info(json.dumps(log_data))

    return response

@app.get("/health")
def health():
    return "OK", 200

@app.get("/slow")
def slow():
    delay = random.uniform(0, 2)
    time.sleep(delay)
    return f"Response after {delay:.2f} seconds", 200

@app.get("/error")
def error():
    if random.random() < 0.3:
        return "Internal Server Error", 500
    return "OK", 200

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)