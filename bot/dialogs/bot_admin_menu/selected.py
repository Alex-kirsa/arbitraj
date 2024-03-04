import validators
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_i18n import I18nContext

from . import states
from ..purchase_menu.states import TopUpOperations
from ..selected_main import not_working_zaliv
from ...db import Repo
from ...services.google_sheets_service.google_sheets_service import write_to_google_sheets
from ...services.notification import notificate_web_masters_new_offer
from ...utils.constants import TargetSource, OfferStatus, ChannelStatus, WithdrawStatus, RoleTypes, casinos_dict, GamblingOfferStatus


async def on_select_request_type(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(request_type=item_id)
    await manager.switch_to(states.Requests.select_request)


async def on_select_request(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(request_id=int(item_id))
    await manager.switch_to(states.Requests.show_request)


async def on_enter_second_price_per_request(message: Message, widget: ManagedTextInput, manager: DialogManager, message_text):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    i18n: I18nContext = manager.middleware_data['i18n']
    request_id = manager.dialog_data['request_id']
    offer_model = await repo.offer_repo.get_offers(offer_id=request_id)
    await repo.offer_repo.update_offer(request_id, status=OfferStatus.ACTIVE.value, second_price_per_request=int(message.text))
    await repo.channel_repo.update_channel_for_traffic_status(offer_model.channel_id, status=OfferStatus.ACTIVE.value)
    await message.answer("Заявка принята", show_alert=True)
    await bot.send_message(offer_model.user_id, i18n.get('your_offer_succ_placed_on_platform', offer_name=offer_model.channel_name))
    all_web_masters = await repo.user_repo.get_users(role=RoleTypes.WEB_MASTER)
    print(all_web_masters)
    await notificate_web_masters_new_offer(all_web_masters, bot, i18n, offer_model)
    await manager.switch_to(states.Requests.select_request)


async def on_accept_request(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    i18n: I18nContext = manager.middleware_data['i18n']
    request_id = manager.dialog_data['request_id']
    request_type = manager.dialog_data['request_type']
    if request_type == "offers":
        return await manager.switch_to(states.Requests.enter_second_price_per_request)
    elif request_type == "channels":
        channel_model = await repo.channel_repo.get_channel(id_=request_id)
        if channel_model.status == ChannelStatus.WAIT_ADMIN_CONFIRM:
            await repo.channel_repo.update_channel(request_id, status=ChannelStatus.WAIT_FOR_PAYMENT)
            await manager.bg(channel_model.channel_owner_id, channel_model.channel_owner_id).start(
                TopUpOperations.select_pament_method, data={
                    'payment_for': 'channel_purchase',
                    'channel_id': request_id,
                },
            )
            await call.answer("Отправлен запрос на оплату собственнику канала", show_alert=True)
        elif channel_model.status == ChannelStatus.WAIT_CONFIRM_PAYMENT:
            await repo.channel_repo.update_channel(request_id, status=ChannelStatus.ACTIVE)
            await call.answer("Канал принят", show_alert=True)
            await bot.send_message(channel_model.channel_owner_id, i18n.get('your_channel_is_active', channel_name=channel_model.channel_title))
        return await manager.back()


async def on_reject_request(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    i18n: I18nContext = manager.middleware_data['i18n']
    request_id = manager.dialog_data['request_id']
    request_type = manager.dialog_data['request_type']
    if request_type == "offers":
        offer_model = await repo.offer_repo.get_offers(offer_id=request_id)
        await bot.send_message(offer_model.user_id, i18n.get('your_offer_is_rejected', offer_name=offer_model.channel_name))
        await repo.offer_repo.update_offer(request_id, status=OfferStatus.CANCELED.value)
        await call.answer("Заявка отклонена", show_alert=True)
    elif request_type == "channels":
        channel_model = await repo.channel_repo.get_channel(id_=request_id)
        await bot.send_message(channel_model.channel_owner_id, i18n.get('your_channel_is_rejected', channel_name=channel_model.channel_title))
        await repo.channel_repo.update_channel(request_id, status=ChannelStatus.CANCELED)
    else:
        raise ValueError("Unknown request type")
    await manager.back()


async def on_select_withdraw_request(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(withdraw_request_id=int(item_id))
    await manager.switch_to(states.RequestsOnWithdrawal.show_request_info)


async def on_accept_withdraw_request(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    i18n: I18nContext = manager.middleware_data['i18n']
    request_id = manager.dialog_data['withdraw_request_id']
    withdraw_request = await repo.payment_repo.get_withdraw_requests(request_id)
    await repo.payment_repo.update_withdraw_status(request_id, status=WithdrawStatus.COMPLETED)
    await repo.user_repo.minus_user_balance(withdraw_request.user_id, balance=withdraw_request.amount)
    await repo.user_repo.sum_user_balance(withdraw_request.user_id, earned=withdraw_request.amount)
    await bot.send_message(withdraw_request.user_id, i18n.get('your_withdraw_request_is_accepted', amount=withdraw_request.amount))
    await call.answer("Заявка на вивід коштів принята", show_alert=True)
    await manager.back()


async def on_reject_withdraw_request(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    i18n: I18nContext = manager.middleware_data['i18n']
    request_id = manager.dialog_data['withdraw_request_id']
    withdraw_request = await repo.payment_repo.get_withdraw_requests(id_=request_id)
    await repo.payment_repo.update_withdraw_status(request_id, status=WithdrawStatus.CANCELED)
    await bot.send_message(withdraw_request.user_id, i18n.get('your_withdraw_request_is_rejected', amount=withdraw_request.amount))
    await call.answer("Заявка на вивід коштів відхилена", show_alert=True)
    await manager.back()


async def on_select_user_role(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(user_role=item_id)
    states_mapping = {
        RoleTypes.CHANNEL_OWNER: states.ChannelOwnerInfo.select_channel_status,
        RoleTypes.CHANNEL_ADMIN: states.ChannelAdminsInfo.select_offers,
        RoleTypes.NEWBIE: states.WebMasterInfo.show_general_webmaster_info,
        RoleTypes.WEB_MASTER: states.WebMasterInfo.show_general_webmaster_info,
    }
    await manager.start(states_mapping[item_id])


async def on_select_channel_status(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(channel_status=item_id)
    await manager.switch_to(states.ChannelOwnerInfo.select_theme)


async def on_select_channel_theme(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel_theme=item_id)
    await manager.switch_to(states.ChannelOwnerInfo.selet_channel)


async def on_select_channel(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel_id=int(item_id))
    await manager.switch_to(states.ChannelOwnerInfo.show_channel_info)


async def on_select_offer_status(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer_status=item_id)
    await manager.switch_to(states.ChannelAdminsInfo.select_offer)


async def on_select_offer(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer_id=int(item_id))
    await manager.switch_to(states.ChannelAdminsInfo.show_offer)


async def on_select_webmaster_offer_status(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer_status=item_id)
    await manager.switch_to(states.WebMasterInfo.select_offer)


async def on_select_offer_in_work(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer_id=int(item_id))
    await manager.switch_to(states.WebMasterInfo.show_offer)


async def on_select_source_for_link(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    if item_id in [TargetSource.ONLY_FANS.name, TargetSource.WEB_STORE.name]:
        return await not_working_zaliv(call, widget, manager)
    manager.dialog_data.update(selected_source=item_id)
    await manager.switch_to(states.AddLink.select_casino_name)


async def on_select_casino_name(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_casino_name=item_id)
    await manager.switch_to(states.AddLink.enter_link)


async def on_enter_casino_link(message: Message, widget: ManagedTextInput, manager: DialogManager, message_text):
    links = message_text.split(' ')
    invalid_links = []
    for link in links:
        validate_link = validators.url(link)
        if not validate_link:
            invalid_links.append(link)
            continue
        manager.dialog_data.setdefault('links', []).append(link)
    if invalid_links:
        await message.answer(f"Неправильные ссылки:\n"
                             f"{', '.join(invalid_links, )}\n"
                             f"Небыли добавлены.")


async def on_done_entering_links(call: CallbackQuery, widget: Button, manager: DialogManager):
    links: list = manager.dialog_data.get('links', [])
    repo: Repo = manager.middleware_data['repo']
    casino_name = casinos_dict.get(manager.dialog_data['selected_casino_name'])
    gambling_offer_model = await repo.offer_repo.get_gambling_offers(casino_name=casino_name)
    if not gambling_offer_model:
        gambling_offer_model = await repo.offer_repo.add_gambling_offer(casino_name=casino_name, status=GamblingOfferStatus.ACTIVE)
    for link in links:
        await repo.offer_repo.add_gambling_offer_link(gambling_offer_model.id, link)
    if gambling_offer_model.status == GamblingOfferStatus.NO_ACTIVE_LINK:
        await repo.offer_repo.update_gambling_offer(gambling_offer_model.id, status=GamblingOfferStatus.ACTIVE)
    await call.answer("Ссылки добавлены", show_alert=True)
    await manager.done()


async def on_enter_username(message: Message, widget: ManagedTextInput, manager: DialogManager, message_text):
    repo: Repo = manager.middleware_data['repo']
    all_matched_users = await repo.user_repo.get_user_link(username=message_text)
    if not all_matched_users:
        return await message.answer("Пользователь не найден")
    manager.dialog_data.update(username=message_text)
    await manager.switch_to(states.SearchUser.select_user)


async def on_select_user(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_user_id=int(item_id))
    await manager.switch_to(states.SearchUser.show_user)


async def on_enter_mailing_message(message: Message, widget: ManagedTextInput, manager: DialogManager, message_text):
    manager.dialog_data.update(message=message.html_text)
    await manager.switch_to(states.Mailing.confirm_mailing)


async def on_send_mailing(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    message = manager.dialog_data['message']
    all_users = await repo.user_repo.get_users()
    for user in all_users:
        await bot.send_message(user.user_id, message)
    await call.answer("Рассылка отправлена", show_alert=True)
    await manager.done()


async def on_update_google_table(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    bot: Bot = manager.middleware_data['bot']
    await call.answer("Таблица обновляется. Ожидайте обновления", show_alert=True)
    url = await write_to_google_sheets(repo.session)
    await call.message.answer(f"Таблица обновлена\n"
                              f"{url}")
