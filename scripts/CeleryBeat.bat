@echo off
echo "starting celery BeatWorker with gevent win64"
celery -A make_celery beat -l debug