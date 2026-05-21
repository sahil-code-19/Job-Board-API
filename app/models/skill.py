from sqlmodel import SQLModel, Field, Relationship
from typing import List

class JobSkillLink(SQLModel, table=True):
    __tablename__ = "job_skill_links"

    job_id : int | None = Field(default=None, foreign_key="jobs.id", primary_key=True)
    skill_id : int | None = Field(default=None, foreign_key="skills.id", primary_key=True)

class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)

    jobs: List["Job"] = Relationship(back_populates="skills", link_model=JobSkillLink)