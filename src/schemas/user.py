from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
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
