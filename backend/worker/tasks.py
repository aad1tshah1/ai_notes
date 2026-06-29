import asyncio
import os

from worker.celery_app import celery
from core.database import SessionLocal

from services.transcription_service import transcribe_audio
from services.summarisation_service import generate_meeting_notes
from repositories.note_repository import save_note
from repositories.job_repository import mark_job_completed, mark_job_failed, update_job_status
from models.user import User
from models.note import Note
from models.job import Job


@celery.task
def process_note(job_id: str, user_id: str, audio_path: str):
    db = SessionLocal()

    try:
        print(f"Processing job {job_id} for user {user_id}")

        update_job_status(db, job_id, user_id, "transcribing")
        transcript = transcribe_audio(audio_path)

        update_job_status(db, job_id, user_id, "summarising")
        notes = asyncio.run(generate_meeting_notes(transcript))

        update_job_status(db, job_id, user_id, "saving")
        saved_note = save_note(db, transcript, notes, user_id)

        mark_job_completed(db, job_id, user_id, saved_note.note_id)

        print(f"Completed job {job_id}")

    except Exception as e:
        db.rollback()
        mark_job_failed(db,job_id, user_id, str(e))

        print(f"Failed job {job_id}: {e}")

    finally:
        db.close()

        if os.path.exists(audio_path):
            os.remove(audio_path)