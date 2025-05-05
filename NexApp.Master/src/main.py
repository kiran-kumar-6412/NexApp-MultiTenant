from fastapi import FastAPI
from src.routes import MaterRoute  # ✅ Absolute Import
from src.models.base import Base
from src.database import engine

app=FastAPI()


try:
    Base.metadata.create_all(bind=engine)  # ✅ Creates tables if not exist
    app.include_router(MaterRoute.router)  # ✅ Include API routes
    
except Exception as e:
    from src.utils import logger
    logger.logging_error(f"Error initializing application: {str(e)}")
    raise RuntimeError("An unexpected error occurred during application initialization.")