from pydantic import BaseModel

class JobFilter(BaseModel):
    location: str | None = None
    job_type: str | None = None
    job_category: str | None = None