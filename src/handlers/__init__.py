import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

from src.schemas import BaseResponse
from fastapi.encoders import jsonable_encoder


def add_validation_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def invalid_token_handler(request: BaseModel, exc: RequestValidationError):
        print(exc.errors())
        return JSONResponse(status_code=422, content=BaseResponse(message="잘못된 접근입니다.").to_dict())

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: BaseModel, exc: ValidationError):
        print(exc)
        return JSONResponse(status_code=500, content=BaseResponse(message="서버에 잘못된 값이 들어왔습니다.").to_dict())

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: BaseModel, exc: StarletteHTTPException):
        message: str = exc.detail

        if exc.status_code == HTTP_405_METHOD_NOT_ALLOWED:
            message="허용되지 않은 메소드입니다."


        return JSONResponse(
            status_code=exc.status_code,
            content=BaseResponse(
                message=message
            ).to_dict()
        )
