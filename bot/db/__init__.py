from sqlalchemy.ext.asyncio import AsyncSession

from .requests.user_requests import UserRequestsRepo


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRequestsRepo(session)
