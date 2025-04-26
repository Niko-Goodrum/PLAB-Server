import uuid

from async_sqlmodel import AsyncSQLModel
from sqlmodel import Field


class BaseUUIDModel(AsyncSQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )