nohup python manage.py runserver 0.0.0.0:8000 &
nohup redis-server start &
nohup celery -A CINMan worker -c 2 -l info &
nohup celery -A CINMan beat_schedule &
