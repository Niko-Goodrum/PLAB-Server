from typing import Any

from pydantic import BaseModel

class BaseDictModel(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
