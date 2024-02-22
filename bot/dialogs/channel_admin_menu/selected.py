from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from . import states
from ..selected_main import not_working_zaliv, not_working_traffic_source
from ...utils.constants import TrafficSource


async def on_select_offer(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_offer=int(item_id))
    await manager.switch_to(states.ChannelAdminPersonalCabinet.show_offer_info)


async def on_select_channel_topic(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel_topic=item_id)
    await manager.switch_to(states.ChannelPosterAdminMenu.select_channel)


async def on_select_category(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id in ['only_fans', 'web_store', 'gambling']:
        return await not_working_zaliv(call, widget, dialog_manager)

    dialog_manager.dialog_data.update(selected_category=item_id)
    await dialog_manager.switch_to(states.CreateOffer.select_source)


async def on_select_traffic_source(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_traffic_source=item_id)
    if item_id not in [TrafficSource.TG_CHANNEL, TrafficSource.REALS, TrafficSource.TIK_TOK]:
        return await not_working_traffic_source(call, widget, dialog_manager)
    if item_id == TrafficSource.TG_CHANNEL:
        return await dialog_manager.start(states.CreateOfferFromTGTraffic.select_topic)

    await dialog_manager.switch_to(states.CreateOffer.confirm)


async def on_select_topic_of_tg_traffic_channel(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_topic=item_id)
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.select_criteria_for_sort)


async def on_select_criteria_for_sort(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(selected_channel_topic='test123')
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.select_channel)


async def on_select_channel(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_channel=int(item_id))
    await dialog_manager.switch_to(states.CreateOfferFromTGTraffic.show_channel_info)

