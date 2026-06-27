from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
import tempfile
import os

from services.transcription_service import transcribe_audio
from services.summarisation_service import generate_meeting_notes
from core.database import get_db
from repositories.note_repository import save_note, list_notes, get_note, delete_note

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("")
async def create_note(audio_file: UploadFile = File(...), db: Session = Depends(get_db)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name

    try:
        transcript = transcribe_audio(temp_audio_path) 

        notes = await generate_meeting_notes(transcript)
        saved_note = save_note(db, transcript, notes)

        return {
                "note_id": str(saved_note.note_id),
                "filename": audio_file.filename,
                "transcript": saved_note.transcript,
                "notes": {
                    "summary": saved_note.summary,
                    "key_points": saved_note.key_points,
                    "action_items": saved_note.action_items,
                },
                "created_at": saved_note.created_at,
                "message": "note generated and saved"
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate note: {str(e)}"
        )

    finally:
        os.remove(temp_audio_path)


@router.get("")
def get_notes(db: Session = Depends(get_db)):
    notes = list_notes(db)

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
def get_note_by_id(note_id: str, db: Session = Depends(get_db)):
    note = get_note(db, note_id)
    
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
def delete_note_by_id(note_id: str, db: Session = Depends(get_db)):
    note = delete_note(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"message": "Note deleted successfully"}

