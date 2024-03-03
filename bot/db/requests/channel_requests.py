from sqlalchemy import select, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *


class ChannelRequestsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_channel(self, **kwargs):
        query = insert(Channels).values(
            kwargs
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def get_channel(self, id_: int):
        query = select(Channels).where(
            Channels.id == id_
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_channels(self, channel_theme: str = None, channel_owner_id: int = None, sort_type: str = "asc", status: ChannelStatus | list[ChannelStatus] = None):
        filters = []

        if channel_theme:
            filters.append(Channels.channel_theme == channel_theme)
        if channel_owner_id:
            filters.append(Channels.channel_owner_id == channel_owner_id)
        if status:
            if isinstance(status, list):
                filters.append(Channels.status.in_(status))
            else:
                filters.append(Channels.status == status)

        query = select(Channels)
        if filters:
            query = query.where(and_(*filters))

        if sort_type == "asc":
            query = query.order_by(Channels.subs_amount.asc())
        else:
            query = query.order_by(Channels.subs_amount.desc())

        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_channe_for_traffic(self, **kwargs):
        query = insert(ChannelsForTraffic).values(
            kwargs
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.commit()

    async def get_channel_for_traffic(self, channel_id: int, owner_id: int = None) -> ChannelsForTraffic:
        if owner_id:
            query = select(ChannelsForTraffic).where(
                ChannelsForTraffic.owner_id == owner_id
            )
            result = await self.session.execute(query)
            return result.scalars().all()

        query = select(ChannelsForTraffic).where(
            ChannelsForTraffic.channel_id == channel_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_channels_for_traffic(self):
        query = select(ChannelsForTraffic)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_channel_for_traffic_status(self, channel_id: int, status: ChannelStatus):
        query = update(ChannelsForTraffic).where(
            ChannelsForTraffic.channel_id == channel_id
        ).values(
            status=status
        )
        await self.session.execute(query)
        await self.session.commit()

    async def update_channel(self, id_: int, **kwargs):
        query = update(Channels).where(
            Channels.id == id_
        ).values(
            kwargs
        )
        await self.session.execute(query)
        await self.session.commit()
