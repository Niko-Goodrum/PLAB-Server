from fastapi import APIRouter

from src.config import Config
from src.schemas import BaseResponse
from fastapi.responses import JSONResponse

root_router = APIRouter()



@root_router.get("/", response_model=BaseResponse, responses={200: {
            "content": {
                "application/json": {
                    "example": {"message": "상민이 여드름"}
                }
            },
        }})
async def root():
    return JSONResponse(status_code=200, content={"message": "상민이 여드름"})

@root_router.get("/test")
async def test():
    return JSONResponse(status_code=200, content={"config": Config.json()})