from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, status, HTTPException, Query, Depends

from pydantic import BaseModel

from ..schemas.job import JobCreate, JobResponse, JobUpdate
from ..schemas.common import PaginatedResponse, ErrorResponse

router = APIRouter(prefix="/jobs")

job_create = {
  "title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer with FastAPI knowledge.",
  "company": "TechNova Solutions",
  "salary_range": "10 LPA - 18 LPA",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "job_type": "Full-time",
  "job_category": "Software Development",
  "location": "Ahmedabad, India",
  "company_website": "https://technova.com",
  "company_description": "TechNova Solutions is a fast-growing AI startup."
}

updated_job = None

job_list = [
  {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer with FastAPI knowledge.",
    "company": "TechNova Solutions",
    "salary_range": "10 LPA - 18 LPA",
    "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "job_type": "Full-time",
    "job_category": "Software Development",
    "location": "Ahmedabad, India",
    "company_website": "https://technova.com",
    "company_description": "TechNova Solutions is a fast-growing AI startup.",
    "views": 120,
    "applicants": 15,
    "date_posted": "2026-05-13T10:30:00"
  },
  {
    "id": 2,
    "title": "Frontend React Developer",
    "description": "Looking for a React developer with 2+ years experience.",
    "company": "WebCraft Pvt Ltd",
    "salary_range": "6 LPA - 10 LPA",
    "skills": ["React", "JavaScript", "Tailwind CSS"],
    "job_type": "Full-time",
    "job_category": "Frontend Development",
    "location": "Remote",
    "company_website": "https://webcraft.io",
    "company_description": "WebCraft builds modern web applications.",
    "views": 85,
    "applicants": 9,
    "date_posted": "2026-05-10T08:15:00"
  },
  {
    "id": 3,
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer with FastAPI knowledge.",
    "company": "TechNova Solutions",
    "salary_range": "10 LPA - 18 LPA",
    "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "job_type": "Part-time",
    "job_category": "Software Development",
    "location": "Ahmedabad, India",
    "company_website": "https://technova.com",
    "company_description": "TechNova Solutions is a fast-growing AI startup.",
    "views": 120,
    "applicants": 15,
    "date_posted": "2026-05-13T10:30:00"
  },
]

job_edit = {
  "salary_range": "12 LPA - 20 LPA",
  "location": "Remote",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"]
}


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def job_create(job_create: JobCreate):
    updated_job = job_create.model_copy(update={
        "id": 3,
        "date_posted": "Monday",
        "applicants": 0,
        "views": 0
    })
    job_list.append(updated_job)
    return updated_job

class JobFilter(BaseModel):
    skills: str | None = None
    location: str | None = None
    company: str | None = None
    job_type: str | None = None
    job_category: str | None = None

@router.get('/all', status_code=status.HTTP_200_OK, response_model=PaginatedResponse[JobResponse])
def all_jobs(job_filter: JobFilter = Depends(), page: int = 1, size: int = 10):
    filter_dict = job_filter.model_dump(exclude_none=True)

    print(filter_dict)

    result = []

    for job in job_list:
        if all(
            key == "skills" and value.capitalize() in job["skills"]
            or key != "skills" and value == job.get(key)
            for key, value in filter_dict.items()
        ):
            result.append(job)

    print(result)
    total = len(result)
    start = (page - 1) * size
    end = size + start

    paginated_items = result[start:end]

    return {
        "total": total,
        "page": page,
        "size": size,
        "items": paginated_items
    }

@router.get('/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
def get_job(job_id: int):
    for job in job_list:
      if job["id"] == job_id:
          return job      
      
    raise HTTPException(
        status_code=404,
        detail={
            "detail": "Job not found",
            "error_code": "JOB_NOT_FOUND"
        }
    )
    

@router.patch('/edit/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
def edit_job(job_id: int, data: JobUpdate):
    updated_data = data.model_dump()

    for index, job in enumerate(job_list):
      if job["id"] == job_id:
          updated_data["id"] = job_id
          job_list[index] = updated_data
          return updated_data
      
    raise HTTPException(
        status_code=404,
        detail={
            "detail": "Job not found",
            "error_code": "JOB_NOT_FOUND"
        }
    )

@router.put('/full-edit/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
def full_edit_job(job_id: int, data: JobUpdate):
    updated_data = data.model_dump(exclude_unset=True)
    for job in job_list:
        if job["id"] == job_id:
            job.update(updated_data)
            return job
    raise HTTPException(
        status_code=404,
        detail={
            "detail": "Job not found",
            "error_code": "JOB_NOT_FOUND"
        }
    )

@router.delete('/delete/{job_id}', response_model=JobResponse, status_code=status.HTTP_200_OK, responses={404: {"model": ErrorResponse}})
def delete_job(job_id: int):
    for job in job_list:
        if job["id"] == job_id:
            job_list.remove(job)
            return job
    raise HTTPException(
        status_code=404,
        detail={
            "detail": "Job not found",
            "error_code": "JOB_NOT_FOUND"
        }
    )
    
