from src.models.user import SetupUser
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from src.utils import logger
from datetime import datetime
from .Sql import MasterSql



class UserRepository:
    @staticmethod
    def check_username(username: str, db: Session):
        try:
            result = db.execute(text(MasterSql.GetUsername),
                                {"username": username})
            username_result = result.first()
            return {
                "username_exists": username_result
            }
        except Exception as e:
            logger.logging_error(f"Username check error: {str(e)}")

    @staticmethod
    def create_user(user: dict, db: Session):
        try:
            user_obj = SetupUser(**user)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Error creating user: {str(e)}")

    @staticmethod
    def login(username: str, db: Session):
        try:
            result = db.execute(text(MasterSql.GetUsername), {"username": username})
            row = result.fetchone()

            if row:
                user = SetupUser(**row._mapping)
                return user

            return None

        except Exception as e:
            logger.logging_error(f"Login Error: {str(e)}")

    @staticmethod
    def all_users(db: Session):
        try:
            result = db.execute(text(MasterSql.GetAllusers))
            users = result.fetchall()
            return [SetupUser(**row._mapping) for row in users]
        except Exception as e:
            logger.logging_error(f"Error getting all users: {str(e)}")

    @staticmethod
    def get_user_id_by_username(username: str, db: Session):
        result = db.execute(text(MasterSql.GetUseridfromUsername),
                            {"username": username}).fetchone()
        return result.Id if result else None

    @staticmethod
    def update_user(id, schema_user, session_username, db: Session):
        try:
            # 1. Check if user exists
            result = db.execute(text(MasterSql.GetUserById), {"id": id})
            user = result.fetchone()
            if not user:
                return None

            # 2. Check if username is taken by another user
            result = db.execute(text(
                MasterSql.CheckUsername
            ), {"Username": schema_user.Username, "id": id})
            if result.fetchone():
                return {
                    "data": None,
                    "status": False,
                    "message": "Username already taken. Please use a different one."
                }

            # 3. Prepare updated values
            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()

            # 4. Update user
            db.execute(text(MasterSql.UpdateUser), {
                "Username": schema_user.Username,
                "IsDeleted": schema_user.IsDeleted,
                "UpdatedBy": updated_by,
                "UpdatedOn": current_time,
                "id": id
            })
            db.commit()

            # 5. Fetch and return updated user
            updated_result = db.execute(text(MasterSql.GetUserById),
                                        {"id": id}).first()
            return SetupUser(**updated_result._mapping)
        except IntegrityError as e:
            db.rollback()
            if "Duplicate entry" in str(e.orig):
                return {
                    "data": None,
                    "status": False,
                    "message": "Username already taken. Please use a different one."
                }
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Update User: {str(e)}")
            return {
                "data": None,
                "status": False,
                "message": f"Update failed: {str(e)}"
            }

    @staticmethod
    def user_delete(id,session_username, db: Session):
        try:
            result = db.execute(text(MasterSql.GetUserById), {"id": id})
            if not result.first():
                return {
                    "data": None,
                    "status": False,
                    "message": f"User with ID {id} not found in the database"
                }
            UpdatedBy=UserRepository.get_user_id_by_username(session_username,db)
            UpdatedOn=datetime.utcnow()

            db.execute(text(MasterSql.SoftDeleteUser), {"UpdatedBy":UpdatedBy,"UpdatedOn":UpdatedOn,"id": id})
            db.commit()
            return {
                "data": True,
                "status": True,
                "message": f"User with ID {id} has been successfully deleted"
            }
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Delete User: {str(e)}")
