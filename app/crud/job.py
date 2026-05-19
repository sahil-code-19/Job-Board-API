from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional, List

from ..schemas.filters import JobFilter
from ..models.job import Job

async def create_job(db: AsyncSession, job_data: dict) -> Job:
    job = Job(**job_data)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

async def get_job(db: AsyncSession, job_id: int) -> Optional[Job]:
    result = await db.execute(
        select(Job).where(Job.id == job_id)
    )

    return result.scalar_one_or_none()

async def list_job(db: AsyncSession, filters: JobFilter, skip: int = 0, limit: int = 10) -> List[Job]:
    query = select(Job)

    if filters.location:
        query = query.where(Job.location.ilike(f"%{filters.location}%"))
    if filters.job_type:
        query = query.where(Job.job_type == filters.job_type)
    if filters.job_category:
        query = query.where(Job.job_category == filters.job_category)
    

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def edit_job(db: AsyncSession, job_id: int, job_data: dict) -> Job:
    job = await get_job(db, job_id)

    if not job:
        return None
    
    for key, value in job_data.items():
        setattr(job, key, value)

    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

async def delete_job(db: AsyncSession, job_id: int) -> bool:
    job = await get_job(db, job_id)

    if not job:
        return False
    
    await db.delete(job)
    await db.commit()
    
    return job