from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Application

async def apply_job(db: AsyncSession, resume_path: str, user_id: int, job_id: int, cover_letter: str):
    application = Application(candidate_id = user_id, job_id = job_id, resume_path = resume_path, cover_letter = cover_letter)
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application