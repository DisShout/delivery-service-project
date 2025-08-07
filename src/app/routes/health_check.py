from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.app.core.database import get_db

router = APIRouter(prefix="/health", tags=["HealthCheck"])


@router.get("/")
async def health():
    return {"status": "ok"}


@router.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
