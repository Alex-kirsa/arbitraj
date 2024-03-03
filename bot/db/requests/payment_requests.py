from sqlalchemy import select, update, and_
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

    async def get_withdraw_requests(self, id_: int = None, user_id: int = None, status: str = None, payment_system: str = None):
        query = select(WithdrawRequests)
        if all([user_id, status, payment_system]):
            query = query.where(WithdrawRequests.user_id == user_id, WithdrawRequests.status == status, WithdrawRequests.payment_system == payment_system)
        elif user_id:
            query = query.where(WithdrawRequests.user_id == user_id)
        elif status:
            query = query.where(WithdrawRequests.status == status)
        elif payment_system:
            query = query.where(WithdrawRequests.payment_system == payment_system)
        elif id_:
            query = query.where(WithdrawRequests.id == id_)
            result = await self.session.execute(query)
            return result.scalars().first()
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_withdraw_request_with_status(self, user_id: int, status: str):
        query = select(WithdrawRequests).where(WithdrawRequests.user_id == user_id, WithdrawRequests.status == status)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_topup_request(self, user_id: int, amount: int, payment_method: PaymentMethods, offer_id: int = None, channel_id: int = None, fullname: str = None,
                                last_4_digits_credit_card: str = None):
        query = insert(TopUpRequests).values(
            user_id=user_id,
            payment_method=payment_method,
            fullname=fullname,
            last_4_digits_credit_card=last_4_digits_credit_card,
            offer_id=offer_id,
            channel_id=channel_id,
            amount=amount,
            status=TopUpStatus.ACTIVE if payment_method == PaymentMethods.ON_CARD else TopUpStatus.COMPLETED_BY_CRYPTOBOT
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def update_withdraw_status(self, id_: int, status: str):
        query = update(WithdrawRequests).where(
            WithdrawRequests.id == id_
        ).values(
            status=status
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_topup_request(self, offer_id: int | str = None, user_id: int = None, status: TopUpStatus | list[TopUpStatus] = None, channel_id: int | str = None, ):
        filters = []
        if status is not None:
            if isinstance(status, list):
                filters.append(TopUpRequests.status.in_([s.value for s in status]))
            elif isinstance(status, TopUpStatus):
                filters.append(TopUpRequests.status == status.value)
        if user_id:
            filters.append(TopUpRequests.user_id == user_id)
        if offer_id:
            if isinstance(offer_id, int):
                filters.append(TopUpRequests.offer_id == offer_id)
            elif isinstance(offer_id, str):
                filters.append(TopUpRequests.offer_id.isnot(None))  # Используем isnot для проверки на not null
        if channel_id:
            if isinstance(channel_id, str):
                filters.append(TopUpRequests.channel_id.isnot(None))
            else:
                filters.append(TopUpRequests.channel_id == channel_id)

        query = select(TopUpRequests)
        if filters:
            query = query.where(and_(*filters))

        result = await self.session.execute(query)
        return result.scalars().all()

