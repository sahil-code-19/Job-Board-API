from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.company import CompanyCreate
from ..models.company import Company
from ..auth.dependencies import get_current_user


router = APIRouter(prefix="/company")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data_dict = data.model_dump()

    data_dict["owner_id"] = current_user.id

    company = Company(**data_dict)
    await db.add(company)
    await db.commit()
    await db.refresh(company)
    return company
