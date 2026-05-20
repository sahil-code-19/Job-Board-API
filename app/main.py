from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from .core.limiter import limiter

from .database import create_db_and_tables
from . import models
from .routers import job, auth, application, notifications, company
from .middleware.request_logging import RequestLoggingMiddleWare
from .middleware.request_id import RequestIDMiddleWare
from .core.logging_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_db_and_tables()
    yield

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
