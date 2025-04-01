import json

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from src.schemas import BaseResponse
from src.routers import root_router
from src.routers.auth.routes import auth_router

AUTH_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

SWAGGER_HEADERS = {
    "title": "PLAB",
    "version": "0.0.69",
}


openapi_tags: list

with open("swagger_metadata.json", "r") as json_file:
    openapi_tags = json.load(json_file)


app = FastAPI(
    redoc_url=None,
    dependencies=[Depends(AUTH_HEADER)],
    openapi_tags=openapi_tags,
    swagger_ui_parameters={ },
    **SWAGGER_HEADERS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(root_router, tags=["상드름"])
app.include_router(auth_router, tags=["Auth"])