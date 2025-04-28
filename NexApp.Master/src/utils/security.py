from passlib.context import CryptContext
from src.utils import logger

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.logging_error(f"Error Hashing password {str(e)}")
        return None
def verify_password(plain_password,hashed_passsword):
    try:
        return pwd_context.verify(plain_password,hashed_passsword)
    except Exception as e:
        logger.logging_error(f"Error verify password {str(e)}")
        return False
