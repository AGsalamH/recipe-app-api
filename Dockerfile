FROM python:3.9-alpine3.13
LABEL maintainer="AGsalamH"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY . /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false
RUN apk add  --update --no-cache\
    --virtual .tmp_build_deps \
    postgresql-dev\
    musl-dev\
    build-base\
    zlib zlib-dev linux-headers && \
    apk add --update --no-cache postgresql-client && \
    python -m venv /pyenv && \
    /pyenv/bin/pip install --upgrade pip && \
    /pyenv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /pyenv/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp_build_deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user


ENV PATH="/pyenv/bin:$PATH"

USER django-user
