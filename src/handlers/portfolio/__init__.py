from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from src.routers.portfolio.exceptions import ImageNotFoundError, ImageExtensionError, FileIsNotImageError, \
    MaxFileSizeError, UrlLoadError, UploadError
from src.schemas import BaseResponse


def add_portfoilo_exception_handler(app: FastAPI):
    @app.exception_handler(ImageNotFoundError)
    async def image_not_found_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=BaseResponse(message="이미지 파일이 없습니다.").to_dict())

    @app.exception_handler(ImageExtensionError)
    async def image_extension_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=BaseResponse(message="지원하지 않는 형식입니다.").to_dict())

    @app.exception_handler(FileIsNotImageError)
    async def file_is_not_image_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=BaseResponse(message="파일이 이미지가 아닙니다.").to_dict())

    @app.exception_handler(MaxFileSizeError)
    async def max_file_size_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=BaseResponse(message="이미지 사이즈가 너무 큽니다.").to_dict())

    @app.exception_handler(UrlLoadError)
    async def url_load_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=BaseResponse(message="URL을 불러오지 못했습니다.").to_dict())

    @app.exception_handler(UploadError)
    async def upload_handler(request: BaseModel, exc: ImageNotFoundError):
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=BaseResponse(message="이미지를 업로드하는데 실패했습니다").to_dict())