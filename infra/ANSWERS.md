
# DevOps Lab 3 — Terraform, Environments and Ephemeral Previews

## Part 1 — First Terraform Configuration

### Q1. What happens if a Docker container is manually deleted outside Terraform?

Terraform detects infrastructure drift during the next `terraform plan`.

After refreshing its knowledge of the actual infrastructure, Terraform notices that the container defined in the configuration no longer exists and proposes recreating it.

In our lab, we manually deleted the `tf-web` container. Terraform detected the missing resource and proposed creating it again.

This demonstrates Terraform's declarative approach: it attempts to reconcile the actual infrastructure with the desired configuration.

### Q2. Why should Terraform state files not be committed to Git?

Terraform state files may contain sensitive information, such as passwords, tokens, resource attributes, and infrastructure identifiers.

Committing state files to Git creates security risks and may cause conflicts when multiple developers work on the same infrastructure.

State files should instead be stored in a secure backend with appropriate access controls, encryption, and state locking.

In our lab, we excluded `*.tfstate` and `*.tfstate.*` using `.gitignore`.

## Part 2 — Variables, Outputs and Modules

### Q3. What are the advantages of using separate folders and state files for each environment instead of Terraform workspaces?

Separate folders and state files provide explicit isolation between environments.

Each environment can have its own variables, backend configuration, permissions, and deployment lifecycle.

This reduces the risk of accidentally modifying production resources while working on development infrastructure.

Terraform workspaces allow multiple states within one configuration, but separate directories are often easier to manage when environments have different requirements.

In our lab, DEV and STAGING used the same reusable module but different configurations, ports, and state files.

## Part 3 — State Management

### Q4. Why is a remote backend with state locking important for a team?

A remote backend provides a shared, centralized location for Terraform state.

State locking prevents multiple team members or CI jobs from modifying the same state simultaneously, reducing the risk of state corruption.

Remote backends can also provide encryption, access control, and versioning.

Our lab used a local backend to simulate state separation, but a production team should use a backend supporting shared state and locking.

### Q5. What sensitive information can Terraform state contain?

Terraform state can contain passwords, API keys, access tokens, database connection information, and other sensitive resource attributes.

Marking an output as `sensitive` hides it from normal CLI output, but does not necessarily remove its value from the state file.

Therefore, state files must be protected with encryption and restricted access.

## Part 4 — Ephemeral Environments per Pull Request

### Q6. What happens if preview environments are never destroyed? Propose three mitigations.

If preview environments are never destroyed, they accumulate and consume CPU, memory, storage, and other infrastructure resources.

They may also increase costs and expose outdated applications or configurations.

Three mitigations are:

1. Automatically destroy preview environments when a Pull Request is closed or merged.
2. Apply a time-to-live (TTL) policy to remove expired environments.
3. Use resource quotas and ownership labels to limit consumption and identify responsible teams.

In our lab, we created `pr-42` and `pr-43` with separate Terraform states, then destroyed `pr-42` without affecting `pr-43`.

## Part 5 — Terraform in CI with Security Scanning

### Q7. Why should Terraform plan run on Pull Requests while apply runs only after merge?

`terraform plan` allows developers and reviewers to inspect proposed infrastructure changes before they are applied.

It helps detect unexpected resource creation, modification, or destruction.

Running `terraform apply` automatically on every Pull Request would allow unreviewed code to modify infrastructure.

Therefore, CI should validate and plan changes during Pull Requests, while applying changes should occur only after approval and merge through an authorized deployment process.

In our lab, GitHub Actions executed Terraform formatting, validation, planning, and Checkov security scanning.

### Q8. Why is OIDC preferable to long-lived cloud credentials in CI/CD?

OpenID Connect (OIDC) allows CI/CD workflows to obtain short-lived cloud credentials through identity federation.

Unlike long-lived access keys, temporary credentials expire automatically and reduce the impact of credential leaks.

OIDC also allows access policies to restrict which repositories, branches, or workflows can assume a cloud role.

This improves security and reduces the need to store permanent cloud credentials as GitHub secrets.