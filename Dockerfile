FROM python:3.10.6-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgresql://parser_user:parser_pass@localhost/parser_db

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
