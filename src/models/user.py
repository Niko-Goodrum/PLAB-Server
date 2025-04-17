import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field
from async_sqlmodel import AsyncSQLModel

from src.models.base_uuid_model import BaseUUIDModel



class UserBase(AsyncSQLModel):

    username: str = Field(nullable=False)
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )

class User(BaseUUIDModel, UserBase, table=True):
    __tablename__ = "users"

    def __repr__(self) -> str:
        return f"<User {self.username}, email={self.email}, uuid={self.id}>"
