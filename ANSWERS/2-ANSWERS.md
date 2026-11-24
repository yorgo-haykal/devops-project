# Lab2 Questions & Answers

## Question 1 — Kubernetes Namespaces

**What is the role of a namespace in Kubernetes? Does it provide strong security isolation by itself?**

A namespace is a logical partition used to organize Kubernetes resources within a cluster. It allows teams to separate environments such as development, staging, and production.

However, namespaces do not provide strong security isolation by themselves. Additional mechanisms such as RBAC, NetworkPolicies, and resource quotas are required to control access, network communication, and resource consumption.


## Question 2 — Pod Recreation

**Why does Kubernetes recreate a deleted pod? Which component is responsible?**

Kubernetes uses controllers to maintain the desired state of an application.

When a Pod managed by a Deployment is deleted, the ReplicaSet controller detects that the actual number of Pods is lower than the desired replica count and creates a replacement. The scheduler then assigns the new Pod to a suitable node.

In our experiment, Kubernetes automatically restored the desired number of replicas after we deleted a Pod.


## Question 3 — Readiness and Liveness Probes

**What is the difference between readiness and liveness probes? What happens to traffic when readiness fails?**

A readiness probe determines whether a container is ready to receive traffic. When it fails, Kubernetes marks the Pod as not ready and removes it from the matching Service's ready endpoints.

A liveness probe determines whether the container is still healthy enough to continue running. When it repeatedly fails, Kubernetes restarts the container according to the Pod's restart policy.

We tested a broken readiness endpoint (`/wrong-health`) and observed an HTTP 404 readiness failure while the existing healthy Pods remained available.


## Question 4 — Kubernetes Secrets

**Are Kubernetes Secrets encrypted by default?**

Kubernetes Secrets are not necessarily encrypted at rest by default. Their values are base64-encoded in manifests, but base64 is an encoding mechanism, not encryption.

To protect sensitive information, administrators should enable encryption at rest for Secret data, restrict access using RBAC, and consider external secret-management solutions.

In our lab, we used a dummy API key (`changeme`) only for demonstration purposes.


## Question 5 — Kustomize and Hybrid/Multi-cloud Deployments

**How does this pattern help with hybrid/multi-cloud deployments? What would differ between a real on-prem cluster and a cloud cluster?**

Kustomize allows us to reuse a common set of Kubernetes manifests while customizing configuration for each environment through overlays.

This reduces duplication and makes deployments more consistent across development, staging, production, on-premises clusters, and cloud platforms.

In a real hybrid or multi-cloud setup, overlays might differ in replica counts, resource allocations, storage classes, ingress configuration, load balancers, network policies, and infrastructure-specific settings.

For our lab, we deployed the same container image with three replicas in `dev`, three in `staging`, and five in `prod`.

Evidence:
- [evidence/lab2/lab2-part4-4.4-dev.txt](../evidence/lab2/lab2-part4-4.4-dev.txt)
- [evidence/lab2/lab2-part4-4.4-staging.txt](../evidence/lab2/lab2-part4-4.4-staging.txt)
- [evidence/lab2/lab2-part4-4.4-prod.txt](../evidence/lab2/lab2-part4-4.4-prod.txt)

## Question 6 — Failed Rolling Update

**Why did the broken rollout not take down the application?**

Kubernetes uses the RollingUpdate strategy to replace Pods progressively while maintaining application availability.

Our Deployment had three replicas, `maxSurge: 25%`, and `maxUnavailable: 25%`. With three replicas, these settings allow one additional Pod and zero unavailable Pods during the rollout.

When we deployed an invalid image tag, the new Pod entered `ErrImagePull`, but the three existing healthy Pods continued running.

Kubernetes did not automatically roll back. We restored the previous configuration using `kubectl rollout undo`, and verified that the original image was running again.

Evidence:
- [evidence/lab2/lab2-part5-5.1-image-update.txt](../evidence/lab2/lab2-part5-5.1-image-update.txt)
- [evidence/lab2/lab2-part5-5.2-rollout.txt](../evidence/lab2/lab2-part5-5.2-rollout.txt)
- [evidence/lab2/lab2-part5-5.2-status.txt](../evidence/lab2/lab2-part5-5.2-status.txt)
- [evidence/lab2/lab2-part5-5.3-rollback-events.txt](../evidence/lab2/lab2-part5-5.3-rollback-events.txt)
- [evidence/lab2/lab2-part5-5.4-rollout-history.txt](../evidence/lab2/lab2-part5-5.4-rollout-history.txt)

## Question 7 — Deployment Traceability

**Starting from a pod running in production, how can you find the commit, the reviewer and the pipeline run that produced it?**

First, inspect the Pod to identify its owning ReplicaSet and Deployment. Then inspect the Deployment's annotations and container image.

In our lab, the production Deployment includes:

- Git commit: `e2aafa2142832bec55000f5885e0289a58476e97`
- Pipeline run: https://github.com/yorgo-haykal/devops-project/actions/runs/44078797914
- Owner: `devops-team`
- Ticket: `LAB2-001`

The Git commit identifies the deployed source revision. The GitHub Actions run provides evidence of the successful build and publication pipeline.

To identify the reviewer, follow the commit to its associated GitHub Pull Request and inspect its reviews and approval history. Reviewer information is not automatically stored in the Kubernetes Deployment.

RBAC evidence (`kubectl auth can-i` results): [evidence/lab2/lab2-part6-6.3-rbac.txt](../evidence/lab2/lab2-part6-6.3-rbac.txt)

## Question 8 — Manual Changes in Production

**Why is manual `kubectl edit` in production a traceability risk?**

Manual `kubectl edit` changes the live Kubernetes configuration without necessarily updating the version-controlled manifests.

This creates configuration drift between the Git repository and the running cluster. The change may also bypass code review, automated tests, and the CI/CD approval process.

As a result, it becomes harder to determine who changed the configuration, why it was changed, and how to reproduce or roll back the modification.

A safer approach is to manage production changes through version-controlled manifests, reviewed Pull Requests, and controlled deployment pipelines.
