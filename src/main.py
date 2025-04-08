import json

from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from src.handlers.auth import add_auth_exception_handlers
from src.handlers import add_validation_exception_handler
from src.routers.root.routes import root_router
from src.routers.auth.routes import auth_router

AUTH_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


app = FastAPI(
    redoc_url=None,
    dependencies=[Depends(AUTH_HEADER)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title="PLAB",
            version="0.0.69",
            routes=app.routes,
        )
    return app.openapi_schema


app.openapi = custom_openapi


add_validation_exception_handler(app)
add_auth_exception_handlers(app)


app.include_router(root_router, tags=["상드름"])
app.include_router(auth_router, tags=["Auth"])