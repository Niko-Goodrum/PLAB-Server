from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.db.main import get_session
from src.models.user import User
from src.routers.auth.dependencies import AccessTokenBearer
from src.routers.interview.enums import InterviewType
from src.routers.interview.exceptions import NoAnswer, NotCreateChatError, NotCreatedChatError
from src.routers.shared.openai_utils import create_interview_prompt
from src.schemas import BaseResponse
from src.schemas.interview import CreateInterviewRequest, InterviewResponse, EditInterviewRequest
from src.services.chat import ChatService

interview_router = APIRouter(prefix="/interview", responses={
    200: {
        "model": BaseResponse
    },
    422: {
        "model": BaseResponse
    }
})

chat_service = ChatService()

access_token_bearer = AccessTokenBearer()

@interview_router.post("/create", response_model=BaseResponse)
async def create_interview(
        request: CreateInterviewRequest,
        user_data: dict = Depends(access_token_bearer),
        session: AsyncSession = Depends(get_session)
):
    sentences = await create_interview_prompt(last_answer="안녕하세요!", type=request.type)

    user_data = User(**user_data["user"])

    question = sentences[0]

    if question is None or len(question) == 0:
        raise NoAnswer


    new_chat = await chat_service.create_chat(user_id=user_data.id, last_question=question, type=request.type.value, session=session)

    if new_chat is None:
        raise NotCreateChatError

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content=BaseResponse(
        message="챗이 성공적으로 만들어졌습니다.",
        data=InterviewResponse(
            question=question,
            chat_id=new_chat.id
        ).to_dict()
    ).to_dict())


@interview_router.post("", response_model=InterviewResponse)
async def interview(
        request: EditInterviewRequest,
        user_data: dict = Depends(access_token_bearer),
        session: AsyncSession = Depends(get_session)
):

    chat_id = request.chat_id
    chat = await chat_service.get_chat_by_id(chat_id=chat_id, session=session)
    print(chat)

    if chat is None:
        raise NotCreatedChatError

    if request.type is None:
        type = InterviewType(chat.type)
    else:
        type = request.type


    prompt = await create_interview_prompt(last_question=chat.last_question, last_answer=request.answer, type=type)

    feedback = prompt[0]
    question = prompt[1]

    await chat_service.update_chat(chat_id=chat_id, type=request.type, last_question=question, session=session)

    return JSONResponse(status_code=HTTP_200_OK, content=BaseResponse(
        message="질문이 도착했습니다.",
        data=InterviewResponse(feedback=feedback, question=question, chat_id=chat_id).to_dict()
    ).to_dict())