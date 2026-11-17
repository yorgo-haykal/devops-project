# Lab 1

## Question 1: Why forbid direct pushes to `main`?

In DevOps, Git plays a key role in the traceability and quality of the code. The `main` branch is considered the **source of truth**, so it must always contain code that is reviewed, tested and ready to be deployed. Forbidding direct pushes and requiring a Pull Request protects that guarantee:

- **Quality:** every change goes through a PR, so it must pass the CI pipeline (lint, tests, build) and be reviewed by at least one teammate.
- **Stability:** a broken or untested commit cannot reach `main`, so the published image stays reliable.
- **Traceability:** each change is linked to a branch, a PR, a pipeline run and a merge, so we know who changed what, when and why.
- **Accountability:** the author and the reviewer are identifiable, so there are people to refer to if something goes wrong.

## Question 2: What is the difference between an image and a container?

An **image** is a read-only template: it packages the application code, its dependencies and the base OS layers, and is built from a Dockerfile. It is immutable, only exists on disk, and can be stored in a registry and shared.

A **container** is a running (or stopped) instance of an image. Docker adds a thin writable layer on top of the image and starts an isolated process with its own filesystem, network and environment. It is ephemeral: it can be stopped, deleted and recreated at any time.

One image can be used to start many containers (like a class and its objects).

## Question 3: Compare the size of your image with a non-slim base image

I built the same application twice, once on `python:3.12-slim` and once on `python:3.12`, then compared them with `docker images myapp`.

| Image | Base image | Disk usage | Content size |
|---|---|---|---|
| `myapp:0.1` | `python:3.12-slim` | 185 MB | 44.9 MB |
| `myapp:full` | `python:3.12` | 1.61 GB | 414 MB |

**Observation:** the slim image is about **9 times smaller** than the full one (185 MB vs 1.61 GB).

**Explanation:** the full image ships a complete Debian system with compilers, headers and many development tools that a Flask app does not need at runtime. The slim image only contains what is required to run Python.

**Why it matters:** a smaller image means faster builds, pulls and deployments, less storage and bandwidth, and a smaller attack surface (fewer packages, so fewer potential vulnerabilities).

## Bonus: Multi-stage build

I turned the Dockerfile into a multi-stage build (`Dockerfile.multi`).

| Image | Build type | Disk usage | Content size |
|---|---|---|---|
| `myapp:full` | single stage, `python:3.12` | 1.61 GB | 414 MB |
| `myapp:multi` | multi-stage, `python:3.12-slim` | 202 MB | 48.8 MB |
| `myapp:0.1` | single stage, `python:3.12-slim` | 185 MB | 44.9 MB |