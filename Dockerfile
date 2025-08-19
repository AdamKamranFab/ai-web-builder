# Use official Python base image
FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /code/app

COPY alembic.ini .
COPY alembic /code/alembic

EXPOSE 8005

ENV PYTHONPATH=/code

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8005"]
