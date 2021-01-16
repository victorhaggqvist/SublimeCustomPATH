FROM python:3.6-slim AS build-env

RUN apt-get update \
  && apt-get install --no-install-recommends -y git

ENV PYTHONUNBUFFERED=1 \
  # prevents python creating .pyc files
  PYTHONDONTWRITEBYTECODE=1 \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry
  # https://python-poetry.org/docs/configuration/#using-environment-variables
  POETRY_VERSION=1.1.4 \
  POETRY_VIRTUALENVS_CREATE=true \
  POETRY_VIRTUALENVS_PATH=/poetry/venv/ \
  # do not ask any interactive question
  POETRY_NO_INTERACTION=1

RUN pip install poetry==$POETRY_VERSION

WORKDIR /project

FROM build-env

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install
