# coding=utf8
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class CustomHTTPException(Exception):

    def __init__(self,status_code:int,detail:str,err_code:int = None):
        self.status_code = status_code
        self.err_code = err_code
        self.detail = detail

# 自定义异常类
async def custom_http_exception_handler(
        request:Request,
        exc: CustomHTTPException):
    
    return JSONResponse(
        status_code = exc.status_code,
        content = {"msg": exc.detail,"err_code":exc.err_code}
    )

# Pydantic数据验证异常
async def validation_exception_handler(
        request:Request,
        exc: RequestValidationError):
    
    return JSONResponse(
        status_code = 422,
        content = {"msg":"验证错误","details":exc.errors()}
    )

# HTTP异常（权限等）
async def http_exception_handler(
        request:Request,
        exc: StarletteHTTPException):
    
    return JSONResponse(
        status_code = exc.status_code,
        content = {"msg":str(exc.detail)}
    )

# 通用异常
async def general_exception_handler(
        request: Request,
        exc: Exception):
    
    return JSONResponse(
        status_code = 500,
        content = {"msg":"发生了未预期错误"}
    )

def add_exception_handlers(app):

    app.add_exception_handler(CustomHTTPException,custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError,validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException,http_exception_handler)
    app.add_exception_handler(Exception,general_exception_handler)