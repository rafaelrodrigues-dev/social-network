#!/bin/sh

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

chown -R duser:duser /data/web/static
chown -R duser:duser /data/web/media
chmod -R 755 /data/web/static
chmod -R 755 /data/web/media

su-exec duser python manage.py collectstatic --noinput
su-exec duser python manage.py makemigrations --noinput
su-exec duser python manage.py migrate --noinput
exec su-exec duser gunicorn project.wsgi:application --bind 0.0.0.0:8000