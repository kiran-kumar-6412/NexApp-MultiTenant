from src.repository.master_repository import UserRepository
from src.utils.security import hash_password, verify_password
from src.utils.token import create_token,verify_token
from src.utils import logger
#from src.utils.token import create_token, verify_token
from fastapi import HTTPException, status, Depends
from src.schemas.user import Setup_User,TokenData
from sqlalchemy.orm import Session
import json
from fastapi.encoders import jsonable_encoder
from datetime import datetime


def user_create(user,session_user,db):
    try:
        user_data = user.dict()

        # Check username/email uniqueness
        verify = UserRepository.check_username(user_data["Username"], db)
        if verify["username_exists"]:
            return {
                "data": None,
                "status": False,
                "message": "Username already taken"
            }
    

        # Hash password
        user_data["Password"] = hash_password(user_data["Password"])
        user_data["CreatedBy"] = UserRepository.get_user_id_by_username(session_user,db)
        user_data["CreatedOn"]=datetime.utcnow()

        # Create user
        created_user = UserRepository.create_user(user_data, db)

        if created_user:
            user_dict = {
                "id": created_user.Id,
                "isdeleted": created_user.IsDeleted,
                "username": created_user.Username,
                "CreatedBy": created_user.CreatedBy,
                "CreatedOn": created_user.CreatedOn
            
            }
            return {
                "data": jsonable_encoder(user_dict),
                "status": True,
                "message": "User created successfully!"
            }

        return {
            "data": None,
            "status": False,
            "message": "User creation failed"
        }
    except Exception as e:
        logger.logging_error(f"User Create Error {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")
    

def login(user,db):
    try:
        username = user.username
        password = user.password

        user_record = UserRepository.login(username, db)
        if not user_record:
            return {
                "data": None,
                "status": False,
                "message": "User not found"
            }

        if not verify_password(password, user_record.Password):
            return {
                "data": None,
                "status": False,
                "message": "Invalid credentials"
            }

        if user_record.IsDeleted:
            return {
                "data": None,
                "status": False,
                "message": "User is not active"
            }
        access_token = create_token({"sub": user_record.Username})
        return {
                
                "access_token": access_token,
                "token_type": "bearer"
                         ,
            "status": True,
            "message": "Login successful"
        }


    except Exception as e:
        logger.logging_error(f"Login error: {str(e)}")
        return {
            "data": None,
            "status": False,
            "message": f"loggin Error{str(e)}"
        }






def get_all_users(current_user,db: Session):
    try:
        if current_user == "kiran":
            users = UserRepository.all_users(db)
            if users:
                # Convert each User object to a dictionary manually
                users_list = [
                    {
                    "id": user.Id,
                    "isdeleted": user.IsDeleted,
                    "username": user.Username,
                    "CreatedBy": user.CreatedBy,
                    "CreatedOn": user.CreatedOn,
                    "updatedon": user.UpdatedOn,
                    "updatedby": user.UpdatedBy
                    }
                    for user in users
                ]
                return {"data": jsonable_encoder(users_list),
                "status": True,
                "message":"All users details"}
            else:
                # If no users are found, return an appropriate response
                return {
                            "data": None,
                            "status": False,
                            "message": "No users found"
                        }
        return {
        "data": None,
        "status": False,
        "message": f"You are not authorized to see users list"
    }

    except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error fetching all users: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
                






from fastapi.encoders import jsonable_encoder

def update_user(id, schema_user, session_username, db):
    # Only allow master user to perform updates
    if session_username == "kiran":
        user = UserRepository.update_user(id, schema_user, session_username, db)

        if not user:
            return {
                "data": None,
                "status": False,
                "message": f"User with ID {id} not found"
            }

        # Prepare user response
        users_list = [
            {
                "id": user.Id,
                "isdeleted": user.IsDeleted,
                "username": user.Username,
                "updatedon": user.UpdatedOn,
                "updatedby": user.UpdatedBy
            }
        ]

        return {
            "data": jsonable_encoder(users_list),
            "status": True,
            "message": "User updated successfully"
        }

    # Unauthorized update attempt
    return {
        "data": None,
        "status": False,
        "message": f"You are not authorized to update this user. Your username was '{session_username}'"
    }


def user_delete(id,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="kiran":                # only master user can update the user details
        return UserRepository.user_delete(id,db)
       
    
    return {    
                "data": None,
                "status": False,
                "message": "You are not authorized to delete this user"
            }
   

def create_or_update_user(id,data,session_user,db):
    if id <= 0 and data.create_data:
        return user_create(data.create_data,session_user, db)
               
    elif data.update_data:
        return update_user(id, data.update_data, session_user, db)
    else:
        return {    
                "data": None,
                "status": False,
                "message": "Invalid input for create/update."
            }







def current_user(token_data: TokenData = Depends(verify_token)):
    try:
        username= token_data.username
        if username:
            return username
        return {
                "data": None,
                "status": False,
                "message": "Users not found something went wrong"
            }
    except Exception as e:
        logger.logging_error(f"Current User Error {str(e)}")
       


def user_delete(id,session_username,db):
    try:
        if session_username=="kiran":               # only master user can delete the user details
            return UserRepository.user_delete(id,session_username,db)
        
        
        return {    
                    "data": None,
                    "status": False,
                    "message": "You are not authorized to delete this user"
                }
    except Exception as e:
        logger.logging_error(f"user delete Error {str(e)}")