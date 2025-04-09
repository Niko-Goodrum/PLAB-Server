from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.routers.auth.exceptions import UserAlreadyExists, InvalidToken, InvalidCredentials, AccessTokenRequired, RefreshTokenRequired
from src.schemas import BaseResponse
from fastapi.encoders import jsonable_encoder


def add_auth_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: BaseModel, exc: InvalidToken):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=BaseResponse(message="토큰이 유효하지 않습니다.").to_dict())

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(request: BaseModel, exc: UserAlreadyExists):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=BaseResponse(message="이미 존재하는 사용자입니다").to_dict())

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request: BaseModel, exc: InvalidCredentials):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=BaseResponse(message="사용자를 찾을 수 없습니다.").to_dict())

    @app.exception_handler(AccessTokenRequired)
    async def access_token_handler(request: BaseModel, exc: AccessTokenRequired):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=BaseResponse(message="액세스 토큰이 필요합니다.").to_dict())

    @app.exception_handler(RefreshTokenRequired)
    async def refresh_token_handler(request: BaseModel, exc: RefreshTokenRequired):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=BaseResponse(message="리프레시 토큰이 필요합니다.").to_dict())