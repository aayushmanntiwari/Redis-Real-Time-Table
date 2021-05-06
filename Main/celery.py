import os
import django
from celery import Celery
from Home import scheduler
from celery.schedules import crontab


#also change in __init__py 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('Main')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL


app.conf.beat_schedule = {
    'download_equity': {
        'task': scheduler.download_equity,
        'schedule':crontab(hour=18, minute=0),
    },
}
app.conf.timezone = 'Asia/Kolkata'



# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'