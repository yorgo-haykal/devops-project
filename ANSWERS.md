# DevOps Lab - Session 2: Answers

## Question 1
What is the role of a namespace? Does it provide strong security isolation by itself?

A namespace is a logical partition inside a Kubernetes cluster. It groups resources (pods, services, configmaps, etc.) so that different teams or environments can share the same cluster without name collisions. For example, a pod called `devops-project` can exist in both the `dev` and `prod` namespaces independently.

However, namespaces do not provide strong security isolation by themselves. By default, pods in one namespace can reach pods in another namespace over the network, and a user with cluster-wide permissions can access any namespace. To enforce real isolation you need additional mechanisms: NetworkPolicies to restrict cross-namespace traffic, RBAC to limit what each user or service account can do per namespace, and ResourceQuotas to prevent one namespace from starving others.

---

## Question 2
Why does Kubernetes recreate the deleted pod? Which component is responsible?

The Deployment controller is responsible. A Deployment declares a desired state, for example 3 replicas. When we manually delete a pod, the actual state drops to 2 replicas. The Deployment controller's reconciliation loop detects the mismatch and immediately creates a new pod to bring the count back to 3.  

---

## Question 3
What is the difference between a readiness and a liveness probe? What happens to traffic when readiness fails?

- Readiness probe: checks if the pod is ready to serve traffic. If it fails, the pod is removed from the Service's endpoints. This is useful during startup or when a pod is temporarily overloaded.

- Liveness probe: checks if the pod is still alive. If it fails, Kubernetes restarts the container. This catches situations where the process is stuck or deadlocked.

When the readiness probe fails, the pod's IP is removed from the Service's endpoint list, so no new traffic is routed to it. Existing connections may still complete depending on the protocol. Once the readiness probe succeeds again, the pod is re-added to the endpoint list.

---

## Question 4
Is a Kubernetes Secret encrypted by default? How would you improve this?

No. By default, Kubernetes Secrets are only base64-encoded, not encrypted. They are stored in etcd in plaintext (base64 is encoding, not encryption). Anyone with access to etcd or the right RBAC permissions can read them.

To improve this:
- Enable encryption at rest in etcd by configuring an `EncryptionConfiguration` on the API server, using a provider like `aescbc`, `secretbox`, or a KMS plugin.
- Use an external secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) with an operator like External Secrets Operator to inject secrets at runtime.
- Restrict RBAC so that only the service accounts and users that truly need access can read Secrets.
- Enable audit logging to track who accesses Secrets and when.

---

## Question 5
How does this pattern help with hybrid/multi-cloud deployments? What would differ between a real on-prem cluster and a cloud cluster?

The base + overlays pattern (Kustomize) lets you keep a single set of manifests for the application while customizing per-environment differences in overlays. The base defines what the app needs (containers, ports, probes), and each overlay adjusts for the target cluster (replica count, image registry, resource limits, labels).

In a real hybrid/multi-cloud setup, the differences between on-prem and cloud would include:
- **StorageClass**: on-prem might use NFS or Ceph; cloud uses EBS, Persistent Disks, etc.
- Ingress/LoadBalancer: cloud providers offer native LoadBalancer services; on-prem typically uses MetalLB or NodePort with an external load balancer.
- Image registry: on-prem might use a private Harbor registry; cloud uses ECR, GCR, or GHCR.
- Resource limits: cloud nodes may have different CPU/memory profiles.
- Node selectors/tolerations: to target specific hardware or availability zones.

Each of these differences lives cleanly in its own overlay, while the core application definition stays the same.

---

## Question 6
Why did the broken rollout not take down the application?

Kubernetes uses a rolling update strategy by default. It creates new pods with the updated image before terminating old ones. The new pods must pass their readiness probe before old pods are removed.

When the new image is broken (e.g., it doesn't exist or crashes), the new pods never become ready. Kubernetes stops rolling out further and keeps the old, healthy pods running. The `maxUnavailable` setting (default 25%) ensures that a minimum number of working pods is always available. So the broken deployment stalls partway through without affecting the existing healthy pods that are still serving traffic.

---

## Question 7
Starting from a pod running in production, how can you find the commit, the reviewer and the pipeline run that produced it?

1. Get the image tag from the pod: `kubectl get pod <name> -n prod -o jsonpath='{.spec.containers[0].image}'`. If the tag is a commit SHA (as in our CI pipeline), you already have the commit.
2. Check annotations on the Deployment: `kubectl describe deployment devops-project -n prod`. Annotations like `git-commit`, `owner`, and `ticket` give you the commit SHA, the responsible team, and the issue reference.
3. From the commit SHA go to GitHub: find the commit, see which PR it was part of (and who reviewed/approved it), and find the associated CI pipeline run in the Actions tab.
4. From the pipeline run URL (if stored as an annotation), go directly to the CI/CD run to see build logs, test results, and the full audit trail.

This is why annotations and proper image tagging (with commit SHAs instead of `latest`) are essential for production traceability.

---

## Question 8
Why is manual `kubectl edit` in production a traceability risk?

`kubectl edit` modifies a resource directly on the cluster without leaving a trace in version control. This means:
- **No git history**: the change is not recorded in any repository, so you cannot see who changed what, when, or why.
- **No code review**: the change bypasses the pull request and review process, so no one else validates it.
- **No CI/CD pipeline**: tests, linting, and security checks are skipped entirely.
- **Drift from source of truth**: the live cluster state diverges from the manifests in git, making future deployments unpredictable — the next `kubectl apply` from git could overwrite or conflict with the manual edit.
- **No rollback path**: without a commit to revert to, rolling back is guesswork.

The proper approach is GitOps: all changes go through git (commit, PR, review, merge), and a pipeline or operator (like ArgoCD or Flux) applies them to the cluster. This ensures every change is auditable, reviewable, and reversible.
