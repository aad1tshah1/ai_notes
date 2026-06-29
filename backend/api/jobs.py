from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from repositories.job_repository import get_job, create_job

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}")
def get_job_by_id(job_id: str,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    job = get_job(
        db,
        job_id,
        current_user.user_id,
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": str(job.job_id),
        "status": job.status,
        "note_id": str(job.note_id) if job.note_id else None,
        "error_message": job.error_message,
        "created_at": job.created_at,
        "completed_at": job.completed_at,
    }

@router.post("")
def create_test_job(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = create_job(db, current_user.user_id)

    return {
        "job_id": str(job.job_id),
        "status": job.status,
    }