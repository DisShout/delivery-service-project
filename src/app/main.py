from fastapi import FastAPI
from src.app.core.middleware import SessionMiddleware
from src.app.routes.parcel import router as parcel_router
from src.app.routes.parcel_type import router as parcel_type_router
from src.app.routes.health_check import router as health_check_router


app = FastAPI()

app.add_middleware(SessionMiddleware)

app.include_router(parcel_router)
app.include_router(parcel_type_router)
app.include_router(health_check_router)
