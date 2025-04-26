import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field

from src.models.uuid import BaseUUIDModel
from src.schemas import BaseDictModel


class ChatBase(BaseDictModel):
    user_id: uuid.UUID = Field(
        nullable=False,
    )
    last_question: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    type: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))


class Chat(BaseUUIDModel, ChatBase, table=True):
    __tablename__ = "chats"

    def __repr__(self) -> str:
        return f"<Chat last_answer={self.last_answer}, uuid={self.id}>"
