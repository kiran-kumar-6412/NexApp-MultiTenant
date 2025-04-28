from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.schemas.tenant_schema import TenantUpdate, TenantBase, TenantCreate
from src.services.tenant_service import TenantService
from src.services import user_services

route = APIRouter()

@route.get("/")
def get_all(
    current_user: str = Depends(user_services.current_user),
    db: Session = Depends(get_db)
):
    return TenantService.get_all(db)

@route.post("/")
def create(
    schema: TenantCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(user_services.current_user)
):
    return TenantService.create(schema, current_user, db)

@route.put("/{tenant_id}")
def update(
    tenant_id: int,
    schema: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(user_services.current_user)
):
    return TenantService.update(tenant_id, schema, current_user, db)

@route.delete("/{tenant_id}")
def delete(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(user_services.current_user)):
    return TenantService.delete(tenant_id, current_user, db)
