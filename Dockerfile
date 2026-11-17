#FROM python:3.13-alpine
#WORKDIR /app
#RUN adduser -D appuser
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#COPY . .
#USER appuser
#EXPOSE 5000
#CMD ["python", "app.py"]



# Multi-stage build
FROM python:3.13-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-alpine
WORKDIR /app
RUN adduser -D appuser
COPY requirements.txt .
COPY --from=builder /install /usr/local
COPY . .
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]
