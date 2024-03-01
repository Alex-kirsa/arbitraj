from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *


class OfferRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_offer(self, kwargs):
        query = Offers(
            **kwargs
        )
        self.session.add(query)
        await self.session.commit()
        return query

    async def get_offers(self, offer_id: int = None,
                         user_id: int = None,
                         target_source: str = None,
                         source_traffic: str = None,
                         channel_theme: str = None,
                         status: str = None,
                         ):
        if all([offer_id, user_id, channel_theme, target_source, source_traffic, status]):
            query = select(Offers).where(
                Offers.id == offer_id,
                Offers.user_id == user_id,
                Offers.channel_theme == channel_theme,
                Offers.target_source == target_source,
                Offers.traffic_source == source_traffic,
                Offers.status == status
            )
        elif offer_id:
            query = select(Offers).where(
                Offers.id == offer_id
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif user_id:
            query = select(Offers).where(
                Offers.user_id == user_id
            )

        # elif offer_type:
        #     query = select(Offers).where(
        #         Offers.offer_type == offer_type
        #     )
        elif channel_theme:
            query = select(Offers).where(
                Offers.channel_theme == channel_theme
            )
        elif target_source:
            query = select(Offers).where(
                Offers.target_source == target_source
            )
        elif source_traffic:
            query = select(Offers).where(
                Offers.traffic_source == source_traffic
            )
        elif status:
            query = select(Offers).where(
                Offers.status == status
            )
        else:
            return None
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_offer(self, offer_id: int, **kwargs):
        query = update(Offers).where(
            Offers.id == offer_id
        ).values(
            **kwargs
        )
        await self.session.execute(query)
        await self.session.commit()

    async def add_offer_in_work(self, offer_id: int, user_id_web_master: int,
                                channel_invite_link: str, redirect_link: str,
                                status: str):
        query = insert(OffersInWork).values(
            offer_id=offer_id,
            user_id_web_master=user_id_web_master,
            channel_invite_link=channel_invite_link,
            redirect_link=redirect_link,
            status=status
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def get_offer_in_work(self, offer_id: int = None, user_id_web_master: int = None,
                                channel_invite_link: str = None, redirect_link: str = None,
                                status: str = None):
        query = select(OffersInWork)
        if all([offer_id, user_id_web_master, channel_invite_link, redirect_link, status]):
            query = select(OffersInWork).where(
                OffersInWork.offer_id == offer_id,
                OffersInWork.user_id_web_master == user_id_web_master,
                OffersInWork.channel_invite_link == channel_invite_link,
                OffersInWork.redirect_link == redirect_link,
                OffersInWork.status == status
            )
        elif offer_id:
            query = select(OffersInWork).where(
                OffersInWork.offer_id == offer_id
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif user_id_web_master:
            query = select(OffersInWork).where(
                OffersInWork.user_id_web_master == user_id_web_master
            )
        elif channel_invite_link:
            query = select(OffersInWork).where(
                OffersInWork.channel_invite_link == channel_invite_link
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif redirect_link:
            query = select(OffersInWork).where(
                OffersInWork.redirect_link == redirect_link
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif status:
            query = select(OffersInWork).where(
                OffersInWork.status == status
            )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_offer_in_work_in_web_master(self, offer_id: int, user_id_web_master: int, status: str = None):
        query = select(OffersInWork).where(
            OffersInWork.offer_id == offer_id,
            OffersInWork.user_id_web_master == user_id_web_master,
        )
        if status:
            query = query.where(OffersInWork.status == status)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_channel_invite_requests(self, user_id: int = None, channel_id: int = None, invite_link: str | list = None, offer_id: int = None):
        if all([user_id, channel_id, invite_link, offer_id]):
            query = select(ChannelInviteRequests).where(
                ChannelInviteRequests.user_id == user_id,
                ChannelInviteRequests.channel_id == channel_id,
                ChannelInviteRequests.invite_link == invite_link if isinstance(invite_link, str) else ChannelInviteRequests.invite_link.in_(invite_link),
                ChannelInviteRequests.offer_id == offer_id
            )
        elif user_id:
            query = select(ChannelInviteRequests).where(
                ChannelInviteRequests.user_id == user_id
            )
        elif offer_id:
            query = select(ChannelInviteRequests).where(
                ChannelInviteRequests.offer_id == offer_id
            )
        elif channel_id:
            query = select(ChannelInviteRequests).where(
                ChannelInviteRequests.channel_id == channel_id
            )
        elif invite_link:
            query = select(ChannelInviteRequests).where(
                ChannelInviteRequests.invite_link == invite_link if isinstance(invite_link, str) else ChannelInviteRequests.invite_link.in_(invite_link)
            )
        else:
            query = select(ChannelInviteRequests)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_gambling_offers(self, offer_id: int = None, status: str = None):
        if all([offer_id, status]):
            query = select(GamblingOffers).where(
                GamblingOffers.id == offer_id,
                GamblingOffers.status == status
            )
        elif offer_id:
            query = select(GamblingOffers).where(
                GamblingOffers.id == offer_id
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif status:
            query = select(GamblingOffers).where(
                GamblingOffers.status == status
            )
        else:
            query = select(GamblingOffers)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_gambling_offer_links(self, offer_id: int = None, user_id: int = None, link: str = None, current_deposit: float = None):
        if all([offer_id, user_id, link, current_deposit]):
            query = select(GamblingOffersLinks).where(
                GamblingOffersLinks.gambling_offer_id == offer_id,
                GamblingOffersLinks.user_id == user_id,
                GamblingOffersLinks.link == link,
                GamblingOffersLinks.current_deposit == current_deposit
            )
        elif offer_id:
            query = select(GamblingOffersLinks).where(
                GamblingOffersLinks.gambling_offer_id == offer_id
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        elif user_id:
            query = select(GamblingOffersLinks).where(
                GamblingOffersLinks.user_id == user_id
            )
        elif link:
            query = select(GamblingOffersLinks).where(
                GamblingOffersLinks.link == link
            )
        elif current_deposit:
            query = select(GamblingOffersLinks).where(
                GamblingOffersLinks.current_deposit == current_deposit
            )
        else:
            query = select(GamblingOffersLinks)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_gambling_offer_links_by_user_id_and_offer_id(self, user_id: int, offer_id: int):
        query = select(GamblingOffersLinks).where(
            GamblingOffersLinks.user_id == user_id,
            GamblingOffersLinks.gambling_offer_id == offer_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_free_gambling_offer_link(self, gambling_offer_id: int):
        query = select(GamblingOffersLinks).where(
            GamblingOffersLinks.gambling_offer_id == gambling_offer_id,
            GamblingOffersLinks.user_id == None
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_gambling_offer_link(self, id_: int, user_id: int = None, deposit: float = None):
        if user_id:
            query = update(GamblingOffersLinks).where(
                GamblingOffersLinks.id == id_,
            ).values(
                user_id=user_id
            )
        elif deposit:
            query = update(GamblingOffersLinks).where(
                GamblingOffersLinks.id == id_,
            ).values(
                current_deposit=deposit
            )
        else:
            return None
        await self.session.execute(query)
        await self.session.commit()

    async def update_gambling_offer(self, gambling_offer_id: int, status: str):
        query = update(GamblingOffers).where(
            GamblingOffers.id == gambling_offer_id
        ).values(
            status=status
        )
        await self.session.execute(query)
        await self.session.commit()
