from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from . import models
from .routers import job

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(job.router, prefix="/api", tags=["job"])