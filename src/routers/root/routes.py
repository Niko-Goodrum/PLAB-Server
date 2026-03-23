from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

root_router = APIRouter()
INDEX_FILE = Path(__file__).resolve().parents[2] / "index.html"


@root_router.get("/", response_class=FileResponse, include_in_schema=False)
async def root():
    return FileResponse(INDEX_FILE)
