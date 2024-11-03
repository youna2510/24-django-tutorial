FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

RUN python manage.py check --deploy || exit 1