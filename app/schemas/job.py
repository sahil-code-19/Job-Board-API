from datetime import datetime
from pydantic import BaseModel

from typing import List

class JobBase(BaseModel):
    title: str
    description: str
    # company: str
    salary_range: str
    # skills: List[str]
    job_type: str
    job_category: str
    location: str | None = None
    company_website: str | None = None
    company_description: str | None = None

class JobCreate(JobBase):
    company_id: int | None = None
    
class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    salary_range: str | None = None
    location: str | None = None
    company_website: str | None = None
    job_type: str | None = None
    job_category: str | None = None
    company_description: str | None = None

class JobResponse(JobBase):
    id: int
    views: int | None = None
    applicants: int | None = None
    date_posted: datetime

    class Config:
        from_attributes = True