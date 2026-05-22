import json
import asyncio
from redis.asyncio import Redis

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from .core.limiter import limiter

from .database import create_db_and_tables
from .routers import job, auth, application, notifications, company, health
from .middleware.request_logging import RequestLoggingMiddleWare
from .middleware.request_id import RequestIDMiddleWare
from .core.logging_config import setup_logging
from .websockets.manager import ConnectionManager
from .core.config import get_settings

settings = get_settings()
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):

    #_____STARTUP________________________
    await create_db_and_tables()

    redis = await Redis.from_url(
        settings.redis_url,
        decode_responses=True
    )

    app.state.redis = redis
    app.state.manager = manager
    
    app.state.listener_task = asyncio.create_task(redis_listener(app))

    print("Startup complete")
    yield
    
    app.state.listener_task.cancel()
    await redis.aclose()
    print("Shutdown complete")

async def redis_listener(app: FastAPI):
    redis = app.state.redis
    manager = app.state.manager
    pubsub = redis.pubsub()
    await pubsub.psubscribe("notification:*")
    async for msg in pubsub.listen():
        if msg["type"] == "pmessage":
            user_id = int(msg["channel"].split(":")[1])
            payload = json.loads(msg["data"])
            await manager.send_to_user(user_id, payload)

setup_logging()

app = FastAPI(lifespan=lifespan)

app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="uploads")

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(RequestIDMiddleWare)
app.add_middleware(RequestLoggingMiddleWare)
app.include_router(auth.router, prefix="/api")
app.include_router(job.router, prefix="/api")
app.include_router(application.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(company.router, prefix="/api")
app.include_router(health.router)