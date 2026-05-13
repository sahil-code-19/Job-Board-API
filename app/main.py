from fastapi import FastAPI
from .routers import job

app = FastAPI()

app.include_router(job.router, prefix="/api", tags=["job"])