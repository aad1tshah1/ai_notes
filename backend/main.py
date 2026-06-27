from fastapi import FastAPI, File, UploadFile, HTTPException
import tempfile
import os

from services.transcription_service import transcribe_audio
from services.summarisation_service import generate_meeting_notes

app = FastAPI()


@app.get("/health")
def get_health():
    return {"message": "Health check successful"}


@app.post("/notes")
async def create_note(audio_file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name

    try:
        transcript = transcribe_audio(temp_audio_path) 

        notes = await generate_meeting_notes(transcript)
        return {
            "filename": audio_file.filename,
            "transcript": transcript,
            "notes": notes,
            "message": "note generated"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate note: {str(e)}"
        )

    finally:
        os.remove(temp_audio_path)