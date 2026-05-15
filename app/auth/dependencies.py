from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .jwt import decode_token, verify_token_type
from ..crud.users import get_user_by_id
from ..models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)

        if not verify_token_type(payload, "access"):
            raise credentials_exception
        
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    
    user = await get_user_by_id(db, int(user_id))
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    
    return user

def require_role(*roles: UserRole):
    """
    Factory dependency — usage:
    Depends(require_role(UserRole.employer))
    Depends(require_role(UserRole.employer, UserRole.admin))
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}"
            )
        return current_user
    return role_checker

CurrentUser = Annotated[User, Depends(get_current_user)]
EmployerUser = Annotated[User, Depends(require_role(UserRole.employer))]
AdminUser = Annotated[User, Depends(require_role(UserRole.admin))]