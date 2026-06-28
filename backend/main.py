from fastapi import FastAPI

from api.notes import router as notes_router
from api.auth import router as auth_router

app = FastAPI()

app.include_router(notes_router)
app.include_router(auth_router)

@app.get("/health")
def get_health():
    return {"message": "Health check successful"}