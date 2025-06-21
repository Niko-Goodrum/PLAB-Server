import datetime
import uuid
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import Column, Field, Relationship

from src.models.user import User

from src.models.uuid import BaseUUIDModel
from src.schemas import BaseDictModel


class CareerBase(BaseDictModel):
    company_name: str
    part: str
    position: str
    join_date: str
    resign_date: Optional[str] = None
    task: Optional[str] = None
    techs: Optional[List[str]] = None

class ProjectURLBase(BaseDictModel):
    title: str
    link: Optional[str] = None

class ProjectBase(BaseDictModel):
    name: str
    part: str
    start_date: str
    end_date: Optional[str] = None
    task: Optional[str] = None
    urls: Optional[List[ProjectURLBase]] = None
    images: Optional[List[str]] = None
    techs: Optional[List[str]] = None

class GradeBase(BaseDictModel):
    received_grade: float
    max_grade: float

class EducationBase(BaseDictModel):
    school_name: str
    level: str
    status: str
    join_date: str
    resign_date: Optional[str] = None
    major: Optional[str] = None
    grade: Optional[GradeBase] = None
    description: Optional[str] = None

class PortfolioBase(BaseDictModel):
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", unique=True)
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    phone_num: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    email: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    user_image: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    introduce: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    job: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    techs: Optional[List[str]] = Field(sa_column=Column(ARRAY(pg.VARCHAR), default=None, nullable=True))
    careers: Optional[List[CareerBase]] = Field(sa_column=Column(ARRAY(JSONB), default=None, nullable=True))
    projects: Optional[List[ProjectBase]] = Field(sa_column=Column(ARRAY(JSONB), default=None, nullable=True))
    educations: Optional[List[EducationBase]] = Field(sa_column=Column(ARRAY(JSONB), default=None, nullable=True))

class Portfolio(BaseUUIDModel, PortfolioBase, table=True):
    __tablename__ = "portfolio"

    user: Optional[User] = Relationship(back_populates="portfolio")

    def __repr__(self) -> str:
        return f"<Portfolio id={self.id}>"
