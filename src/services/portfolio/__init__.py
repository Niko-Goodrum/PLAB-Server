import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional

from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select

from src.models.portfolio import Portfolio, Career, Project, Education, ProjectURL
from src.schemas.portfolio import EditPortfolioRequest, PortfolioResponse, ProjectResponse, EducationResponse


class PortfolioService:
    async def get_portfolio(
            self,
            user_id: uuid.UUID,
            session: AsyncSession
    ) -> Optional[PortfolioResponse]:

        statement = select(Portfolio).where(Portfolio.user_id == user_id).options(
            joinedload(Portfolio.careers),
            joinedload(Portfolio.projects).joinedload(Project.urls),
            joinedload(Portfolio.educations).joinedload(Education.grade)
        )

        result = await session.execute(statement)


        portfolio = result.unique().scalar_one_or_none()
        return PortfolioResponse.model_validate(portfolio)


    async def create_portfolio(self, user_id: uuid.UUID, name: str, session: AsyncSession):
        create_dict: dict[str, Any] = {
            "name": name,
            "user_id": user_id
        }

        created_portfolio = Portfolio(**create_dict)

        session.add(created_portfolio)

        await session.flush()
        await session.commit()

        return created_portfolio

    async def edit_portfolio(
        self,
        user_id: uuid.UUID,
        request: EditPortfolioRequest,
        session: AsyncSession
    ) -> Optional[Portfolio]:

        statement = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await session.execute(statement)
        portfolio = result.scalar_one_or_none()

        if not portfolio:
            return None

        update_fields = request.model_dump(
            exclude_none=True,
            exclude={"careers", "projects", "educations"}
        )
        for key, value in update_fields.items():
            setattr(portfolio, key, value)

        if request.careers is not None:
            await session.execute(delete(Career).where(Career.portfolio_id == portfolio.id))
            for career_data in request.careers:
                careers = Career(**career_data.model_dump())
                careers.portfolio_id = portfolio.id
                session.add(careers)

        if request.projects is not None:
            await session.execute(delete(Project).where(Project.portfolio_id == portfolio.id))
            for project_data in request.projects:
                projects = Career(**project_data.model_dump())
                projects.portfolio_id = portfolio.id
                session.add(projects)

        if request.educations is not None:
            await session.execute(delete(Education).where(Education.portfolio_id == portfolio.id))
            for edu_data in request.educations:
                educations = Career(**edu_data.model_dump())
                educations.portfolio_id = portfolio.id
                session.add(educations)

        session.add(portfolio)
        await session.commit()
        await session.refresh(portfolio)

        return portfolio

    async def delete_portfolio_by_user_id(self, user_id: uuid.UUID, session: AsyncSession) -> Optional[Portfolio]:
        statement = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await session.execute(statement)
        deleting_portfolio = result.scalar_one_or_none()

        if deleting_portfolio:
            await session.delete(deleting_portfolio)
            await session.commit()
            return deleting_portfolio
