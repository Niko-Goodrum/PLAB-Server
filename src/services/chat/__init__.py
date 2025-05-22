import logging
import uuid
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import Optional

from src.models.chat import Chat
from src.routers.interview.enums import InterviewType
from src.schemas.interview import CreateInterviewRequest, EditInterviewRequest


class ChatService:
    async def create_chat(self, user_id: uuid.UUID, type: str, last_question: str, session: AsyncSession):

        chat_dict: dict[str, Any] = {
            "last_question": last_question,
            "type": type,
            "user_id": user_id
        }

        new_chat = Chat(**chat_dict)

        session.add(new_chat)

        await session.flush()
        await session.commit()

        return new_chat

    async def get_chat_by_id(self, chat_id: uuid.UUID, session: AsyncSession) -> Optional[Chat]:
        try:
            statement = select(Chat).where(Chat.id == chat_id)
            result = await session.exec(statement)
            chat = result.first()
            return chat

        except Exception as e:
            logging.exception(msg=e)
            return None

    async def update_chat(self, chat_id, type: InterviewType, last_question: str, session: AsyncSession):
        chat = await self.get_chat_by_id(chat_id, session)

        if type is not None:
            chat.type = type.value


        chat.last_question = last_question

        await session.flush()

        await session.commit()
        await session.refresh(chat)

        return chat


    async def get_chats_by_user_id(self, user_id: uuid.UUID, session: AsyncSession):
        try :
            statement = select(Chat).where(Chat.user_id == user_id)
            result = await session.exec(statement)
            return result

        except Exception as e:
            return []