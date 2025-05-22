from typing import Any, Optional, Union, Literal

from pydantic import BaseModel
from pydantic.main import IncEx
from typing_extensions import override

from src.models import BaseDictModel


class BaseResponse(BaseDictModel):
    message: str
    data: Union[dict, None] = None


class BaseListResponse(BaseDictModel):
    message: str
    data: list = None