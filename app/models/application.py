from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    accepted = "accepted"
    rejected = "rejected"

class Application(SQLModel, table=True):
    __tablename__ = "applications"

    id: int | None = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="users.id")
    job_id: int = Field(foreign_key="jobs.id")
    status: ApplicationStatus = Field(default=ApplicationStatus.pending)
    resume_path: str | None = Field(default=None)
    cover_letter: str | None = Field(default=None)
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    candidate: Optional["User"] = Relationship(back_populates="applications")

    job: Optional["Job"] = Relationship(back_populates="applications")