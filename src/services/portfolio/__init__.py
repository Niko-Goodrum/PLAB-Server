import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional

from sqlmodel import select

from src.models.portfolio import Portfolio
from src.schemas.portfolio import EditPortfolioRequest


class PortfolioService:
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

    async def edit_portfolio(self, user_id: uuid.UUID, request: EditPortfolioRequest, session: AsyncSession) -> Optional[Portfolio]:
        statement = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await session.execute(statement)
        existing_portfolio = result.scalar_one_or_none()

        if not existing_portfolio:
            return None

        update_data = request.model_dump(exclude_none=True)

        if 'careers' in update_data and update_data['careers'] is not None:
            update_data['careers'] = [
                career.model_dump() for career in request.careers if career is not None
            ]

        if 'projects' in update_data and update_data['projects'] is not None:
            update_data['projects'] = [
                project.model_dump() for project in request.projects if project is not None
            ]

        if 'educations' in update_data and update_data['educations'] is not None:
            update_data['educations'] = [
                education.model_dump() for education in request.educations if education is not None
            ]

        for field_name, value in update_data.items():
            setattr(existing_portfolio, field_name, value)

        session.add(existing_portfolio)
        await session.commit()
        await session.refresh(existing_portfolio)

        return existing_portfolio

    async def delete_portfolio_by_user_id(self, user_id: uuid.UUID, session: AsyncSession) -> Optional[Portfolio]:
        statement = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await session.execute(statement)
        deleting_portfolio = result.scalar_one_or_none()

        if deleting_portfolio:
            await session.delete(deleting_portfolio)
            await session.commit()
            return deleting_portfolio
