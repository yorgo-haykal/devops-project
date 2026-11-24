
# Runbook — HighErrorRate

## Alert
- Name: HighErrorRate
- Severity: critical
- Condition: More than 10% HTTP 5xx errors for 2 minutes
- Environment: Kubernetes namespace `dev`
- Application: `myapp`

## 1. Identify the incident

Check the alert in Prometheus:
http://localhost:9090/alerts

Check the Grafana dashboard:
http://localhost:3001

Look at traffic, HTTP 5xx error rate, p95 latency and memory usage.

## 2. Check Kubernetes

```bash
kubectl get pods -n dev
kubectl get deployment myapp -n dev
kubectl describe deployment myapp -n dev
```

Look for failing pods, restarts or deployment issues.

## 3. Inspect application logs

```bash
kubectl logs deployment/myapp -n dev --tail=100 --prefix=true
```

Look for HTTP 500 responses and application errors.

## 4. Mitigate the incident

If the incident was caused by a recent deployment:

```bash
kubectl rollout history deployment/myapp -n dev
kubectl rollout undo deployment/myapp -n dev
kubectl rollout status deployment/myapp -n dev
```

Only roll back after confirming that a previous healthy revision exists.

## 5. Verify recovery

- Confirm pods are healthy.
- Check that HTTP 5xx error rate drops below 10%.
- Verify that HighErrorRate returns to Inactive.
- Check the Grafana dashboard.

## 6. Escalation

If the issue persists, contact the application team and investigate the root cause.

## 7. Postmortem

Document the incident timeline, impact, root cause, mitigation and preventive actions in `docs/postmortem.md`.
