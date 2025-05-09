import logging
import uuid
from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User
from src.schemas.user import CreateUserRequest
from src.routers.auth.utils import generate_password_hash



class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            user = result.first()
            return user

        except Exception as e:
            logging.exception(msg=e)
            return None


    async def get_user_by_id(self, user_uuid: uuid.UUID, session: AsyncSession):
        statement = select(User).where(User.id == user_uuid)

        result = await session.exec(statement)

        user = result.scalars().first()

        return user


    async def create_user(self, user_data: CreateUserRequest, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_password_hash(user_data.password)

        session.add(new_user)

        await session.flush()
        await session.commit()

        return new_user

    async def update_user(self, user: User, user_date: dict, session: AsyncSession):
        for k, v in user_date.items():
            setattr(user, k, v)

        await session.flush()

        await session.commit()
        await session.refresh(user)

        return user
