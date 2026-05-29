from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..core.security import hash_password, DUMMY_HASH, verify_password
from ..schemas import auth


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: auth.UserRegister) -> User:
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)

    if not user.is_active:
        return None
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user
