import shutil
import os

from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated, List

from ..database import get_db
from ..models.application import ApplicationStatus, Application
from ..models.user import User
from ..crud.application import apply_job
from ..auth.dependencies import get_current_user
from ..service.email import send_email

router = APIRouter(prefix="/application", tags=["application"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/apply", status_code=status.HTTP_201_CREATED)
async def create_application(file: Annotated[UploadFile, File(description="A file read as UploadFile")], background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db), job_id: int = Form(), current_user: User = Depends(get_current_user), cover_letter: str = Form(default=None)):
    ALLOWED_TYPES = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF or Word documents allowed"
        )
    
    file_location = f"{UPLOAD_DIR}/{file.filename}"

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    file_size = 0

    with open(file_location, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                buffer.close()
                os.remove(file_location)
                raise HTTPException(status_code=400, detail="File too large")

            buffer.write(chunk)

    application = await apply_job(db, file_location, current_user.id, job_id, cover_letter)

    if application:
        background_tasks.add_task(
        send_email,
        "delivered@resend.dev",
        f"Welcome",
        "You have applied successfully 🚀"
    )
        return application
    
    raise HTTPException(
        status_code=400,
        detail="Can't apply! try again."
    )
