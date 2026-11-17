# devops-project

Minimal Flask API for the DevOps continuous deployment course.
Group members : Léanna Suissa, Yorgo Haykal, Lucie Moreau, Junior Adjiey

## Endpoints

| Method | Path      | Response |
|--------|-----------|----------|
| GET    | `/health` | `OK` (200) |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
python app.py
curl http://localhost:3000/health
```

## Workflow

- `main` is protected: all changes go through a Pull Request.
