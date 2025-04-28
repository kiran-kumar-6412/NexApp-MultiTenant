from fastapi import APIRouter
from src.controller.master import route as master_router
import src.utils.logger as logger

router = APIRouter()

try:
    router.include_router(master_router, tags=["Master"], prefix="/masters")
except Exception as e:
    error_msg = f"Error Including User Routes: {str(e)}"
    logger.logging_error(error_msg)
    raise RuntimeError(error_msg)  # 🚀 Raise the error so FastAPI fails early
