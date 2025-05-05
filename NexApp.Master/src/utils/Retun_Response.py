from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any

def error_response(message:str,status_code:int=status.HTTP_400_BAD_REQUEST,data:Any=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "data" : data,
            "status" : False,
           "message" : message
        }
    )

def success_response(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content={
            "data": data,
            "status": True,
            "message": message
        }
    )