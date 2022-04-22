#!/bin/bash
set -e

# define settings module
export DJANGO_SETTINGS_MODULE=settings.production
export DJANGO_DEBUG=False

if [ "$STARTUP" == "APP" ]
then

  # execute migrations
  python manage.py migrate --noinput

  # execute collect static
  python manage.py collectstatic --noinput

  # start the gunicorn server
  gunicorn -c /gunicorn.py wsgi:application

elif [ "$STARTUP" == "WORKER" ]
then

  # Run Celery
  celery -A celery_app worker \
         --concurrency=4 \
         --max-tasks-per-child=100 \
         --loglevel=INFO \
         --events -O fair

elif [ "$STARTUP" == "WORKER-SCHEDULER" ]
then

  # Run Celery Beat
  celery -A celery_app beat -s /data/celerybeat-schedule -l INFO

else
  exit 1
fi

exec "$@"
