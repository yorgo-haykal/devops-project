# Runbook — HighErrorRate

## Alert
More than 10% HTTP 5xx errors for 2 minutes.

## 1. Symptoms
- Application errors.
- High HTTP 5xx rate.

## 2. Quick checks
```bash
kubectl get pods -n pr-43
kubectl get deployment myapp -n pr-43
kubectl logs deployment/myapp -n pr-43 --tail=100
```

Check Prometheus: http://localhost:9090/alerts

## 3. Mitigation
If a recent deployment caused the issue:
```bash
kubectl rollout undo deployment/myapp -n pr-43
kubectl rollout status deployment/myapp -n pr-43
```

## 4. Verify
- Pods are healthy.
- Error rate is below 10%.
- Alert is inactive.