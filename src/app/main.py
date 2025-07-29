# src/app/main.py
from fastapi import FastAPI, Depends
from src.app.services.currency_service import CurrencyService
from src.app.core.middleware import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.app.core.database import get_db
from src.app.routes.parcel import router as parcel_router
from src.app.routes.parcel_type import router as parcel_type_router


app = FastAPI()
app.add_middleware(SessionMiddleware)

app.include_router(parcel_router)
app.include_router(parcel_type_router)


@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.get("/currency")
async def get_currency():
    return await CurrencyService().get_usd_to_rub()
