from typing import List, TYPE_CHECKING, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship

from src.models.uuid import BaseUUIDModel
from src.schemas import BaseDictModel
if TYPE_CHECKING:
    from src.models.chat import Chat
    from src.models.portfolio import Portfolio

class UserBase(BaseDictModel):

    username: str = Field(nullable=False)
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )

class User(BaseUUIDModel, UserBase, table=True):
    __tablename__ = "users"

    chats: List["Chat"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    portfolio: Optional["Portfolio"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self) -> str:
        return f"<User {self.username}, email={self.email}, uuid={self.id}>"
