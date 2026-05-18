from pydantic import BaseModel

from ..models.application import ApplicationStatus

class StatusUpdateSchema(BaseModel):
    status: ApplicationStatus