import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *


class UserRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_id: int, full_name: str, username: str | None, refferer_id: int | None):
        query = insert(Users).values(
            user_id=user_id,
            fullname=full_name,
            username=username,
            refferer_id=refferer_id,
            registration_date=datetime.datetime.now()
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

    async def get_users(self, user_role: RoleTypes = None, refferer_id: int = None):
        if user_role:
            query = select(Users).where(
                Users.role == user_role
            )
        elif refferer_id:
            query = select(Users).where(
                Users.refferer_id == refferer_id
            )
        else:
            query = select(Users)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def sum_user_balance(self, user_id: int, balance: int = None, earned: int = None, earned_from_referals: int = None):
        if balance:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                balance=Users.balance + balance
            )
            await self.session.execute(query)
        if earned:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                earned=Users.earned + earned
            )
            await self.session.execute(query)
        if earned_from_referals:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                earned_from_referals=Users.earned_from_referals + earned_from_referals
            )
            await self.session.execute(query)
        await self.session.commit()

    async def minus_user_balance(self, user_id: int, balance: int = None, earned: int = None, earned_from_referals: int = None):
        if balance:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                balance=Users.balance - balance
            )
            await self.session.execute(query)
        if earned:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                earned=Users.earned - earned
            )
            await self.session.execute(query)
        if earned_from_referals:
            query = update(Users).where(
                Users.user_id == user_id
            ).values(
                earned_from_referals=Users.earned_from_referals - earned_from_referals
            )
            await self.session.execute(query)
        await self.session.commit()

    async def get_user_link(self, username: str):
        query = select(Users).where(Users.username.like(f'%{username}%'))
        result = await self.session.execute(query)
        return result.scalars().all()
