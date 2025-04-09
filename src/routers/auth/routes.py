from datetime import timedelta, datetime

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user,
)
from .exceptions import UserAlreadyExists, InvalidCredentials, InvalidToken
from src.schemas.user import CreateUserRequest, SigninRequest, UserResponse, RefreshRequest
from .service import UserService
from .utils import create_access_token, verify_password
from ...config import Config
from ...db.main import get_session
from src.schemas import BaseResponse

auth_router = APIRouter(prefix="/auth", responses={
    200: {
        "model": BaseResponse
    },
    422: {
        "model": BaseResponse
    }
})
user_service = UserService()


@auth_router.post("/signup", response_model=BaseResponse)
async def signup(
        user_data: CreateUserRequest,
        bg_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_access_token({"email": email})

    return JSONResponse(status_code=201, content=BaseResponse(message="회원가입이 완료되었습니다.").to_dict()())


@auth_router.post("/signin", response_model=BaseResponse)
async def signin(
        user_data: SigninRequest,
        bg_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_is_valid = verify_password(password, user.password_hash)

        if password_is_valid:
            access_token = create_access_token(
                user_data={
                    "email": email,
                    "user_uuid": str(user.id),
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": email,
                    "user_uuid": str(user.id),
                },
                refresh=True,
                expiry=timedelta(hours=Config.REFRESH_EXPIRY)
            )

            return JSONResponse(
                status_code=200,
                content=BaseResponse(
                    message="로그인이 성공했습니다.",
                    data=UserResponse(
                        access_token=access_token,
                        refresh_token=refresh_token
                    ).to_dict()).to_dict()
            )

    raise InvalidCredentials()


@auth_router.post("/refresh")
async def refresh(
        request: RefreshRequest,
        token_details: dict = Depends(AccessTokenBearer())
):
    expiry_timestamp = token_details["exp"]

    RefreshTokenBearer().verify_token_data(token_data=request)

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(status_code=HTTP_200_OK, content=BaseResponse(
            message="리프레시가 성공했습니다.",
            data=UserResponse(
                access_token=new_access_token,
                refresh_token=request.refresh_token
            ).to_dict()
        ).to_dict())


    raise InvalidToken
