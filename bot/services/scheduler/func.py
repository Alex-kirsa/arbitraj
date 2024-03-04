import asyncio
import datetime

from aiogram import Bot
from aiogram_i18n.cores import FluentRuntimeCore
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.constants import OfferStatus

from bot.db import Repo


async def send_scheduled_message(ctx, offer_id: int, web_master_id: int, locale: str = "uk"):
    db_factory = ctx["db_factory"]
    bot: Bot = ctx["bot"]
    core: FluentRuntimeCore = ctx["core"]
    async with db_factory() as db_session:
        session: AsyncSession = db_session
        repo = Repo(session)
        offer_model = await repo.offer_repo.get_offers(offer_id)
        if offer_model.status in [OfferStatus.COMPLETED, OfferStatus.CANCELED, OfferStatus.BOT_HAVE_NO_RIGHTS]:
            return
        offer_in_work_model = await repo.offer_repo.get_offer_in_work(offer_id=offer_id, user_id_web_master=web_master_id)
        if offer_in_work_model.current_reqeusts_amount < 1:
            await bot.send_message(web_master_id, core.get('no_progress_on_offer', locale, offer_name=offer_model.channel_name))


async def check_current_requests_amount(ctx, offer_id: int, web_master_id: int, locale: str = "uk"):
    db_factory = ctx["db_factory"]
    bot: Bot = ctx["bot"]
    core: FluentRuntimeCore = ctx["core"]
    async with db_factory() as db_session:
        session: AsyncSession = db_session
        repo = Repo(session)
        offer_model = await repo.offer_repo.get_offers(offer_id)
        if offer_model.status in [OfferStatus.COMPLETED, OfferStatus.CANCELED, OfferStatus.BOT_HAVE_NO_RIGHTS]:
            return
        offer_in_work_model = await repo.offer_repo.get_offer_in_work(offer_id=offer_id, user_id_web_master=web_master_id)
        if offer_in_work_model.current_reqeusts_amount < 1:
            await repo.offer_repo.update_offer_in_work(offer_in_work_model.id, status=OfferStatus.CLOSED)
            await bot.send_message(web_master_id, core.get('offer_closed', locale, offer_name=offer_model.channel_name))
