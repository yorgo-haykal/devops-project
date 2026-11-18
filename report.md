# Lab 1

## Question 1: Why forbid direct pushes to `main`?
In DevOps, git has a huge role in the tracability and quality of code especially the `main` branch which is considered to be the source of truth. Therefore, it should always contain code that is reviewed, tested and ready to be deployed. Forbidding direct pushes and requiring a Pull Request protects that guarantee: 
- Quality (every change goes through a PR, so it must pass the CI pipeline (lint, tests, build) and be reviewed by at least one teammate)
- Stability.

## Question 2: What is the difference between an image and a container?

An **image** is a read-only template: it packages the application code, its dependencies and the base OS layers, built from a Dockerfile. It is immutable and only exists on disk (it can be stored in a registry and shared).

A **container** is a running (or stopped) instance of an image. Docker adds a thin writable layer on top of the image and starts an isolated process with its own filesystem, network and environment. It is ephemeral: it can be stopped, deleted and recreated at any time.

One image can be used to start many containers.

## Question 3: Compare the size of your image with a non-slim base image

I built the same application twice, once on `python:3.12-slim` and once on `python:3.12`, then compared them with `docker images myapp`.
> docker images myapp
IMAGE        ID             DISK USAGE   CONTENT SIZE   EXTRA
myapp:0.1    5b5804954393        185MB         44.9MB    U
myapp:full   0dbfd226e284       1.61GB          414MB

The slim image is almost 10 times smaller than the full image. We can explain it because python slim version loads only what it needs for the code whereas the full version loads everything.

A smaller image means faster builds, pulls and deployments, less storage and bandwidth, and a smaller attack surface.

## Bonus: Multi-stage build

I turned the Dockerfile into a multi-stage build (`Dockerfile.multi`).

| Image | Build type | Disk usage | Content size |
|---|---|---|---|
| `myapp:full` | single stage, `python:3.12` | 1.61 GB | 414 MB |
| `myapp:multi` | multi-stage, `python:3.12-slim` | 202 MB | 48.8 MB |
| `myapp:0.1` | single stage, `python:3.12-slim` | 185 MB | 44.9 MB |
A smaller image means faster builds, pulls and deployments, less storage and bandwidth, and a smaller attack surface.

lab 2 : 

Question 1. What is the role of a namespace? Does it provide strong security isolation by
itself?
 The namespace allows us to divide one cluster into multiple smaller clusters which allows us to have different sessions or environment for example. 
 By itself it doesn't provide much safety but if you add rules on how you can push code from one environment to the other it will be more secure.

 Question 5. How does this pattern help with hybrid/multi-cloud deployments? What would
differ between a real on-prem cluster and a cloud cluster?

the pattern Kustomize helps because the base defines the source of truth which allows to avoid duplicates and differences of configurations on different devices like on cloud or on prem. 
It also allows it to be more portable (one api for everything) and you can see the changes and differences between environement more easily. 

the difference between an on prem configuration and an on cloud would be : 
- availability issues
- scalability
- access to the data with or without internet. 
- exposition of the network (if the load is correctly balanced)
- storage
- cost issues 

question 6
broken image : 
PS C:\Users\aanak\Desktop\S9\07_DEVOPS-CONTINUOUS-DEPLOYMENT\devops-project>   kubectl get pods -n dev
NAME                     READY   STATUS         RESTARTS   AGE
curl-test                1/1     Running        0          47s
myapp-6c74fc7cf8-8sbcp   0/1     ErrImagePull   0          5s
myapp-b8bf6cb8f-njlvc    1/1     Running        0          10m
PS C:\Users\aanak\Desktop\S9\07_DEVOPS-CONTINUOUS-DEPLOYMENT\devops-project>

the broken rollout didn't break the application because the deployment used rollingupdate and readinessprobe. RollingUpdate is a kubernetes function which is dictates that a new pod is published when it's working but in the mean time it still runs the old pod.  readinessprob checks regularly that the functions are working and healthy and doesn't allow new pods if it's broken

kubernetes only deletes the old/running pod when the new pod is ready. which allows it to prevent human errors of misclicks from breaking everything. 