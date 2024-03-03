from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_i18n import I18nContext

from . import states
from ..selected_main import not_working_zaliv, not_working_traffic_source
from ..web_master_menu.states import MainMenu
from ...db import Repo
from ...utils.constants import TrafficSource, TargetSource, RoleTypes
from ...utils.misc import get_link_on_tg_user


async def on_select_offer(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer_id=int(item_id))
    await manager.start(states.AdminOffers.show_offer_info, data=manager.dialog_data)


async def on_select_channel_theme(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel_theme=item_id)
    await manager.switch_to(states.ChannelPosterAdminMenu.select_channel)


async def on_select_target_source(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id in [TargetSource.ONLY_FANS.name, TargetSource.WEB_STORE.name]:
        return await not_working_zaliv(call, widget, dialog_manager)
    dialog_manager.dialog_data.update(selected_target_source=item_id)
    await dialog_manager.switch_to(states.CreateOffer.select_traffic_source)


async def on_select_traffic_source(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_traffic_source=item_id)
    if item_id not in [TrafficSource.TG_CHANNEL, TrafficSource.REELS, TrafficSource.TIK_TOK]:
        return await not_working_traffic_source(call, widget, dialog_manager)
    if item_id == TrafficSource.TG_CHANNEL:
        return await dialog_manager.start(states.CreateOfferFromTGTraffic.select_theme)
    await dialog_manager.switch_to(states.CreateOffer.enter_offer_data)


async def on_select_topic_of_tg_traffic_channel(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_topic=item_id)
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.select_criteria_for_sort)


async def on_select_criteria_for_sort(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_criteria_for_sort=item_id)
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.select_channel)


async def on_select_channel(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_channel_id=int(item_id))
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.show_channel_info)


async def on_change_sort_criteria(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    current_sort_criteria = dialog_manager.dialog_data.get('sort_criteria', 'asc')
    dialog_manager.dialog_data.update(sort_criteria='asc' if current_sort_criteria == 'desc' else 'desc')


async def on_accept_channel(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.enter_comment)


async def on_enter_comment(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, message_text: str):
    repo: Repo = dialog_manager.middleware_data['repo']
    bot: Bot = dialog_manager.middleware_data['bot']
    i18n: I18nContext = dialog_manager.middleware_data['i18n']
    selected_channel_model = await repo.channel_repo.get_channel(dialog_manager.dialog_data['selected_channel_id'])
    owner_id = selected_channel_model.channel_owner_id
    username = message.from_user.username if message.from_user.username else f"<a href='{get_link_on_tg_user(owner_id)}'>{message.from_user.full_name}</a>"
    text = i18n.get('T_new_offer_request', username=username, comment=message_text)
    await bot.send_message(owner_id, text)
    await message.answer(i18n.get('T_request_successfuly_sent'))
    await dialog_manager.start(MainMenu.select_action, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def on_select_offer_status(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_offer_status=item_id)
    await dialog_manager.start(states.AdminOffers.select_offer, data=dialog_manager.dialog_data)


async def on_select_webmaster(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    start_data = manager.start_data
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.WEB_MASTER)


async def on_select_sell_traffic(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data['repo']
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.CHANNEL_OWNER)
