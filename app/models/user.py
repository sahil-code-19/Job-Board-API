from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    candidate = "candidate"
    employer = "employer"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=100, unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.candidate)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    company: Optional["Company"] = Relationship(back_populates="owner")

    applications: List["Application"] = Relationship(back_populates="candidate")

    notifications: List["Notification"] = Relationship(back_populates="user")