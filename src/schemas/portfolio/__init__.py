from typing import List, Optional

from pydantic import Field, ConfigDict
from sqlalchemy import Column, ARRAY

from src.models import BaseDictModel
from src.models.portfolio import CareerBase, ProjectBase, EducationBase, ProjectURLBase, GradeBase


class ImageUploadResponse(BaseDictModel):
    image_url: str = Field()

class CareerResponse(BaseDictModel):
    company_name: str
    part: str
    position: str
    join_date: str
    resign_date: Optional[str]
    task: Optional[str]
    techs: Optional[List[str]]

    model_config = {
        "from_attributes": True
    }


class ProjectResponse(BaseDictModel):
    name: str
    part: str
    start_date: str
    end_date: Optional[str]
    task: Optional[str]
    images: Optional[List[str]]
    techs: Optional[List[str]]
    urls: Optional[List[ProjectURLBase]]

    model_config = {
        "from_attributes": True
    }

class EducationResponse(BaseDictModel):
    school_name: str
    level: str
    status: str
    join_date: str
    resign_date: Optional[str]
    major: Optional[str]
    description: Optional[str]
    grade: Optional[GradeBase]

    model_config = {
        "from_attributes": True
    }


class PortfolioResponse(BaseDictModel):
    name: str
    phone_num: Optional[str]
    email: Optional[str]
    user_image: Optional[str]
    introduce: Optional[str]
    job: Optional[str]
    techs: Optional[List[str]]
    careers: Optional[List[CareerResponse]]
    projects: Optional[List[ProjectResponse]]
    educations: Optional[List[EducationResponse]]

    model_config = {
        "from_attributes": True
    }


class EditPortfolioRequest(BaseDictModel):
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 1, "example": "<이름>"}
    )
    phone_num: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 2, "example": "<전화번호>"}
    )
    email: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 3, "example": "<이메일>"}
    )
    user_image: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 4, "example": "<URL>"}
    )
    introduce: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 5, "example": "<상세설명>"}
    )
    job: Optional[str] = Field(
        default=None,
        json_schema_extra={"x-order": 6, "example": "<직무>"}
    )
    techs: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={"x-order": 7, "example": ["<기술스택>"]}
    )
    careers: Optional[List[CareerBase]] = Field(
        default=None,
        json_schema_extra={"x-order": 8, "example": [
            {
                "company_name": "<회사명>",
                "part": "<부서명>",
                "position": "<포지션>",
                "join_date": "YYYY.MM",
                "resign_date": "YYYY.MM",
                "task": "<주요 업무>",
                "techs": ["<기술스택>"],
            }
        ]}
    )
    projects: Optional[List[ProjectBase]] = Field(
        default=None,
        json_schema_extra={"x-order": 9, "example": [
            {
                "name": "<프로젝트명>",
                "part": "<담당역할>",
                "start_date": "YYYY.MM",
                "end_date": "YYYY.MM",
                "task": "<주요 업무>",
                "urls": [
                    {
                        "title": "<사이트 링크, Notion 링크>",
                        "link": "https://example.com",
                    }
                ],
                "images": ["<URL>"],
                "techs": ["<주요업무>"],
            }
        ]}
    )
    educations: Optional[List[EducationBase]] = Field(
        default=None,
        json_schema_extra={"x-order": 10, "example": [
            {
                "school_name": "<학교명>",
                "level": "<학력>",
                "join_date": "YYYY.MM",
                "resign_date": "YYYY.MM",
                "major": "<전공>",
                "grade": {
                    "received_grade": "<받은 학점>",
                    "max_grade": "<기준 학점>"
                },
                "description": "<상세설명>",
            }
        ]}
    )

