# Base
FROM python:3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk update && \
    apk upgrade && \
    apk add --no-cache netcat-openbsd && \
    rm -rf /var/cache/apk/* && \
    pip install --no-cache-dir --upgrade pip && \
    adduser --disabled-password -h /home/duser duser && \
    mkdir -p /data/web/static /data/web/media && \
    chown -R duser:duser /data/web

COPY pyproject.toml .
COPY ./entrypoint.sh /entrypoint.sh

# Dev
FROM base AS development
COPY ./app ./app

RUN pip install --no-cache-dir -e ".[dev]" && \
    sed -i 's/\r$//' /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown -R duser:duser /code

USER duser

WORKDIR /code/app

EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

# Prod
FROM base AS production

COPY ./app ./app

RUN pip install --no-cache-dir . && \
    sed -i 's/\r$//' /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown -R duser:duser /code

USER duser

WORKDIR /code/app

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "project.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "2", \
    "--timeout", "60", \
    "--max-requests", "1000", \
    "--max-requests-jitter", "50"]