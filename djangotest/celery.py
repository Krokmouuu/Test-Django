from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangotest.settings')

app = Celery('djangotest')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Needed for development
app.conf.update(
    task_always_eager=True,   # Execute the task locally
    task_eager_propagates=True,  # progate exceptions
    broker_url='memory://'  # Use an in-memory broker to execute tasks locally
)