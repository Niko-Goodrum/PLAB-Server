import json

from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from src.handlers.auth import add_auth_exception_handlers
from src.handlers import add_validation_exception_handler
from src.routers.auth.dependencies import AccessTokenBearer
from src.routers.portfolio.routes import portfolio_router
from src.routers.root.routes import root_router
from src.routers.auth.routes import auth_router



app = FastAPI(
    redoc_url=None,
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
app.include_router(portfolio_router, tags=["포트폴리오"])