# Lab 1

## Question 1: Why forbid direct pushes to `main`?

In DevOps, git has a huge role in the tracability and quality of code especially the `main` branch which is considered to be the source of truth. Therefore, it should always contain code that is reviewed, tested and ready to be deployed. Forbidding direct pushes and requiring a Pull Request protects that guarantee: 
- Quality (every change goes through a PR, so it must pass the CI pipeline (lint, tests, build) and be reviewed by at least one teammate)
- Stability.
- Traceability.
- Accountability.

## Question 2: What is the difference between an image and a container?

An **image** is a read-only template: it packages the application code, its dependencies and the base OS layers, built from a Dockerfile. It is immutable and only exists on disk (it can be stored in a registry and shared).

A **container** is a running (or stopped) instance of an image. Docker adds a thin writable layer on top of the image and starts an isolated process with its own filesystem, network and environment. It is ephemeral: it can be stopped, deleted and recreated at any time.

One image can be used to start many containers.

## Question 3: Compare the size of your image with a non-slim base image

> docker images myapp
IMAGE        ID             DISK USAGE   CONTENT SIZE   EXTRA
myapp:0.1    5b5804954393        185MB         44.9MB    U
myapp:full   0dbfd226e284       1.61GB          414MB

The slim image is almost 10 times smaller than the full image. We can explain it because python slim version loads only what it needs for the code whereas the full version loads everything.

A smaller image means faster builds, pulls and deployments, less storage and bandwidth, and a smaller attack surface.