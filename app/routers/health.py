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

@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_metrics(request: Request):
    try:
        redis = request.app.state.redis
        total_requests = int(await redis.get("metrics:total_requests" or 0))
        total_errors = await redis.get("metrics:total_errors" or 0)
        total_latency_ms = float(await redis.get("metrics:total_latency_ms" or 0.0))

        avg_latency = total_latency_ms / total_requests if total_requests > 0 else 0.0
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Some Problems occured!"
        )

    return {
        "avg_latency_ms": avg_latency,
        "total_requests" : total_requests,
        "total_errors" : int(total_errors) if total_errors else 0
    }