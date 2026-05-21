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
        metrics = request.app.state.metrics
        avg_latency = metrics["total_latency_ms"] / metrics["total_requests"] if metrics["total_requests"] != 0 else 0.0
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Some Problems occured"
        )
    
    return {
        "average_latency" : avg_latency,
        "total_requests" : metrics["total_requests"],
        "total_errors" : metrics["total_errors"]
    }