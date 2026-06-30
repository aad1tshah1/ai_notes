from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.notes import router as notes_router
from api.auth import router as auth_router
from api.jobs import router as jobs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(notes_router)
app.include_router(auth_router)
app.include_router(jobs_router)

@app.get("/health")
def get_health():
    return {"message": "Health check successful"}