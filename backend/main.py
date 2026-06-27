from fastapi import FastAPI

from api.notes import router as notes_router

app = FastAPI()

app.include_router(notes_router)


@app.get("/health")
def get_health():
    return {"message": "Health check successful"}