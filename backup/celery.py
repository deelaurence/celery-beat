import os
from celery import Celery
from dotenv import load_dotenv
from backup.tasks import backup_postgres_and_upload
from datetime import timedelta
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_project.settings')

app = Celery('backupPG')

# Load environment variables from .env file
load_dotenv()

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls the first backup task for 'infifteen' every 10 seconds
    sender.add_periodic_task(
        timedelta(seconds=10),
        backup_postgres_and_upload.s(
            database_name=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
            host=os.environ.get('DATABASE_HOST'),
            port=5432,
            backup_dir='.'
        ),
        name='Backup PostgreSQL every 10 seconds'
    )


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')





