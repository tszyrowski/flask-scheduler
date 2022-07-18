#!/bin/sh

celery -A app.celery worker --loglevel=DEBUG --detach --pidfile=''

celery -A app.celery beat --loglevel=DEBUG --detach --pidfile=''

flask run --host=0.0.0.0 --port 5000