from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class Company(SQLModel, table=True):

    __tablename__ = "companies"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, unique=True, index=True)
    description: str | None = Field(default=None)
    website: str | None = Field(default=None, max_length=255)
    email: str = Field(max_length=255, unique=True, index=True)
    owner_id: int = Field(foreign_key="users.id", unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional["User"] = Relationship(back_populates="company")

    jobs: List["Job"] = Relationship(back_populates="company")