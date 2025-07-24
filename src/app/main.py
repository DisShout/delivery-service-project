# src/app/main.py
from fastapi import FastAPI, Depends
from src.app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.app.core.database import get_db

app = FastAPI()


@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}