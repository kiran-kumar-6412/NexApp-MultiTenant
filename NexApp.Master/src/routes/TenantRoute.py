from fastapi import APIRouter
from src.controller.tenant_controller import route as tenant_router
import src.utils.logger as logger



router = APIRouter()

try:
    router.include_router(tenant_router, tags=["tenant"], prefix="/tenant")
except Exception as e:
    error_msg = f"Error Including tanent Routes: {str(e)}"
    logger.logging_error(error_msg)
    raise RuntimeError(error_msg)  # 🚀 Raise the error so FastAPI fails early
