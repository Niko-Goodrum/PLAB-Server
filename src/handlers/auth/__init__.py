from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.routers.auth.exceptions import UserAlreadyExists, InvalidToken
from src.schemas import BaseResponse
from fastapi.encoders import jsonable_encoder


def add_auth_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: BaseModel, exc: InvalidToken):
        return JSONResponse(status_code=401, content=BaseResponse(message="토큰이 유효하지 않상민띠").model_dump(mode="json"))

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(request: BaseModel, exc: UserAlreadyExists):
        return JSONResponse(status_code=409, content=BaseResponse(message="이미 존재하는 사용자입니다").model_dump(mode="json"))