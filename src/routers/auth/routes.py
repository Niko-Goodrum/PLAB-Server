from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user,
)
from .errors import UserAlreadyExists
from src.schemas.user import CreateUserRequest
from .service import UserService
from .utils import create_access_token
from ...db.main import get_session
from src.schemas import BaseResponse

auth_router = APIRouter()
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

    return JSONResponse({"message": token, "user": new_user})