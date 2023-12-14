FROM python:3.9-alpine3.13
LABEL maintainer="AGsalamH"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY . /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false
RUN python -m venv /pyenv && \
    /pyenv/bin/pip install --upgrade pip && \
    /pyenv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /pyenv/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
    # mkdir -p /vol/web/media && \
    # mkdir -p /vol/web/static && \
    # chown -R django-user:django-user /vol && \
    # chmod -R 755 /vol && \
    # chmod -R +x /scripts

ENV PATH="/pyenv/bin:$PATH"

USER django-user








#region old_version
    # FROM python:3.12-alpine3.17
    # LABEL maintainer="AGsalamH"

    # ENV PYTHONUNBUFFERED 1


    # COPY requirements.txt /tmp/requirements.txt
    # COPY requirements.dev.txt /tmp/requirements.dev.txt

    # WORKDIR /app
    # COPY . .

    # ARG DEV=false
    # RUN pip3 install --upgrade pip && \ 
    #     pip3 install -r /tmp/requirements.txt && \
    #     if [$DEV = "true"]; \
    #         then pip3 install -r /tmp/requirements.dev.txt; \
    #     fi && \
    #     rm -rf /tmp && \
    #     adduser \
    #         --disabled-password \
    #         django-user

    # USER django-user
    # EXPOSE 8000
#endregion



