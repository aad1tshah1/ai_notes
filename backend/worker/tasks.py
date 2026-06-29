from worker.celery_app import celery


@celery.task
def process_note(job_id: str, user_id: str, audio_path: str):
    print(f"Processing job {job_id} for user {user_id}")
    print(f"Audio path: {audio_path}")