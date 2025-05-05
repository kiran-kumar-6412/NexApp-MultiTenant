from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Setup_User(BaseModel):
    IsDeleted: bool = False
    Username: str
    Password: str
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    UpdatedBy: Optional[int] = None
    UpdatedOn: Optional[datetime] = None

class Login(BaseModel):
    Username:str
    Password:str





class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str


class User_update(BaseModel):
    Username: Optional[str]
    IsDeleted: bool=False
   
  


class UserActionSchema(BaseModel):
    create_data: Optional[Setup_User] = None
    update_data: Optional[User_update] = None