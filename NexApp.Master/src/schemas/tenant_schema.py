from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TenantBase(BaseModel):
    TenantId: str
    ServerName: str
    DatabaseName: str
    ServerUsername: str
    ServerPassword: str

class TenantCreate(TenantBase):
    # CreatedBy will be set in the backend from the token
    pass

class TenantUpdate(BaseModel):
    ServerName: str
    DatabaseName: str
    ServerUsername: str
    ServerPassword: str

    # UpdatedBy will be set from the token in the backend
    pass

# class TenantOut(TenantBase):
#     Id: int
#     CreatedBy: Optional[int]
#     CreatedOn: Optional[datetime]
#     UpdatedBy: Optional[int]
#     UpdatedOn: Optional[datetime]
#     IsDeleted: bool

    class Config:
        orm_mode = True
