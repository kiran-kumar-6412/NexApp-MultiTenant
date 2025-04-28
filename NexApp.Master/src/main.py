from fastapi import FastAPI
from src.routes import MaterRoute  # ✅ Absolute Import
from src.routes import TenantRoute
from src.models.base import Base
from src.database import engine

app=FastAPI()


try:
    Base.metadata.create_all(bind=engine)  # ✅ Creates tables if not exist
    app.include_router(MaterRoute.router)  # ✅ Include API routes
    app.include_router(TenantRoute.router)
except Exception as e:
    raise str(e)