from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from src.handlers.auth import add_auth_exception_handlers
from src.handlers import add_validation_exception_handler
from src.handlers.interview import add_interview_exception_handler
from src.handlers.portfolio import add_portfoilo_exception_handler
from src.routers.interview.routes import interview_router
from src.routers.portfolio.routes import portfolio_router
from src.routers.root.routes import root_router
from src.routers.auth.routes import auth_router
from src.routers.user.routes import user_router

app = FastAPI(
    redoc_url=None,
)

load_dotenv()

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
add_interview_exception_handler(app)
add_portfoilo_exception_handler(app)


app.include_router(root_router, tags=["Root"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(user_router, tags=["User"])
app.include_router(portfolio_router, tags=["포트폴리오"])
app.include_router(interview_router, tags=["면접"])
