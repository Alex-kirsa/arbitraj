from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from . import states
from ..channel_admin_menu.states import ChannelAdminPersonalCabinet


async def on_select_channel(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel=int(item_id))
    await manager.switch_to(states.UserChannels.channel_info)


async def on_select_channel_topic(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(selected_channel_topic=item_id)
    await manager.switch_to(states.ChannelPosterOwnerMenu.show_channels)


async def on_select_personal_cabinet(call: CallbackQuery, widget: Button, manager: DialogManager):
    state = states.ChannelOwnerPersonalCabinet.select_action if manager.start_data and manager.start_data.get('user_type') == 'channel_owner' else ChannelAdminPersonalCabinet.select_action
    await manager.start(state)