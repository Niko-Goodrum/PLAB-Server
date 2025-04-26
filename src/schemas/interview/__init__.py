import uuid

from pydantic import Field

from src.models import BaseDictModel
from src.routers.interview.enums import InterviewType
from src.schemas import BaseResponse


class CreateInterviewRequest(BaseDictModel):
    type: InterviewType = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "Total"
            }
        }
    }

class EditInterviewRequest(BaseDictModel):
    chat_id: uuid.UUID = Field()
    answer: str = Field()
    type: InterviewType = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "chat_id": "CHAT_ID",
                "answer": "제 최애는 박상민입니다."
            }
        }
    }


class InterviewResponse(BaseDictModel):
    feedback: str = Field(default=None)
    question: str = Field()
    chat_id: uuid.UUID = Field()



