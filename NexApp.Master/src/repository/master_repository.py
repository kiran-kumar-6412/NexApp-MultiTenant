from src.models.user import SetupUser
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from src.utils import logger
from datetime import datetime
from src.utils.query_loader import Queries


class UserRepository:
    @staticmethod
    def check_username(username: str, db: Session):
        try:
            sql = Queries["user"]["GetUsername"]
            result = db.execute(text(sql), {"username": username})
            return {"username_exists": result.first()}
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
            sql = Queries["user"]["GetUsername"]
            result = db.execute(text(sql), {"username": username})
            row = result.fetchone()
            return SetupUser(**row._mapping) if row else None
        except Exception as e:
            logger.logging_error(f"Login Error: {str(e)}")

    @staticmethod
    def all_users(db: Session):
        try:
            sql = Queries["user"]["GetAllUsers"]
            result = db.execute(text(sql))
            users = result.fetchall()
            return [SetupUser(**row._mapping) for row in users]
        except Exception as e:
            logger.logging_error(f"Error getting all users: {str(e)}")

    @staticmethod
    def get_user_id_by_username(username: str, db: Session):
        sql = Queries["user"]["GetUseridfromUsername"]
        result = db.execute(text(sql), {"username": username}).fetchone()
        return result.Id if result else None

    @staticmethod
    def update_user(id, schema_user, session_username, db: Session):
        try:
            sql_get_user = Queries["user"]["GetUserById"]
            user = db.execute(text(sql_get_user), {"id": id}).fetchone()
            
            if not user:
                return None

            # Optional: Check if username already exists
            sql_check_username = Queries["user"]["CheckUsername"]
            result = db.execute(text(sql_check_username), {
                "Username": schema_user.Username,
                "id": id
            })
            if result.fetchone():
                return ValueError("Username already taken. Please use a different one.")

            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            current_time = datetime.utcnow()

            sql_update = Queries["user"]["UpdateUser"]
            db.execute(text(sql_update), {
                "Username": schema_user.Username,
                "UpdatedBy": updated_by,
                "UpdatedOn": current_time,
                "id": id
            })
            db.commit()

            updated_result = db.execute(text(sql_get_user), {"id": id}).first()
            return SetupUser(**updated_result._mapping)
        
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Update User: {str(e)}")

    @staticmethod
    def user_delete(id, session_username, db: Session):
        try:
            sql_get_user = Queries["user"]["GetUserById"]
            user = db.execute(text(sql_get_user), {"id": id}).first()

            if not user:
                return None

            updated_by = UserRepository.get_user_id_by_username(session_username, db)
            updated_on = datetime.utcnow()

            sql_delete = Queries["user"]["SoftDeleteUser"]
            db.execute(text(sql_delete), {
                "UpdatedBy": updated_by,
                "UpdatedOn": updated_on,
                "IsDeleted": 1, 
                "id": id
            })
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            logger.logging_error(f"Delete User: {str(e)}")
            return False  # Explicitly return False on error
