from sqlalchemy.orm import Session
from src.models.setup_tenant import SetupTenant
from src.schemas.tenant_schema import TenantCreate, TenantUpdate
from sqlalchemy import text
from src.repository.master_repository import UserRepository
from datetime import datetime
from src.utils import logger
from .Sql import TenantSql

class TenantRepository:

    @staticmethod
    def get_all(db: Session):
        try:
            result = db.execute(text(TenantSql.GetAllTenants))
            tenants = result.fetchall()
            return [SetupTenant(**row._mapping) for row in tenants ]
        except Exception as e:
            logger.logging_error(f"Error fetching all tenants: {str(e)}")
            return []

    @staticmethod
    def get_by_id(tenant_id: int, db: Session):
        result = db.execute(text(TenantSql.GetTenantById), {"id": tenant_id}).fetchone()
        if result:
            return SetupTenant(**result._mapping)
        return None

    @staticmethod
    def create(db: Session, tenant_data: TenantCreate, created_by: int, created_on: datetime):
        try:
            db.execute(text(TenantSql.CreateTenant), {
                "TenantId": tenant_data.TenantId,
                "ServerName": tenant_data.ServerName,
                "DatabaseName": tenant_data.DatabaseName,
                "ServerUsername": tenant_data.ServerUsername,
                "ServerPassword": tenant_data.ServerPassword,
                "CreatedBy": created_by,
                "CreatedOn": created_on,
                "IsDeleted": False
            })
            db.commit()

            # Fetch and return the newly created tenant
            result = db.execute(text(TenantSql.Get_Teant_By_TenantId), {
                "TenantId": tenant_data.TenantId
            }).fetchone()

            return SetupTenant(**result._mapping) if result else None

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def update(db, tenant_id: int, tenant_data: TenantUpdate, session_username: str, updated_by: int, current_time):
        try:
            # Optional: Check if the tenant exists
            result = db.execute(text(TenantSql.Get_Teant_By_TenantId), {"TenantId": tenant_id})
            existing_tenant = result.fetchone()
            if not existing_tenant:
                return None

            # Perform the update
            db.execute(text(TenantSql.Update_Tenant), {
                "ServerName": tenant_data.ServerName,
                "DatabaseName": tenant_data.DatabaseName,
                "ServerUsername": tenant_data.ServerUsername,
                "ServerPassword": tenant_data.ServerPassword,
                "UpdatedBy": updated_by,
                "UpdatedOn": current_time,
                "TenantId": tenant_id
            })
            db.commit()

            # Fetch and return updated tenant
            updated_result = db.execute(text(TenantSql.Get_Teant_By_TenantId), {"TenantId": tenant_id}).fetchone()
            return SetupTenant(**updated_result._mapping) if updated_result else None

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(tenant_id: int, db: Session, updated_by: int, current_time: datetime):
        try:
            # 1. Check if tenant exists
            result = db.execute(text(TenantSql.Get_Teant_By_TenantId), {"TenantId": tenant_id})
            tenant = result.fetchone()
            if not tenant:
                return None 
            

            # 2. Soft delete the tenant (set IsDeleted = True)
            db.execute(text(TenantSql.TenantSoftDelete), {
                "IsDeleted": True,
                "UpdatedBy": updated_by,
                "UpdatedOn": current_time,
                "TenantId": tenant_id
            })
            db.commit()

            # 3. Return success message after deletion
            return True
        
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Delete Tenant: {str(e)}")
           
