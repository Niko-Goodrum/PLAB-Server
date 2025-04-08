from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.schemas import BaseResponse
from fastapi.encoders import jsonable_encoder


def add_validation_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def invalid_token_handler(request: BaseModel, exc: RequestValidationError):
        return JSONResponse(status_code=422, content=BaseResponse(message="유효성 오류").model_dump())
