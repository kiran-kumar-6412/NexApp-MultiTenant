from fastapi import APIRouter
from src.controller.master import route as master_router
from src.controller.tenant_controller import route as tenant_router


router = APIRouter()

try:
    router.include_router(master_router, tags=["Master"], prefix="/masters")
    router.include_router(tenant_router, tags=["tenant"], prefix="/tenant")
except Exception as e:
    import src.utils.logger as logger
    error_msg = f"Error Including User Routes: {str(e)}"
    logger.logging_error(error_msg)
    raise RuntimeError(error_msg)  # 🚀 Raise the error so FastAPI fails early
