from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.config import Config
from src.routers.auth.dependencies import AccessTokenBearer
from src.routers.portfolio.exceptions import ImageNotFoundError, ImageExtensionError, FileIsNotImageError, \
    MaxFileSizeError, UrlLoadError, UploadError
from src.schemas import BaseResponse

from src.models.portfolio import Portfolio

import vercel_blob
import io
from PIL import Image
import secrets

from src.schemas.portfolio import ImageUploadResponse

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
    return JSONResponse(status_code=HTTP_200_OK, content=BaseResponse(message="Get Portfolio").to_dict())


@portfolio_router.post("", response_model=BaseResponse)
async def post_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code=HTTP_201_CREATED, content=BaseResponse(message="Created Portfolio").to_dict())


@portfolio_router.get("/feedback", response_model=BaseResponse)
async def feedback_portfolio(
        _: dict = Depends(access_token_bearer)
):
    return JSONResponse(status_code=HTTP_200_OK, content=BaseResponse(message="Feedback Portfolio by AI").to_dict())


@portfolio_router.post("/upload-image", response_model=BaseResponse)
async def upload_image(
        file: UploadFile = File(...),
        user_info: dict = Depends(access_token_bearer)
):
    if not file:
        raise ImageNotFoundError()

    allowed_extensions = ["jpg", "jpeg", "png"]
    file_extension = file.filename.rsplit(".", maxsplit=1)[-1].lower()

    if file_extension not in allowed_extensions:
        raise ImageExtensionError()

    if not file.content_type or not file.content_type.startswith("image"):
        raise FileIsNotImageError

    try:
        file_content = await file.read()

        max_file_size_mb = 10
        max_file_size_bytes = max_file_size_mb * 128 * 128
        if len(file_content) > max_file_size_bytes:
            raise MaxFileSizeError()

        image = Image.open(io.BytesIO(file_content))
        output = io.BytesIO()
        image_format = 'JPEG' if file_extension in ['jpg', 'jpeg'] else 'PNG'
        image.save(output, format=image_format)
        save_file_content = output.getvalue()
        new_filename = f"{secrets.token_hex(16)}.{image_format.lower()}"

        blob_request = vercel_blob.put(
            new_filename,
            save_file_content
        )

        blob_metadata = vercel_blob.head(
            new_filename
        )

        blob_url = blob_metadata.get("url")

        if not blob_url:
            raise UrlLoadError()

        return JSONResponse(status_code=HTTP_201_CREATED, content=BaseResponse(message="이미지를 업로드했습니다", data=ImageUploadResponse(image_url=blob_url).to_dict()).to_dict())

    except Exception as e:
        print(e)
        raise UploadError()