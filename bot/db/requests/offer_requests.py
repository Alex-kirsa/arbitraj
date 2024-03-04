from sqlalchemy import select, update, and_, or_
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
                         traffic_source: str = None,
                         channel_theme: str = None,
                         status: OfferStatus | list[OfferStatus] = None,
                         channel_id: int = None
                         ):
        filters = []

        if offer_id:
            query = select(Offers).where(Offers.id == offer_id)
            result = await self.session.execute(query)
            return result.scalars().first()

        if user_id:
            filters.append(Offers.user_id == user_id)
        if channel_id:
            filters.append(Offers.channel_id == channel_id)
        if target_source:
            filters.append(Offers.target_source == target_source)
        if traffic_source:
            filters.append(Offers.traffic_source == traffic_source)
        if channel_theme:
            filters.append(Offers.channel_theme == channel_theme)
        if status:
            if isinstance(status, list):
                filters.append(Offers.status.in_(status))
            else:
                filters.append(Offers.status == status)

        query = select(Offers)
        if filters:
            query = query.where(and_(*filters))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_offers_by_target_source_and_traffic_source(self, target_source: str, traffic_source: str):
        query = select(Offers).where(
            Offers.target_source == target_source,
            Offers.traffic_source == traffic_source
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_offer(self, offer_id: int, commit=True, **kwargs):
        query = update(Offers).where(
            Offers.id == offer_id
        ).values(
            **kwargs
        )
        await self.session.execute(query)
        if commit:
            await self.session.commit()

    async def update_offer_in_work(self, id_: int, commit=True, **kwargs):
        query = update(OffersInWork).where(
            OffersInWork.id == id_,
        ).values(
            **kwargs
        )
        await self.session.execute(query)
        if commit:
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
                                status: str = None, id_: int = None):
        query = select(OffersInWork)

        if any([channel_invite_link, redirect_link, id_]):
            conditions = []
            if channel_invite_link:
                conditions.append(OffersInWork.channel_invite_link == channel_invite_link)
            if redirect_link:
                conditions.append(OffersInWork.redirect_link == redirect_link)
            if id_:
                conditions.append(OffersInWork.id == id_)

            query = select(OffersInWork).where(or_(*conditions))
            result = await self.session.execute(query)
            return result.scalars().first()

        filters = []
        if offer_id:
            filters.append(OffersInWork.offer_id == offer_id)
        if user_id_web_master:
            filters.append(OffersInWork.user_id_web_master == user_id_web_master)
        if status:
            filters.append(OffersInWork.status == status)

        if filters:
            query = select(OffersInWork).where(and_(*filters))

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

    async def add_channel_invite_request(self, user_id: int, channel_id: int, invite_link: str, offer_id: int, commit=True):
        query = insert(ChannelInviteRequests).values(
            user_id=user_id,
            channel_id=channel_id,
            invite_link=invite_link,
            offer_id=offer_id
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        if commit:
            await self.session.commit()

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

    async def get_channel_invite_requests_by_user_id(self, user_id: int, link: str):
        query = select(ChannelInviteRequests).where(
            ChannelInviteRequests.user_id == user_id,
            ChannelInviteRequests.invite_link == link
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_gambling_offers(self, offer_id: int = None, casino_name: str = None, status: str = None):
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
        elif casino_name:
            query = select(GamblingOffers).where(
                GamblingOffers.casino_name == casino_name
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        else:
            query = select(GamblingOffers)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_gambling_offer_links(self, offer_id: int = None, user_id: int = None, link: str = None, current_deposit: float = None):
        filters = []

        if all([offer_id, user_id, link, current_deposit]):
            filters.extend([
                GamblingOffersLinks.gambling_offer_id == offer_id,
                GamblingOffersLinks.user_id == user_id,
                GamblingOffersLinks.link == link,
                GamblingOffersLinks.current_deposit == current_deposit
            ])
        elif offer_id:
            filters.append(GamblingOffersLinks.gambling_offer_id == offer_id)
        elif user_id:
            filters.append(GamblingOffersLinks.user_id == user_id)
        elif link:
            filters.append(GamblingOffersLinks.link == link)
        elif current_deposit:
            filters.append(GamblingOffersLinks.current_deposit == current_deposit)

        query = select(GamblingOffersLinks)
        if filters:
            query = query.where(*filters)

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
            GamblingOffersLinks.user_id.is_(None)
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

    async def add_gambling_offer(self, casino_name: str, status: GamblingOfferStatus):
        query = GamblingOffers(
            casino_name=casino_name,
            status=status
        )
        self.session.add(query)
        await self.session.commit()
        return query

    async def add_gambling_offer_link(self, gambling_offer_id: int, link: str):
        query = insert(GamblingOffersLinks).values(
            gambling_offer_id=gambling_offer_id,
            link=link,
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()