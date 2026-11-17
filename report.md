# Lab 1

## Question 1: Why forbid direct pushes to `main`?

In DevOps, git has a huge role in the tracability and quality of code especially the `main` branch which is considered to be the source of truth. Therefore, it should always contain code that is reviewed, tested and ready to be deployed. Forbidding direct pushes and requiring a Pull Request protects that guarantee: 
- Quality (every change goes through a PR, so it must pass the CI pipeline (lint, tests, build) and be reviewed by at least one teammate)
- Stability.
- Traceability.
- Accountability.