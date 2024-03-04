from aiogram import Router, Bot, Dispatcher
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated
from aiogram_dialog import DialogManager, ShowMode
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.dialogs.purchase_menu.states import TopUpOperations
from bot.filters.bot_reg_filters import AddBotOnCreateOffer, DelBotFilter
from bot.utils.constants import OfferStatus
from bot.utils.misc import check_enough_rights

router = Router()


@router.my_chat_member(AddBotOnCreateOffer())
async def add_bot_handler(
        update: ChatMemberUpdated,
        dp: Dispatcher,
        dialog_manager: DialogManager,
        repo: Repo,
        bot: Bot,
        i18n: I18nContext,
):
    inviter_id = update.from_user.id
    bot_rights = update.new_chat_member
    chat_id = update.chat.id
    chat_title = update.chat.title
    await i18n.set_locale("uk")
    channel_model = await repo.channel_repo.get_channel_for_traffic(chat_id)
    state = dp.fsm.get_context(bot=bot, user_id=inviter_id, chat_id=inviter_id)
    if channel_model:
        if not await check_enough_rights(bot_rights):
            return await bot.send_message(inviter_id, i18n.get("not_enough_bot_rights_error"))
        else:
            return await bot.send_message(inviter_id, i18n.get("channel_already_added"))
    else:
        if not await check_enough_rights(bot_rights):
            return await bot.send_message(inviter_id, i18n.get("not_enough_bot_rights_error"))
        else:
            bg = dialog_manager.bg(user_id=inviter_id, chat_id=inviter_id)
            dialog_data = await state.get_data()
            channel_data = {
                'channel_id': chat_id,
                'channel_title': chat_title,
                'channel_owner_id': inviter_id,
            }
            await repo.channel_repo.add_channe_for_traffic(**channel_data)
            offer_data = {
                'user_id': inviter_id,
                'target_source': dialog_data.get('selected_target_source'),
                'traffic_source': dialog_data.get('selected_traffic_source'),
                'channel_id': chat_id,
                'channel_name': update.chat.title,
                'channel_theme': dialog_data.get('channel_theme'),
                'custom_channel_theme': dialog_data.get('custom_channel_theme'),
                'target_request_amount': dialog_data.get('amount_requests'),
                'first_price_per_request': dialog_data.get('price_per_request'),
                'money_reserved': 0,
                'offer_deadline': dialog_data.get('deadline'),
                'traffic_rules': dialog_data['traffic_rules'],
                'comment': dialog_data.get('comment'),
                'contacts': dialog_data.get('contact'),
                'status': OfferStatus.WAIT_FOR_PAYMENT,
            }
            offer_model = await repo.offer_repo.add_offer(offer_data)
            data = {
                'offer_id': offer_model.id,
                'payment_for': 'offer_purchase'
            }
            data.update(offer_data)
            await state.update_data(data)
            # await bg.update(data)
            await dialog_manager.bg(user_id=inviter_id, chat_id=inviter_id).start(
                TopUpOperations.select_pament_method, show_mode=ShowMode.DELETE_AND_SEND,
                data=data
            )
            # await dp.fsm.get_context(bot, inviter_id, inviter_id).clear()


@router.my_chat_member(DelBotFilter())
async def del_bot_from_channel(
        update: ChatMemberUpdated,
        repo: Repo,
        bot: Bot,
        i18n: I18nContext,
):
    inviter_id = update.from_user.id
    bot_rights = update.new_chat_member
    chat_id = update.chat.id
    chat_title = update.chat.title
    await i18n.set_locale("uk")
    offers_in_channel = await repo.offer_repo.get_offers(channel_id=chat_id, status=[OfferStatus.IN_WORK, OfferStatus.ACTIVE])
    if offers_in_channel and bot_rights.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.RESTRICTED):
        await repo.offer_repo.update_offer(offers_in_channel.id, status=OfferStatus.BOT_HAVE_NO_RIGHTS)
        return await bot.send_message(update.from_user.id, i18n.get("bot_was_deleted_from_channel", channel_name=update.chat.title))
    elif offers_in_channel and not await check_enough_rights(bot_rights):
        await repo.offer_repo.update_offer(offers_in_channel.id, status=OfferStatus.BOT_HAVE_NO_RIGHTS)
        return await bot.send_message(update.from_user.id, i18n.get("bot_was_deleted_from_channel", channel_name=update.chat.title))
