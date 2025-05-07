from fastapi import APIRouter,Depends,Response
from src.dependencies import get_db
from sqlalchemy.orm import Session
from src.schemas.user import Setup_User,Login,UserActionSchema
from src.services import user_services
from fastapi.security import OAuth2PasswordRequestForm



route=APIRouter()

# @route.post("/register")
# def register(user:Setup_User,db:Session=Depends(get_db)):
#     return user_services.user_create(user,db)

@route.post("/login")
def login(form_data:Login,response:Response,db:Session=Depends(get_db)):
    return user_services.login(form_data,response,db)


@route.get("/all")
def get_users(current_user : str = Depends(user_services.current_user),db: Session = Depends(get_db)):  
    return user_services.get_all_users(current_user,db)


@route.post("/user/{id}")
def create_or_update_user(id:int,data:UserActionSchema,session_user:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    #print("Current User:", session_user)
    return user_services.create_or_update_user(id,data,session_user,db)

@route.delete("/user/id")
def user_delete(id:int,session_username:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    return user_services.user_delete(id,session_username,db)