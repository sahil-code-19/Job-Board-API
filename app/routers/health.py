from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..database import get_db


router = APIRouter(tags=["health-check"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def check_health(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

    try:
        redis = request.app.state.redis
        await redis.ping()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Redis unavailable"
        )
    
    return {"status": "ok", "database": "ok", "redis": "ok"}