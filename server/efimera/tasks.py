from celery import Celery

from .utils import save_data_to_db

# Configure Celery
celery = Celery('tasks', broker='redis://cache')

@celery.task(bind=True, max_retries=3)
def save_data_to_db_task(self, text_blob):
    try:
        save_data_to_db(text_blob)  # Your original database save function
    except Exception as exc:
        # Retry the task if it fails, with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

