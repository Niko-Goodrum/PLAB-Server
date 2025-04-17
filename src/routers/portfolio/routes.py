from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.routers.auth.dependencies import AccessTokenBearer
from src.schemas import BaseResponse

portfolio_router = APIRouter(prefix="/portfolio", responses={
    200: {
        "model": BaseResponse
    },
    422: {
        "model": BaseResponse
    }
})

access_token_bearer = AccessTokenBearer()


@portfolio_router.get("", response_model=BaseResponse)
async def get_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code= HTTP_200_OK, content=BaseResponse(message="Portfolio").to_dict())


@portfolio_router.get("", response_model=BaseResponse)
async def get_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code= HTTP_200_OK, content=BaseResponse(message="Get Portfolio").to_dict())


@portfolio_router.post("", response_model=BaseResponse)
async def post_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code= HTTP_201_CREATED, content=BaseResponse(message="Created Portfolio").to_dict())


@portfolio_router.get("/feedback", response_model=BaseResponse)
async def feedback_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code= HTTP_200_OK, content=BaseResponse(message="Feedback Portfolio by AI").to_dict())

