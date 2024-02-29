from sqlalchemy.ext.asyncio import AsyncSession

from .requests.channel_requests import ChannelRequestsRepo
from .requests.offer_requests import OfferRequestsRepo
from .requests.payment_requests import PaymentRequestsRepo
from .requests.user_requests import UserRequestsRepo


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRequestsRepo(session)
        self.offer_repo = OfferRequestsRepo(session)
        self.channel_repo = ChannelRequestsRepo(session)
        self.payment_repo = PaymentRequestsRepo(session)
