from sqlmodel import SQLModel, Field, Relationship

from datetime import datetime
from typing import List, Optional

from .skill import JobSkillLink

class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: int = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    salary_range: str | None = Field(default=None)
    job_type: str
    job_category: str
    location: str | None = Field(default=None)
    company_id:  int = Field(foreign_key="companies.id")
    company_website: str | None = Field(default=None)
    company_description: str | None = Field(default=None)
    views: int | None = Field(default=0)
    applicants: int | None = Field(default=0)
    date_posted: datetime = Field(default_factory=datetime.utcnow)

    company: Optional["Company"] = Relationship(back_populates="jobs")

    applications: List["Application"] = Relationship(back_populates="job")

    skills: List["Skill"] = Relationship(back_populates="jobs", link_model=JobSkillLink)