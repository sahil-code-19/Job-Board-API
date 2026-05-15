from pydantic import BaseModel, EmailStr
from ..models.user import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.candidate

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str