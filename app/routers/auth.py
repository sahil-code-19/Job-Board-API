from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_current_user
from ..auth.jwt import create_access_token, create_refresh_token, decode_token, verify_token_type
from ..crud.users import get_user_by_email, create_user, authenticate_user
from ..database import get_db
from ..schemas.auth import UserLogin, UserRegister, UserResponse, Token, RefreshRequest
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, data.email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email id already taken"
        )
    
    user = await create_user(
        db,
        user_in= data
    )
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not exist or user is inactive!"
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/token", include_in_schema=False)
async def login_for_swagger(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """Special endpoint for Swagger UI Authorize button"""
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    print(f"Access token: {access_token}")
    print(f"Refresh token: {refresh_token}")
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )
    try:
        payload = decode_token(data.refresh_token)
        if not verify_token_type(payload, "refresh"):
            raise credentials_exception
        
        user_id = payload.get('sub')

        if not user_id:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    
    access_token = create_access_token({"sub": str(user_id)})
    refresh_token = create_refresh_token({"sub": str(user_id)})

    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user