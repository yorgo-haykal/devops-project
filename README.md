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

## Tests

Run automated tests using pytest:

```bash
python -m pytest -v
```

## Docker

Build the Docker image:

```bash
docker build -t myapp:0.1 .
```

Run the container:

```bash
docker run -d -p 3000:5000 --name myapp myapp:0.1
```

Test the application:

```bash
curl http://localhost:3000/health
```

Stop and remove the container:

```bash
docker stop myapp
docker rm myapp
```

## Project structure

```text
devops-project/
├── .dockerignore
├── app.py
├── Dockerfile
├── README.md
├── requirements.txt
└── test_app.py
```
