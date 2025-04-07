echo "Starting celery Worker"
sleep 1
celery -A make_celery worker -B -l info -E