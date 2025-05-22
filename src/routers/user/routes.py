import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.db.main import get_session
from src.models.user import User
from src.routers.auth.dependencies import AccessTokenBearer
from src.routers.auth.exceptions import InvalidCredentials
from src.services.chat import ChatService
from src.services.user import UserService
from src.schemas import BaseResponse, BaseListResponse

user_router = APIRouter(prefix="/user", responses={
    200: {
        "model": BaseResponse
    },
    422: {
        "model": BaseResponse
    }
})

user_service = UserService()
chat_service = ChatService()


@user_router.get("", response_model=BaseResponse)
async def get_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
):

    user_data = User(**token_details["user"])
    user = await user_service.get_user_by_email(user_data.email, session=session)

    if user:
        return JSONResponse(BaseResponse(message="유저를 성공적으로 조회했습니다.", data=user.to_dict()).to_dict())

    raise InvalidCredentials()


@user_router.get("/chats", response_model=BaseResponse)
async def get_chats_by_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
):
    user_data = User(**token_details["user"])

    chats = await chat_service.get_chats_by_user_id(user_data.id, session=session)

    if chats:
        return JSONResponse(BaseListResponse(message="채팅을 성공적으로 불러왔습니다.", data=chats).to_dict())

    raise InvalidCredentials()

