from pydantic import BaseModel
from typing import TypeVar, List, Generic

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None