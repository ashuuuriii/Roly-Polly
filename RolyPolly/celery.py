import os

from celery import Celery

# Pass the project settings module to celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RolyPolly.settings")

app = Celery("RolyPolly")

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefi
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks contained in tasks.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
