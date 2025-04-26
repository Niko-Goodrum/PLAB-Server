from pydantic import BaseModel, Field

from src.schemas import BaseResponse, BaseDictModel


class CreateUserRequest(BaseDictModel):
    email: str = Field()
    password: str = Field()
    username: str = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "EMAIL@gmail.com",
                "password": "PASSWORD",
                "username": "USERNAME",
            }
        }
    }

class SigninRequest(BaseDictModel):
    email: str = Field()
    password: str = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "EMAIL@gmail.com",
                "password": "PASSWORD"
            }
        }
    }

class RefreshRequest(BaseDictModel):
    refresh_token: str = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "refresh_token": "REFRESH_TOKEN",
            }
        }
    }

class UserResponse(BaseDictModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "ACCESS_TOKEN",
                "refresh_token": "REFRESH_TOKEN"
            }
        }
    }