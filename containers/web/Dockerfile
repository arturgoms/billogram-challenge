FROM python:3.9-slim

MAINTAINER artur "contato@arturgomes.com.br"

WORKDIR /app
COPY src/ .

# Environment
ARG ENV
ENV ENV=${production} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

ADD ./containers/web/entrypoint.sh /
ADD ./containers/web/gunicorn.py /
COPY poetry.lock pyproject.toml /app/

# Install requirements
RUN pip install gunicorn==20.0

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENV" == production && echo "--no-dev") --no-interaction --no-ansi


# Prepare entrypoint
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 80
