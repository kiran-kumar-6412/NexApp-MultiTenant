from sqlalchemy.orm import Session
from src.models.setup_tenant import SetupTenant
from src.schemas.tenant_schema import TenantCreate, TenantUpdate
from sqlalchemy import text
from src.repository.master_repository import UserRepository
from datetime import datetime
from src.utils import logger
from src.utils.query_loader import Queries

class TenantRepository:
    @staticmethod
    def check_tenant_id(id,db:Session):
        try:
            sql=Queries["tenant"]["GetTenant"]
            result=db.execute(text(sql),{"id":id})
            return {"tenant_exists": result.first()}
            
        except Exception as e:
            logger.logging_error(f"check tent id {str(e)}")

    @staticmethod
    def get_all(db: Session):
        try:
            sql = Queries["tenant"]["GetAllTenants"]
            result = db.execute(text(sql))
            tenants = result.fetchall()
            return [SetupTenant(**row._mapping) for row in tenants ]
        except Exception as e:
            logger.logging_error(f"Error fetching all tenants: {str(e)}")
            return []

    @staticmethod
    def get_by_id(tenant_id: int, db: Session):
        sql = Queries["tenant"]["GetTenantByTenantId"]
        result = db.execute(text(sql), {"id": tenant_id}).fetchone()
        if result:
            return SetupTenant(**result._mapping)
        return None

    @staticmethod
    def create(db: Session, tenant_data: TenantCreate, created_by: int, created_on: datetime):
        try:
            sql = Queries["tenant"]["CreateTenant"]
            db.execute(text(sql), {
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
            sql = Queries["tenant"]["GetTenantByTenantId"]
            result = db.execute(text(sql), {
                "TenantId": tenant_data.TenantId
            }).fetchone()

            return SetupTenant(**result._mapping) if result else None

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def update(db: Session, tenant_id: int, tenant_data: TenantUpdate, session_username: str, updated_by: int, current_time):
        try:
            # Check if tenant exists
            sql_get = Queries["tenant"]["GetTenantByTenantId"]
            result = db.execute(text(sql_get), {"TenantId": tenant_id})
            existing_tenant = result.fetchone()
            if not existing_tenant:
                return None

            # Perform update
            sql_update = Queries["tenant"]["UpdateTenant"]
            db.execute(text(sql_update), {
                "ServerName": tenant_data.ServerName,
                "DatabaseName": tenant_data.DatabaseName,
                "ServerUsername": tenant_data.ServerUsername,
                "ServerPassword": tenant_data.ServerPassword,
                "UpdatedBy": updated_by,
                "UpdatedOn": current_time,
                "TenantId": tenant_id
            })
            db.commit()

            # Fetch updated tenant
            updated_result = db.execute(text(sql_get), {"TenantId": tenant_id}).fetchone()
            return SetupTenant(**updated_result._mapping) if updated_result else None

        except Exception as e:
            db.rollback()
            logger.logging_error(f"Update Tenant Repository Error: {str(e)}")
            return None


        @staticmethod
        def delete(tenant_id: int, db: Session, updated_by: int, current_time: datetime):
            try:
                # 1. Check if tenant exists
                sql = Queries["tenant"]["GetTenantByTenantId"]
                result = db.execute(text(sql), {"TenantId": tenant_id})
                tenant = result.fetchone()
                if not tenant:
                    return None 
                

                # 2. Soft delete the tenant (set IsDeleted = True)
                sql = Queries["tenant"]["TenantSoftDelete"]
                db.execute(text(sql), {
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
            
