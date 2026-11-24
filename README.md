# DevOps Lab Session 3: Terraform, Environments and Ephemeral Previews

## Part 1: First Terraform Configuration
### 1.1 Run init, fmt, validate and plan.
```bash
(.venv) PS C:\Users\Lucie\Documents\Efrei\in3\DevOps and Continuous Deployment\devops-project\infra\quickstart> terraform init
[...]
Terraform has been successfully initialized!
[...]


(.venv) PS C:\Users\Lucie\Documents\Efrei\in3\DevOps and Continuous Deployment\devops-project\infra\quickstart> terraform fmt


(.venv) PS C:\Users\Lucie\Documents\Efrei\in3\DevOps and Continuous Deployment\devops-project\infra\quickstart> terraform validate
Success! The configuration is valid.


(.venv) PS C:\Users\Lucie\Documents\Efrei\in3\DevOps and Continuous Deployment\devops-project\infra\quickstart> terraform plan 
[...]
Plan: 2 to add, 0 to change, 0 to destroy.
```

### 1.2 Apply and check the container with curl http://localhost:8081.
```bash
terraform apply
[...]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

```bash
curl.exe http://localhost:8081
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### 1.3 Change the external port to 8082, run plan and read the diff carefully.
```bash
terraform fmt
terraform plan
[...]

      ~ ports {
          ~ external = 8081 -> 8082 # forces replacement
            # (3 unchanged attributes hidden)
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```
### 1.4 Apply, then run terraform show and inspect the state.
```bash
terraform apply
[...]

      ~ ports {
          ~ external = 8081 -> 8082 # forces replacement
            # (3 unchanged attributes hidden)
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.
[...]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.


(.venv) PS C:\Users\Lucie\Documents\Efrei\in3\DevOps and Continuous Deployment\devops-project\infra\quickstart> terraform show
[...]

    ports {
        external = 8082
        internal = 80
        ip       = "0.0.0.0"
        protocol = "tcp"
    }
}

# docker_image.nginx:
resource "docker_image" "nginx" {
    id          = "sha256:6784fb0834aa7dbbe12e3d7471e69c290df3e6ba810dc38b34ae33d3c1c05f7dnginx:1.27"
    image_id    = "sha256:6784fb0834aa7dbbe12e3d7471e69c290df3e6ba810dc38b34ae33d3c1c05f7d"
    name        = "nginx:1.27"
    repo_digest = "nginx@sha256:6784fb0834aa7dbbe12e3d7471e69c290df3e6ba810dc38b34ae33d3c1c05f7d"
}
```
```bash
curl.exe http://localhost:8082
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
### 1.5 Delete the container manually with docker rm -f tf-web, then run plan
```bash
terraform plan
[...]

Plan: 1 to add, 0 to change, 0 to destroy.
```

### Question 1. What did Terraform propose after you deleted the container by hand? What is this situation called?
Terraform proposed to create the container again because it was deleted manually. This situation is called drift. 


### Question 2. Why should the state file never be committed to Git?
The state file should never be committed to Git because it can contain sensitive information and private data.


 ## Part 2: Variables, Outputs and Modules

### 2.3 Apply both environments separately with -chdir and -var-file.
```bash
terraform -chdir=envs/dev plan -var-file="dev.tfvars"
terraform -chdir=envs/dev apply -var-file="dev.tfvars"
[...]

Plan: 2 to add, 0 to change, 0 to destroy.
[...]

Plan: 2 to add, 0 to change, 0 to destroy.
[...]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

```bash
terraform -chdir=envs/staging init
terraform -chdir=envs/staging plan -var-file="staging.tfvars"
terraform -chdir=envs/staging apply -var-file="staging.tfvars"
[...]

Terraform has been successfully initialized!
[...]

      + ports {
          + external = 8083
          + internal = 80
          + ip       = "0.0.0.0"
          + protocol = "tcp"
        }
    }

  # module.webapp.docker_image.app will be created
  + resource "docker_image" "app" {
      + id          = (known after apply)
      + image_id    = (known after apply)
      + name        = "nginx:1.27"
      + repo_digest = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

─[...]

      + ports {
          + external = 8083
          + internal = 80
          + ip       = "0.0.0.0"
          + protocol = "tcp"
        }
    }

  # module.webapp.docker_image.app will be created
  + resource "docker_image" "app" {
      + id          = (known after apply)
      + image_id    = (known after apply)
      + name        = "nginx:1.27"
      + repo_digest = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
[...]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```


### 2.4 Confirm both containers run side by side with different names.
```bash
docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED              STATUS              PORTS                       NAMES
702ce9097453   6784fb0834aa           "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:8083->80/tcp        tf-staging
1e9dabbae32a   6784fb0834aa           "/docker-entrypoint.…"   3 minutes ago        Up 3 minutes        0.0.0.0:8082->80/tcp        tf-dev
```

### Question 3. What are the advantages of one folder and one state per environment compared to workspaces
Using one folder and one state per environment makes the configuration easier to understand and manage. It keeps dev and staging separate and reduces the risk of modifying the wrong environment. It is also easier to work with different configurations for each environment.


## Part 3: State Management

## #3.3 Move the state of dev to a local “remote-like” backend path (shared folder) and run terraform init -migrate-state.
```bash
terraform -chdir=infra/envs/dev init -migrate-state
[...]
Successfully configured the backend "local"! Terraform will automatically
[...]
Terraform has been successfully initialized!
```

### 3.4 List resources with terraform state list and inspect one with terraform state show.
```bash
terraform state list
module.webapp.docker_container.app
module.webapp.docker_image.app
```

```bash
terraform state show module.webapp.docker_container.app
resource "docker_container" "app" {
   [...]
    name                                        = "tf-dev"
    [...]
    ports {
        external = 8082
        internal = 80
        ip       = "0.0.0.0"
        protocol = "tcp"
    }
}
```

### 3.5 Simulate drift: change the container port outside Terraform (recreate it with Docker) and detect it with terraform plan.
```bash
docker rm -f tf-dev
tf-dev

docker run -d --name tf-dev -p 8084:80 nginx:1.27
058e7acbd5e7205f5fa2a70360de7eeffb8529c82e19bcfed62dd99c8164123f


terraform plan -refresh-only
var.env_name
  Enter a value: dev

var.external_port
  Enter a value: 8082

var.image
  Enter a value: nginx:1.27
[...]
  - resource "docker_container" "app" {
      [...]
      - name                                        = "tf-dev" -> null
      [...]
      - ports {
          - external = 8082 -> null
          - internal = 80 -> null
          - ip       = "0.0.0.0" -> null
          - protocol = "tcp" -> null
        }
    }

```

### Question 4. Why is a remote backend with locking essential for a team? Which problems does it prevent?
A remote backend allows team members to share the same Terraform state file. Locking prevents multiple people from modifying the infrastructure at the same time. It avoids conflicts, state corruption and inconsistent infrastructure.

### Question 5. What information in a state file can be sensitive?
A Terraform state file can contain sensitive information such as passwords, API keys, access tokens, database credentials and private infrastructure details. This information must be protected to prevent unauthorized access.


## Part 4: Ephemeral Environment per Pull Request

### 4.1 Complete the configuration with a Service exposing the deployment.

```bash
terraform validate
Success! The configuration is valid.
```

### 4.2 Deploy a preview for fake PR number 42, using a unique state file per PR.
```bash
terraform init -backend-config="path=state/pr-42.tfstate"
[...]

Terraform has been successfully initialized!
```
```bash
 kubectl get all -n pr-42
NAME                         READY   STATUS    RESTARTS   AGE
pod/myapp-79cc5fd58c-q9xvs   1/1     Running   0          28s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/myapp   ClusterIP   10.101.6.173   <none>        5000/TCP   28s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp   1/1     1            1           28sterraform init -backend-config="path=state/pr-43.tfstate" -reconfigure
```

### 4.3 Deploy a second preview for PR 43 and confirm they are isolated.
```bash
 kubectl get all -n pr-43
NAME                         READY   STATUS    RESTARTS   AGE
pod/myapp-79cc5fd58c-qw5d2   1/1     Running   0          35s

NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/myapp   ClusterIP   10.108.158.81   <none>        5000/TCP   35s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp   1/1     1            1           35s
```

```bash
kubectl get namespaces
[...]
NAME                   STATUS   AGE
pr-42                  Active   5m57s
pr-43                  Active   75s
```


### 4.4 Destroy preview 42 and verify its namespace and resources disappear.
```bash
terraform destroy -var="pr_number=42" -var="image=ghcr.io/yorgo-haykal/devops-project:ed42b424ce2c80d941dbf38112225f1ec399a099"
[...]
Destroy complete! Resources: 3 destroyed.

kubectl get namespaces
NAME                   STATUS   AGE
[...]
pr-43                  Active   4m55s
```

### Question 6. What could go wrong if the preview environment is never destroyed? List three mitigations.
If a preview environment is never destroyed:
- It wastes resources and increases costs.
- It can create security risks.
-  It uses resources that other projects need.

Three mitigations:
1. Automatically destroy it when the pull request is closed.
2. Add an expiration date (expires label).
3. Regularly check and delete unused environments.


## Part 5: Terraform in CI with Security Scanning 

### 5.1 Runs terraform fmt -check and terraform validate.
```bash
terraform -chdir=infra/envs/dev fmt -check
terraform -chdir=infra/envs/dev validate
Success! The configuration is valid.
```

### 5.2 Runs terraform plan and uploads the output as an artifact.
```bash
terraform -chdir=infra/envs/dev plan -out=tfplan
[...]
Plan: 2 to add, 0 to change, 1 to destroy.
```


### Question 7. Why run plan on a Pull Request but apply only after merge?
plan is read-only. It shows what will change without touching anything, so reviewers can check the impact before approving. apply changes the real infrastructure, so it must run only after the code is reviewed and merged into main. This avoids untested or unsafe changes, keeps main as the single source of truth, and prevents conflicts between several open PRs.


### Question 8. Why should a CI pipeline use short-lived credentials (OIDC) rather than long-lived access keys?
With OIDC, the pipeline gets a temporary token for each run, so there is no permanent secret to store. If a token leaks, it expires quickly, but a long-lived key stays valid until someone revokes it. OIDC also removes manual key rotation and lets us limit access to one repository or branch.

