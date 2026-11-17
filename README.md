# devops-project

Minimal Flask API for the DevOps continuous deployment course.

## Endpoints

| Method | Path      | Response |
|--------|-----------|----------|
| GET    | `/health` | `OK` (200) |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
```

## Workflow

- `main` is protected: all changes go through a Pull Request.

## Questions & Answers

### Question 1: Why forbid direct pushes to main?

Direct pushes to `main` are forbidden to protect the stability of the project. Pull Requests allow developers to review changes, run automated tests and detect potential problems before merging code into the main branch.

### Question 2: What is the difference between an image and a container?

A Docker image is a read-only template containing the application, its dependencies and the environment required to run it.

A Docker container is a running instance of an image. Multiple containers can be created from the same image.

### Question 3: Compare the size of your image with a non-slim base image. What do you observe?

We built two Docker images using different Python base images.

| Base image | Disk usage |
|---|---:|
| `python:3.12-slim` | 198 MB |
| `python:3.12` | 1.62 GB |

The slim image is approximately 87.8% smaller.

This is because slim images exclude many unnecessary system packages and tools. Using slim images reduces storage requirements and can improve image transfer times.

### Question 4: Why tag the image with the commit SHA rather than latest?

Using the commit SHA provides a unique identifier that links the Docker image to a specific version of the source code.

It improves traceability and reproducibility and makes it easier to identify or roll back to a specific version.

The `latest` tag is mutable and does not reliably identify a specific version.

### Question 5: What does "fail fast" mean in a pipeline?

Fail fast means stopping the pipeline as soon as a critical step fails, instead of continuing with unnecessary operations.

For example, when our automated health endpoint test failed, GitHub Actions stopped the job before building the Docker image.

This saves resources and prevents invalid code from progressing through the pipeline.