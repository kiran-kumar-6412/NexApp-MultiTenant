import jwt
from datetime import timedelta,datetime
from src.config.config import settings
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from fastapi import HTTPException,status,Depends,Request
from src.schemas.user import TokenData
from sqlalchemy.orm import Session
from src.utils import Retun_Response




SECRETE_KEY=settings.SECRET_KEY
EXPIRE_TIME_MINUTES=settings.EXPIRE_TIME_MINUTES
ALGORITHM=settings.ALGORITHM

def create_token(data:dict):
    try:
        to_encode=data.copy()
        expire=datetime.utcnow()+timedelta(EXPIRE_TIME_MINUTES)
        to_encode.update({'exp':expire})
        access_token=jwt.encode(to_encode,SECRETE_KEY,algorithm=ALGORITHM)
        return (access_token)
    except Exception as e:
        from src.utils import logger
        logger.logging_error(f"Token Create Error {str(e)}")


def verify_token(request:Request):
    token=request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token missing Please login again")

    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )
        return TokenData(username=username) # Successfully authenticated

    except ExpiredSignatureError:
        from src.utils import logger
        logger.logging_error("Token Expired")
        raise HTTPException(
            status_code=401,
            detail="Session expired. Please log in again."
        )

    except InvalidTokenError:
        from src.utils import logger
        logger.logging_error("Token ERROR Invalid Token")
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )