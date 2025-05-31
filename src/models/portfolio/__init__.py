import uuid
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship

from src.models.user import User

from src.models.uuid import BaseUUIDModel
from src.schemas import BaseDictModel

class PortfolioBase(BaseDictModel):
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", unique=True)
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    phone_num: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    user_image: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))


class Portfolio(BaseUUIDModel, PortfolioBase, table=True):
    __tablename__ = "portfolio"

    user: Optional[User] = Relationship(back_populates="portfolio")

    def __repr__(self) -> str:
        return f"<Portfolio id={self.id}>"
