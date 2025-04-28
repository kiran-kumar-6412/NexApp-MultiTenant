

GetUsername="SELECT * FROM setup_user WHERE Username = :username AND IsDeleted = 0"
GetAllusers="SELECT * FROM setup_user"
GetUseridfromUsername="SELECT Id FROM setup_user WHERE Username = :username AND IsDeleted = 0"
GetUserById="SELECT * FROM setup_user WHERE Id = :id AND IsDeleted = 0"
CheckUsername = """
SELECT * FROM setup_user 
WHERE Username = :Username
AND IsDeleted = 0
"""

UpdateUser="""
                UPDATE setup_user 
                SET Username = :Username,
                    UpdatedBy = :UpdatedBy,
                    UpdatedOn = :UpdatedOn
                WHERE Id = :id
            """
SoftDeleteUser="""
                UPDATE setup_user 
                SET IsDeleted = :True,
                    UpdatedBy = :UpdatedBy,
                    UpdatedOn = :UpdatedOn
                WHERE Id = :id
            """