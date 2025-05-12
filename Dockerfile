FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt && \
    apk add --no-cache su-exec && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chmod -R +x /entrypoint.sh

ENV PATH="/scripts:/venv/bin:$PATH"

CMD ["/entrypoint.sh"]