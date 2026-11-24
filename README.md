# DevOps Lab Session 4: Observability, Alerting and Incident Response

## Part 1: Instrument the Application

### 1.3 Run locally, call the endpoints, then check curl localhost:3000/metrics.
```bash
Invoke-WebRequest http://localhost:5000/health                              
Invoke-WebRequest http://localhost:5000/slow                                                                                                                            
Invoke-WebRequest http://localhost:5000/error                                                                                                                           
                                                                                                                                                                        
StatusCode        : 200
StatusDescription : OK
[...]

StatusCode        : 200
StatusDescription : OK
[...]

StatusCode        : 200
StatusDescription : OK

```
```bash
curl.exe http://localhost:5000/metrics
[...]
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/slow",status="200"} 3.0
http_requests_total{method="GET",route="/error",status="500"} 21.0
http_requests_total{method="GET",route="/error",status="200"} 40.0
http_requests_total{method="GET",route="/health",status="200"} 1.0
http_requests_total{method="GET",route="/metrics",status="200"} 1.0
[...]
# HELP http_request_duration_seconds HTTP request duration in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_count{method="GET",route="/slow"} 3.0
http_request_duration_seconds_sum{method="GET",route="/slow"} 3.27635
```

### 1.4 Build, tag with the commit SHA and push through your Session 1 pipeline.


### Question 1. Why is it a problem to use a user ID or a full URL containing IDs as a metric label?
### Question 2. Why log to stdout in JSON rather than to a file in plain text?



```bash
```

