import asyncio
import os

from worker.celery_app import celery
from core.database import SessionLocal

from services.transcription_service import transcribe_audio
from services.summarisation_service import generate_meeting_notes
from repositories.note_repository import save_note
from repositories.job_repository import mark_job_completed, mark_job_failed
from models.user import User
from models.note import Note
from models.job import Job


@celery.task
def process_note(job_id: str, user_id: str, audio_path: str):
    db = SessionLocal()

    try:
        print(f"Processing job {job_id} for user {user_id}")

        transcript = transcribe_audio(audio_path)

        notes = asyncio.run(generate_meeting_notes(transcript))

        saved_note = save_note(
            db,
            transcript,
            notes,
            user_id,
        )

        mark_job_completed(
            db,
            job_id,
            user_id,
            saved_note.note_id,
        )

        print(f"Completed job {job_id}")

    except Exception as e:
        mark_job_failed(
            db,
            job_id,
            user_id,
            str(e),
        )

        print(f"Failed job {job_id}: {e}")

    finally:
        db.close()

        if os.path.exists(audio_path):
            os.remove(audio_path)