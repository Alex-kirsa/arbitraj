from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *
from bot.utils.constants import PaymentMethods


class PaymentRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_withdraw_request(self, user_id: int, amount: int, payment_system: str, bank_name: str, card_number: str, crypto_adress: str):
        query = insert(WithdrawRequests).values(
            user_id=user_id,
            amount=amount,
            payment_system=payment_system,
            bank_name=bank_name,
            crypto_adress=crypto_adress,
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

    async def add_topup_request(self, user_id: int, amount: int, payment_method: PaymentMethods, fullname: str = None, last_4_digits_credit_card: int = None, offer_id: int = None):
        query = insert(TopUpRequests).values(
            user_id=user_id,
            payment_method=payment_method,
            fullname=fullname,
            last_4_digits_credit_card=last_4_digits_credit_card,
            offer_id=offer_id,
            amount=amount,
            status=TopUpStatus.ACTIVE if payment_method == PaymentMethods.ON_CARD else TopUpStatus.COMPLETED_BY_CRYPTOBOT
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()
