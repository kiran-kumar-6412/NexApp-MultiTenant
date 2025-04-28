from sqlalchemy.orm import Session
from src.repository.tenant_repository import TenantRepository
from src.schemas.tenant_schema import TenantCreate, TenantUpdate
from src.repository.master_repository import UserRepository
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from src.utils import logger  # Assuming you have a logger utility

class TenantService:

    @staticmethod
    def get_all(db: Session):
        try:
            tenant = TenantRepository.get_all(db)
            if tenant:
                tenants = [{"TenantId": tenant_data.TenantId,
                            "ServerName": tenant_data.ServerName,
                            "DatabaseName": tenant_data.DatabaseName,
                            "ServerUsername": tenant_data.ServerUsername,
                            "ServerPassword": tenant_data.ServerPassword,
                            "CreatedBy": tenant_data.CreatedBy,
                            "CreatedOn": tenant_data.CreatedOn,
                            "UpdatedBy": tenant_data.UpdatedBy,
                            "UpdatedOn": tenant_data.UpdatedOn} for tenant_data in tenant]
                
                return {"data": jsonable_encoder(tenants),
                        "status": True,
                        "message": "All tenant details"}
            else:
                # If no tenants are found, return an appropriate response
                return {
                    "data": None,
                    "status": False,
                    "message": "No tenants found"
                }
        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error fetching all tenants: {str(e)}")
            return {
                "data": None,
                "status": False,
                "message": "Error fetching tenant details"
            }

    @staticmethod
    def create(tenant_data, session_username, db: Session):
        try:
            created_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()

            created_tenant = TenantRepository.create(db, tenant_data, created_by, current_time)
        
            if created_tenant:
                tenant_dict = {
                    "TenantId": created_tenant.TenantId,
                    "ServerName": created_tenant.ServerName,
                    "DatabaseName": created_tenant.DatabaseName,
                    "ServerUsername": created_tenant.ServerUsername,
                    "ServerPassword": created_tenant.ServerPassword,
                    "CreatedBy": created_tenant.CreatedBy,
                    "CreatedOn": created_tenant.CreatedOn
                }
                return {
                    "data": jsonable_encoder(tenant_dict),
                    "status": True,
                    "message": "Tenant created successfully!"
                }

            return {
                "data": None,
                "status": False,
                "message": "Tenant creation failed"
            }
        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error creating tenant: {str(e)}")
            return {
                "data": None,
                "status": False,
                "message": "Error creating tenant"
            }

    @staticmethod
    def update(tenant_id, tenant_data: TenantUpdate, session_username: str, db: Session):
        try:
            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()

            # Call repository function with everything it needs
            tenant_update = TenantRepository.update(db, tenant_id, tenant_data, session_username, updated_by, current_time)
            
            if not tenant_update:
                return {
                    "data": None,
                    "status": False,
                    "message": f"Tenant not found"
                }
            
            tenant_dict = {
                "ServerName": tenant_update.ServerName,
                "DatabaseName": tenant_update.DatabaseName,
                "ServerUsername": tenant_update.ServerUsername,
                "ServerPassword": tenant_update.ServerPassword,
                "UpdatedBy": tenant_update.UpdatedBy,
                "UpdatedOn": tenant_update.UpdatedOn
            }
            
            return {
                "data": jsonable_encoder(tenant_dict),
                "status": True,
                "message": "Tenant updated successfully"
            }
        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error updating tenant: {str(e)}")
            return {
                "data": None,
                "status": False,
                "message": "Error updating tenant"
            }

    @staticmethod
    def delete(tenant_id: int,session_username, db: Session):
        try:
            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()
            return TenantRepository.delete(tenant_id, db,updated_by,current_time)
        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error deleting tenant with ID {tenant_id}: {str(e)}")
            return {
                "data": None,
                "status": False,
                "message": "Error deleting tenant"
            }
