import tempfile

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from repositories.note_repository import list_notes, get_note, delete_note
from repositories.job_repository import create_job
from core.security import get_current_user
from models.user import User
from worker.tasks import process_note

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("")
async def create_note(audio_file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = create_job(db, current_user.user_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name

    process_note.delay(
        str(job.job_id),
        str(current_user.user_id),
        temp_audio_path,
    )

    return {
        "job_id": str(job.job_id),
        "status": job.status,
        "message": "note processing started",
    }


@router.get("")
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes = list_notes(db, current_user.user_id)

    return [
        {
            "note_id": str(note.note_id),
            "transcript": note.transcript,
            "notes": {
                "summary": note.summary,
                "key_points": note.key_points,
                "action_items": note.action_items,
            },
            "created_at": note.created_at,
        }
        for note in notes
    ]

@router.get("/{note_id}")
def get_note_by_id(note_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = get_note(db, note_id, current_user.user_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "note_id": str(note.note_id),
        "transcript": note.transcript,
        "notes": {
            "summary": note.summary,
            "key_points": note.key_points,
            "action_items": note.action_items,
        },
        "created_at": note.created_at,
    }

@router.delete("/{note_id}")
def delete_note_by_id(note_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = delete_note(db, note_id, current_user.user_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"message": "Note deleted successfully"}

