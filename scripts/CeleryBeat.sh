echo "Starting celery BeatWorker"
sleep 1
celery -A make_celery beat -l debug