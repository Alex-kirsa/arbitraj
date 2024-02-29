from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *


class PaymentRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_withdraw_request(self, user_id: int, amount: int, payment_system: str, bank_name: str):
        query = insert(WithdrawRequests).values(
            user_id=user_id,
            amount=amount,
            payment_system=payment_system,
            bank_name=bank_name
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def get_withdraw_requests(self, user_id: int = None, status: str = None, payment_system: str = None):
        query = select(WithdrawRequests)
        if all([user_id, status, payment_system]):
            query = query.where(WithdrawRequests.user_id == user_id, WithdrawRequests.status == status, WithdrawRequests.payment_system == payment_system)
        elif user_id:
            query = query.where(WithdrawRequests.user_id == user_id)
        elif status:
            query = query.where(WithdrawRequests.status == status)
        elif payment_system:
            query = query.where(WithdrawRequests.payment_system == payment_system)
        result = await self.session.execute(query)
        return result.scalars().all()

