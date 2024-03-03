from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.utils.constants import OfferStatus

router = Router()


@router.chat_join_request()
async def chat_join_handler(request: ChatJoinRequest, repo: Repo, bot: Bot, i18n: I18nContext, dialog_manager: DialogManager):
    invite_link = request.invite_link.invite_link
    offer_in_work = await repo.offer_repo.get_offer_in_work(channel_invite_link=invite_link)
    if not offer_in_work:
        return
    if offer_in_work.status != OfferStatus.IN_WORK:
        return
    user_exists = await repo.offer_repo.get_channel_invite_requests_by_user_id(request.chat.id, invite_link)
    if user_exists:
        return
    offer_model = await repo.offer_repo.get_offers(offer_in_work.offer_id)
    await repo.offer_repo.add_channel_invite_request(request.from_user.id, offer_model.channel_id, invite_link, offer_in_work.offer_id)
    await repo.offer_repo.update_offer_in_work(offer_in_work.id, current_reqeusts_amount=offer_in_work.current_reqeusts_amount + 1,
                                               earned_money=offer_in_work.earned_money + offer_model.second_price_per_request)
    web_manster_user_model = await repo.user_repo.get_user(offer_in_work.user_id_web_master)
    if web_manster_user_model.refferer_id:
        await repo.user_repo.sum_user_balance(web_manster_user_model.refferer_id,
                                              balance=offer_model.second_price_per_request * 0.05,
                                              earned=offer_model.second_price_per_request * 0.05,
                                              earned_from_referals=offer_model.second_price_per_request * 0.05)
    await repo.offer_repo.update_offer(offer_id=offer_in_work.offer_id, money_reserved=offer_model.money_reserved - offer_model.first_price_per_request)
    await repo.user_repo.sum_user_balance(offer_in_work.user_id_web_master, balance=offer_model.second_price_per_request, earned=offer_model.second_price_per_request)

    offers_in_work = await repo.offer_repo.get_offer_in_work(offer_in_work.offer_id)
    sum_all_requests = sum([offer.current_reqeusts_amount for offer in offers_in_work])
    if sum_all_requests >= offer_model.target_request_amount:
        await repo.offer_repo.update_offer_in_work(offer_id=offer_in_work.offer_id, status=OfferStatus.COMPLETED)
        await repo.offer_repo.update_offer(offer_id=offer_in_work.offer_id, status=OfferStatus.COMPLETED)
        return
    requests_amount_left = offer_model.target_request_amount - sum_all_requests
    percent_left = (requests_amount_left / offer_model.target_request_amount) * 100
    if percent_left <= 10:
        for web_master_offer in offers_in_work:
            await bot.send_message(web_master_offer.user_id_web_master,
                                   i18n.get('left_less_10_percent_requests', offer_name=offer_model.channel_name))
