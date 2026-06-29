from datetime import datetime

from models.job import Job


def create_job(db, user_id):
    job = Job(
        user_id=user_id,
        status="pending",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db, job_id, user_id):
    return (
        db.query(Job)
        .filter(
            Job.job_id == job_id,
            Job.user_id == user_id,
        )
        .first()
    )


def mark_job_completed(db, job_id, user_id, note_id):
    job = get_job(db, job_id, user_id)

    if not job:
        return None

    job.status = "completed"
    job.note_id = note_id
    job.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return job


def mark_job_failed(db, job_id, user_id, error_message):
    job = get_job(db, job_id, user_id)

    if not job:
        return None

    job.status = "failed"
    job.error_message = error_message
    job.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return job

def update_job_status(db, job_id, user_id, status):
    job = get_job(db, job_id, user_id)

    if not job:
        return None

    job.status = status

    db.commit()
    db.refresh(job)

    return job