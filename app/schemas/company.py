from pydantic import BaseModel, ConfigDict

class CompanyCreate(BaseModel):
    name: str
    description: str | None = None
    website: str | None = None

    model_config = ConfigDict(from_attributes=True)