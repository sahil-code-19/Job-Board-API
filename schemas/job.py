from pydantic import BaseModel

from typing import List

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    salary_range: str
    skills: List[str]
    location: str | None = None
    company_website: str | None = None

class JobCreate(JobBase):
    pass
    
class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    company: str | None = None
    salary_range: str | None = None
    skills: List[str] | None = None
    location: str | None = None
    company_website: str | None = None

class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True

    