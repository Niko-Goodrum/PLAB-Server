import typing
from typing import Any, Optional, Union, Literal

from pydantic import BaseModel
from pydantic.main import IncEx
from starlette.responses import JSONResponse
from typing_extensions import override

from src.models import BaseDictModel


def toJson(content: typing.Any, status_code: int = 200):
    return JSONResponse(content, status_code=status_code, media_type="charset=utf-8")

class BaseResponse(BaseDictModel):
    message: str
    data: Union[dict, None] = None


class BaseListResponse(BaseDictModel):
    message: str
    data: list = None