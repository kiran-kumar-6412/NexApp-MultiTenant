from src.repository.master_repository import UserRepository
from src.utils.security import hash_password, verify_password
from src.utils.token import create_token,verify_token
from src.utils import logger,Retun_Response
from fastapi import HTTPException, status, Depends,Request
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
            return Retun_Response.error_response("Username already taken")
    

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
            return Retun_Response.success_response(data=jsonable_encoder(user_dict),message="User created successfully!",status_code=status.HTTP_201_CREATED)

        return Retun_Response.error_response("User creation failed")
    except Exception as e:
        logger.logging_error(f"User Create Error {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")
    

def login(user,response,db):
    try:
        username = user.Username
        password = user.Password

        user_record = UserRepository.login(username, db)
        if not user_record:
            return Retun_Response.error_response(message="User Not Found",status_code=status.HTTP_404_NOT_FOUND)

        if not verify_password(password, user_record.Password):
            return Retun_Response.error_response("Invalid credentials")

        if user_record.IsDeleted:
            return Retun_Response.error_response("User is not active")
        
        access_token = create_token({"sub": user_record.Username})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict"
        )

        return Retun_Response.success_response(data={"access_token": access_token,
                "token_type": "bearer"},message="Login successful")


    except Exception as e:
        logger.logging_error(f"Login error: {str(e)}")
        






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
                return Retun_Response.success_response(data=jsonable_encoder(users_list),message="All users details")
            
            else:
                # If no users are found, return an appropriate response
                return Retun_Response.error_response(message="No users found",status_code=status.HTTP_404_NOT_FOUND)
        return Retun_Response.error_response("You are not authorized to see users list")

    except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error fetching all users: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
                


def update_user(id, schema_user, session_username, db):
    # Only allow master user to perform updates
    if session_username == "kiran":
        try:
            user = UserRepository.update_user(id, schema_user, session_username, db)
            if not user:
                return Retun_Response.error_response(f"User with ID {id} not found",status_code=status.HTTP_404_NOT_FOUND)

            # If the repository returns a dict, it's an error message
            if isinstance(user, dict):
                return user
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

            return Retun_Response.success_response(data=jsonable_encoder(users_list),message="User updated successfully")
        except ValueError as e:
            return Retun_Response.error_response(str(e))

    # Unauthorized update attempt
    return Retun_Response.error_response("You are not authorized to update this user",status_code=status.HTTP_401_UNAUTHORIZED)




    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="kiran":                # only master user can update the user details
        return UserRepository.user_delete(id,db)
       
    
    return Retun_Response.error_response(message="You are not authorized to delete this user",status_code=status.HTTP_401_UNAUTHORIZED)
   

def create_or_update_user(id,data,session_user,db):
    if id <= 0 and data.create_data:
        return user_create(data.create_data,session_user, db)
               
    elif data.update_data:
        return update_user(id, data.update_data, session_user, db)
    else:
        return Retun_Response.error_response("Invalid input for create/update.")







def current_user(token_data: TokenData = Depends(verify_token)):
    try:
        username= token_data.username
        if username:
            return username
        return Retun_Response.error_response("something went wrong to get Current User")
    except Exception as e:
        logger.logging_error(f"Current User Error {str(e)}")
       


def user_delete(id,session_username,db):
    try:
        if session_username=="kiran":               # only master user can delete the user details
            return UserRepository.user_delete(id,session_username,db)
        
        
        return Retun_Response.error_response(message="You are not authorized to delete this user",status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.logging_error(f"user delete Error {str(e)}")