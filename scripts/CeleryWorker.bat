@echo off
echo "starting celery Worker with gevent win64"
celery -A make_celery worker -l info -P gevent -E