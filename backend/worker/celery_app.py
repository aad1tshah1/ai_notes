from celery import Celery

celery = Celery(
    "ai_notes",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["worker.tasks"],
)