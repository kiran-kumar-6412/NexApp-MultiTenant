import jwt
from datetime import timedelta,datetime
from src.config.config import settings
from src.utils import logger
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from fastapi import HTTPException,status,Depends
from src.schemas.user import TokenData
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session




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
        logger.logging_error(f"Token Create Error {str(e)}")

oauth2_schemes = OAuth2PasswordBearer(tokenUrl="/masters/login")

def verify_token(token:str=Depends(oauth2_schemes)):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return TokenData(username=username) # Successfully authenticated

    except ExpiredSignatureError:
        logger.logging_error("Token Expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Expired, please log in again"
        )

    except InvalidTokenError:
        logger.logging_error("Token ERROR Invalid Token")
        # return {    
        #         "data": None,
        #         "status": False,
        #         "message": "Invalid Token"
        #     }
    #     #raise 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )