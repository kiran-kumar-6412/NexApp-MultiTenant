from sqlalchemy.orm import Session
from src.repository.tenant_repository import TenantRepository
from src.schemas.tenant_schema import TenantCreate, TenantUpdate
from src.repository.master_repository import UserRepository
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from src.utils import logger,Retun_Response

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
                
                return Retun_Response.success_response(data=jsonable_encoder(tenants),message="All tenant details fetched sucessfully")
            
            else:
                # If no tenants are found, return an appropriate response
                return Retun_Response.error_response("No tenants found")
        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error fetching all tenants: {str(e)}")
            

    @staticmethod
    def create(tenant_data:TenantCreate, session_username, db: Session):
        try:
            verify=TenantRepository.check_tenant_id(tenant_data.TenantId,db)
            if verify["tenant_exists"]:
                return Retun_Response.error_response("TenantId must be Unique")
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
                return Retun_Response.success_response(data=jsonable_encoder(tenant_dict),message="Tenant created successfully!")
               

            return Retun_Response.error_response("Tenant creation failed")
        except Exception as e:
            logger.logging_error(f"Error creating tenant: {str(e)}")
            

    @staticmethod
    def update(tenant_id: int, tenant_data: TenantUpdate, session_username: str, db: Session):
        try:
            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()

            tenant_update = TenantRepository.update(
                db=db,
                tenant_id=tenant_id,
                tenant_data=tenant_data,
                session_username=session_username,
                updated_by=updated_by,
                current_time=current_time
            )

            if not tenant_update:
                return Retun_Response.error_response("Tenant not found")

            tenant_dict = {
                "ServerName": tenant_update.ServerName,
                "DatabaseName": tenant_update.DatabaseName,
                "ServerUsername": tenant_update.ServerUsername,
                "ServerPassword": tenant_update.ServerPassword,
                "UpdatedBy": tenant_update.UpdatedBy,
                "UpdatedOn": tenant_update.UpdatedOn
            }

            return Retun_Response.success_response(
                data=jsonable_encoder(tenant_dict),
                message="Tenant updated successfully"
            )

        except Exception as e:
            logger.logging_error(f"Error updating tenant: {str(e)}")
            return Retun_Response.error_response("Internal server error")
    

    @staticmethod
    def delete(tenant_id: int,session_username, db: Session):
        try:
            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()
            tenant= TenantRepository.delete(tenant_id, db,updated_by,current_time)
            if not tenant:
                return Retun_Response.error_response(f"Tenant with ID {tenant_id} not found in the database")
                
            else:
                return Retun_Response.success_response(data=None,message=f"Tenant with ID {tenant_id} has been successfully deleted")


        except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error deleting tenant with ID {tenant_id}: {str(e)}")
            return Retun_Response.error_response("Error deleting tenant")
