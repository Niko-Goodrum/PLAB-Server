from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKeyHeader

AUTH_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

SWAGGER_HEADERS = {
    "title": "박상민의 서버",
    "version": "0.0.1",
}
app = FastAPI(
    redoc_url=None,
    dependencies=[Depends(AUTH_HEADER)],
    swagger_ui_parameters={
        "docExpansion": "none",
    },
    **SWAGGER_HEADERS
)

app.get


@app.get("/sangmin")
async def root():
    return {"message": "상드름"}
