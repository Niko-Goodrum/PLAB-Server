from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST

from src.routers.interview.exceptions import InvalidInerviewType, NoAnswer, NotCreateChatError, NotCreatedChatError
from src.schemas import BaseResponse


def add_interview_exception_handler(app: FastAPI):
    @app.exception_handler(InvalidInerviewType)
    async def invalid_interview_type_handler(request: BaseModel, exc: InvalidInerviewType):
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=BaseResponse(message="면접 타입이 잘못됐습니다.").to_dict())

    @app.exception_handler(NoAnswer)
    async def no_answer_handler(request: BaseModel, exc: NoAnswer):
        return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content=BaseResponse(message="답이 없습니다.").to_dict())

    @app.exception_handler(NotCreateChatError)
    async def not_create_chat_handler(request: BaseModel, exc: NotCreateChatError):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=BaseResponse(message="챗을 만드는 데 실패했습니다.").to_dict())

    @app.exception_handler(NotCreatedChatError)
    async def not_created_chat_handler(request: BaseModel, exc: NotCreatedChatError):
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=BaseResponse(message="만들어지지 않은 챗입니다.").to_dict())