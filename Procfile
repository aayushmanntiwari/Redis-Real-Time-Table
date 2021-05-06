release: python manage.py migrate
web: gunicorn Main.wsgi --log-file - 
worker: celery -A Main worker --beat -S django --l info