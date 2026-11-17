FROM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-alpine

RUN adduser -D appuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
