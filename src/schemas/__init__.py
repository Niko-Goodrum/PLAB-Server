from typing import Any, Optional, Union, Literal

from pydantic import BaseModel
from pydantic.main import IncEx
from typing_extensions import override


class BaseDictModel(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)

class BaseResponse(BaseDictModel):
    message: str
    data: Union[dict, None] = None


    