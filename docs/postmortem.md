# Postmortem — Failed Kubernetes Deployment

## 1. Incident Summary

**Date:** November 24, 2026  
**Environment:** Local Kubernetes cluster (`kind`), namespace `dev`  
**Application:** `myapp` (Flask)  
**Incident type:** Failed deployment caused by an incorrect readiness probe  
**Status:** Resolved

During a controlled incident simulation, the application's readiness probe was intentionally changed from `/health` to `/health-broken`.

The new pod started successfully but failed its readiness checks because the configured endpoint returned HTTP 404. Kubernetes prevented the new pod from receiving traffic, and the rolling update could not complete.

## 2. Impact

- One newly created pod remained `0/1 Ready`.
- The deployment rollout was blocked.
- Three existing healthy pods remained available.
- No complete service outage was observed.
- The incident affected the local development environment only.

## 3. Timeline (UTC)

*Approximate times based on the recorded terminal observations.*

| Time (UTC) | Event |
|---|---|
| 12:26 | Incorrect readiness probe deployed using `kubectl patch`. |
| 12:27 | New pod observed as `0/1 Ready`; rollout timed out. |
| 12:28 | Kubernetes events confirmed readiness probe failures with HTTP 404. |
| 12:29 | Rollback initiated to known healthy revision 10. |
| 12:29 | Rollout completed successfully; three healthy pods confirmed. |
| 12:30 | Readiness probe verified as `/health`. |

## 4. Root Cause

The Deployment was configured to check `/health-broken`, an endpoint that does not exist in the Flask application.

The readiness probe received HTTP 404 responses, preventing the new pod from becoming Ready.

**Contributing factor:** The deliberately incorrect probe configuration was applied without a prior validation step.

## 5. Detection and Diagnosis

The incident was identified using:

- `kubectl get pods -n dev`
- `kubectl rollout status deployment/myapp -n dev --timeout=15s`
- `kubectl describe pod`
- `kubectl rollout history deployment/myapp -n dev`

Kubernetes events provided the decisive diagnostic evidence:

`Readiness probe failed: HTTP probe failed with statuscode: 404`

## 6. Mitigation and Recovery

The team restored the previously verified healthy deployment revision:

```bash
kubectl rollout undo deployment/myapp -n dev --to-revision=10
```

Recovery was verified using:

```bash
kubectl rollout status deployment/myapp -n dev --timeout=120s
kubectl get pods -n dev
```

All three healthy replicas were available, and the readiness probe path was restored to `/health`.

## 7. What Went Well

- Kubernetes readiness probes prevented the unhealthy new pod from receiving traffic.
- Existing healthy replicas remained available during the failed rollout.
- Kubernetes events clearly identified the problem.
- Deployment revision history enabled a quick rollback.

## 8. What Could Be Improved

- Deployment configuration should be validated before rollout.
- Automated smoke tests should verify health endpoints.
- CI/CD should detect failed deployments and stop promotion.
- Monitoring should distinguish application HTTP errors from deployment readiness failures.

## 9. Preventive Action Items

| Action | Owner | Target |
|---|---|---|
| Add automated health endpoint checks | DevOps team | Next CI/CD improvement |
| Validate readiness probe paths before deployment | DevOps team | Next deployment update |
| Add rollout verification to the deployment pipeline | DevOps team | Next CI/CD improvement |
| Document recovery procedures in the runbook | DevOps team | Lab 4 |

## 10. Lessons Learned

A container being `Running` does not mean it is ready to serve requests.

Readiness probes and rolling updates can prevent a faulty deployment from causing a complete outage. However, automated deployment validation and rollback procedures remain essential for reliable continuous delivery.

This postmortem is blameless and focuses on improving the system rather than assigning individual responsibility.