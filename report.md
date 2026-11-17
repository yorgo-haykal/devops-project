# Lab 1

## Question 1: Why forbid direct pushes to `main`?

In DevOps, git has a huge role in the tracability and quality of code especially the `main` branch which is considered to be the source of truth. Therefore, it should always contain code that is reviewed, tested and ready to be deployed. Forbidding direct pushes and requiring a Pull Request protects that guarantee: 
- Quality (every change goes through a PR, so it must pass the CI pipeline (lint, tests, build) and be reviewed by at least one teammate)
- Stability.
- Traceability.
- Accountability.

## Question 2: What is the difference between an image and a container?

An image is the blueprint that is used to run containers. A container is basically an instance of that image, we can have mutliple container running from the same image.

## Question 3. Compare the size of your image with a non-slim base image. What do you observe?

Our slim Alpine image is way smaller than the full non-slim Python image, because the full image includes a complete Debian system with build tools, compilers, and system libraries that our simple Flask app doesn’t need. Using a lightweight base image reduces storage and speeds up pulls and deployments.