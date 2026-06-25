from fastapi import FastAPI, File, UploadFile, HTTPException
import whisper
import tempfile
import os

app = FastAPI()

model = whisper.load_model("base")


@app.get("/health")
def get_health():
    return {"message": "Health check successful"}


@app.post("/notes")
async def create_note(audio_file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name

    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        result = model.transcribe(temp_audio_path)

        return {
            "filename": audio_file.filename,
            "transcript": result["text"],
            "message": "transcription complete"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

    finally:
        os.remove(temp_audio_path)