from celery import Celery

app = Celery()
app.conf.broker_url = "redis://redis:6379/0"
app.conf.result_backend = "redis://redis:6379/0"

app.autodiscover_tasks(['app.core'])
