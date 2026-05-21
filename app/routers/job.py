from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.job import JobCreate, JobResponse, JobUpdate
from ..schemas.common import PaginatedResponse, ErrorResponse
from ..schemas.filters import JobFilter
from ..auth.dependencies import EmployerUser

from ..crud import job as crud

router = APIRouter(prefix="/jobs", tags=["Job"])

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def job_create(job_create: JobCreate, current_user: EmployerUser, db: AsyncSession = Depends(get_db)):
    return await crud.create_job(db, job_create.model_dump())


@router.get('/all', status_code=status.HTTP_200_OK, response_model=PaginatedResponse[JobResponse])
async def all_jobs(job_filter: JobFilter = Depends(), page: int = 1, size: int = 10, db: AsyncSession = Depends(get_db)):
    skip = (page-1) * size
    jobs =  await crud.list_job(db, job_filter, skip, size)

    return {
        "total": len(jobs),
        "page": page,
        "size": size,
        "items": jobs
    }

@router.get('/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await crud.get_job(db, job_id)
    if not job:
        raise HTTPException(
        status_code=404,
        detail={
            "detail": "Job not found",
            "error_code": "JOB_NOT_FOUND"
        }
    )
    return job
    

@router.patch('/edit/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
async def edit_job(job_id: int, data: JobUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud.edit_job(db, job_id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=404,
            detail={"detail": "Job not found", "error_code": "JOB_NOT_FOUND"}
        )
    return updated

@router.put('/full-edit/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
async def full_edit_job(job_id: int, data: JobUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud.edit_job(db, job_id, data.model_dump())
    if not updated:
        raise HTTPException(
            status_code=404,
            detail={"detail": "Job not found", "error_code": "JOB_NOT_FOUND"}
        )
    return updated

@router.delete('/delete/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_job(db, job_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"detail": "Job not found", "error_code": "JOB_NOT_FOUND"}
        )
    else:
        return result
