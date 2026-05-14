from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from . import models
from .routers import job, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api")
app.include_router(job.router, prefix="/api")