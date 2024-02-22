from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *


class UserRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_id: int, full_name: str, username: str | None):
        query = insert(Users).values(
            user_id=user_id,
            fullname=full_name,
            username=username,
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def update_user_role(self, user_id: int, role: str):
        query = update(Users).where(
            Users.user_id == user_id
        ).values(
            role=role
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_user(self, user_id: int):
        query = select(Users).where(
            Users.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_users(self):
        query = select(Users)
        result = await self.session.execute(query)
        return result.scalars().all()
