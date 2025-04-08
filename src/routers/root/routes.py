from fastapi import APIRouter

from src.config import Config
from src.schemas import BaseResponse
from fastapi.responses import JSONResponse

root_router = APIRouter()


@root_router.get("/", response_model=BaseResponse, responses={
    200: {
        "model": BaseResponse
    }
})
async def root():
    return JSONResponse(status_code=200, content=BaseResponse(message="상민이 여드름").to_dict())
