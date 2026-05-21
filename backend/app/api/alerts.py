from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.alert import Alert


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
async def get_alerts(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Alert).order_by(
            Alert.created_at.desc()
        )
    )

    alerts = result.scalars().all()

    return alerts