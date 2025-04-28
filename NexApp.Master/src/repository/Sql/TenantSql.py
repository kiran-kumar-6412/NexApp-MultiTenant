GetAllTenants = "SELECT * FROM setup_tenant WHERE IsDeleted = 0"
GetTenantById="SELECT * FROM setup_tenant WHERE Id = :id AND IsDeleted = 0"
CreateTenant=""" 
                INSERT INTO setup_tenant (
                    TenantId, ServerName, DatabaseName, ServerUsername, ServerPassword,
                    CreatedBy, CreatedOn,IsDeleted
                ) VALUES (
                    :TenantId, :ServerName, :DatabaseName, :ServerUsername, :ServerPassword,
                    :CreatedBy, :CreatedOn, :IsDeleted
                )
            """
Get_Teant_By_TenantId="SELECT * FROM setup_tenant WHERE TenantId = :TenantId AND IsDeleted = 0"
Update_Tenant=""" 
                UPDATE setup_tenant 
                SET ServerName = :ServerName,
                    DatabaseName = :DatabaseName,
                    ServerUsername = :ServerUsername,
                    ServerPassword = :ServerPassword,
                    UpdatedBy = :UpdatedBy,
                    UpdatedOn = :UpdatedOn
                WHERE TenantId = :TenantId
            """
TenantSoftDelete=""" 
                UPDATE setup_tenant
                SET IsDeleted = :IsDeleted,
                    UpdatedBy = :UpdatedBy,
                    UpdatedOn = :UpdatedOn
                WHERE TenantId = :TenantId
            """