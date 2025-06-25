import datetime
import uuid
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
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
    techs: List[str] = Field(sa_column=Column(ARRAY(pg.VARCHAR), nullable=True))

class ProjectURLBase(BaseDictModel):
    title: str
    link: Optional[str] = None

class ProjectBase(BaseDictModel):
    name: str
    part: str
    start_date: str
    end_date: Optional[str] = None
    task: Optional[str] = None
    images: List[str] = Field(sa_column=Column(ARRAY(pg.VARCHAR), nullable=True))
    techs: List[str] = Field(sa_column=Column(ARRAY(pg.VARCHAR), nullable=True))

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
    description: Optional[str] = None

class PortfolioBase(BaseDictModel):
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    phone_num: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    email: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    user_image: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    introduce: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    job: Optional[str] = Field(sa_column=Column(pg.VARCHAR, default=None, nullable=True))
    techs: List[str] = Field(sa_column=Column(ARRAY(pg.VARCHAR), nullable=True))

class Career(BaseUUIDModel, CareerBase, table=True):
    __tablename__ = "careers"

    portfolio_id: Optional[uuid.UUID] = Field(default=None, foreign_key="portfolio.id")
    portfolio: Optional["Portfolio"] = Relationship(back_populates="careers")

class ProjectURL(BaseUUIDModel, ProjectURLBase, table=True):
    __tablename__ = "project_urls"

    project_id: Optional[uuid.UUID] = Field(default=None, foreign_key="projects.id")
    project: Optional["Project"] = Relationship(back_populates="urls")

class Project(BaseUUIDModel, ProjectBase, table=True):
    __tablename__ = "projects"

    portfolio_id: Optional[uuid.UUID] = Field(default=None, foreign_key="portfolio.id")
    portfolio: Optional["Portfolio"] = Relationship(back_populates="projects")

    urls: List["ProjectURL"] = Relationship(sa_relationship=relationship("ProjectURL", back_populates="project", cascade="all, delete-orphan", lazy="select"))

class Grade(BaseUUIDModel, GradeBase, table=True):
    __tablename__ = "grades"

    education_id: Optional[uuid.UUID] = Field(default=None, foreign_key="educations.id")
    education: Optional["Education"] = Relationship(back_populates="grade")

class Education(BaseUUIDModel, EducationBase, table=True):
    __tablename__ = "educations"

    portfolio_id: Optional[uuid.UUID] = Field(default=None, foreign_key="portfolio.id")
    portfolio: Optional["Portfolio"] = Relationship(back_populates="educations")

    grade: Optional["Grade"] = Relationship(sa_relationship=relationship("Grade", back_populates="education", lazy="select"))



class Portfolio(BaseUUIDModel, PortfolioBase, table=True):
    __tablename__ = "portfolio"

    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", unique=True)

    user: Optional[User] = Relationship(back_populates="portfolio")
    careers: List["Career"] = Relationship(sa_relationship=relationship("Career", back_populates="portfolio", cascade="all, delete-orphan", lazy="select"))
    projects: List["Project"] = Relationship(sa_relationship=relationship("Project", back_populates="portfolio", cascade="all, delete-orphan", lazy="select"))
    educations: List["Education"] = Relationship(sa_relationship=relationship("Education", back_populates="portfolio", cascade="all, delete-orphan", lazy="select"))

    def __repr__(self) -> str:
        return f"<Portfolio id={self.id}>"
