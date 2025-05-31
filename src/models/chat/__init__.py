import uuid
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship


from src.models.user import User

from src.models.uuid import BaseUUIDModel
from src.schemas import BaseDictModel




class ChatBase(BaseDictModel):
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    last_question: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    type: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))


class Chat(BaseUUIDModel, ChatBase, table=True):
    __tablename__ = "chats"

    user: Optional[User] = Relationship(back_populates="chats")

    def __repr__(self) -> str:
        return f"<Chat uuid={self.id}>"
