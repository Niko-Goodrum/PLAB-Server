from pydantic import Field

from src.models import BaseDictModel


class ImageUploadResponse(BaseDictModel):
    image_url: str = Field()