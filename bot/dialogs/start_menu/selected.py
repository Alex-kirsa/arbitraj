from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from bot.db import Repo
from bot.dialogs.channel_admin_menu.states import ChannelAdminMainMenu as ChannelAdminMenu
from bot.dialogs.channel_owner_menu.states import ChannelOwnerMainMenu as ChannelOwnerMenu
from bot.dialogs.web_master_menu.states import MainMenu as WebMasterMenu
from bot.utils.constants import RoleTypes
from configreader import config


async def on_select_webmaster(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    repo: Repo = dialog_manager.middleware_data['repo']
    start_data = dialog_manager.start_data
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.WEB_MASTER)
    await dialog_manager.start(WebMasterMenu.select_action, data=start_data)


async def on_select_newbie(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    repo: Repo = dialog_manager.middleware_data['repo']
    start_data = dialog_manager.start_data
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.NEWBIE)
    await dialog_manager.start(WebMasterMenu.select_action, data=start_data)


async def on_select_sell_traffic(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    repo: Repo = dialog_manager.middleware_data['repo']
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.CHANNEL_OWNER)
    await dialog_manager.start(ChannelOwnerMenu.select_action)


async def on_select_buy_traffic(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    repo: Repo = dialog_manager.middleware_data['repo']
    await repo.user_repo.update_user_role(call.from_user.id, RoleTypes.CHANNEL_ADMIN)
    await dialog_manager.start(ChannelAdminMenu.select_action)


async def on_send_coop_message(message: Message, widget: ManagedTextInput, manager: DialogManager, message_text):
    bot: Bot = manager.middleware_data['bot']
    text_for_channel = (f'Користувач {message.from_user.full_name} @{message.from_user.username}:\n'
                        f'Співпраця:\n\n'
                        f' {message.html_text}')
    await bot.send_message(config.cooperation_channel_id, text_for_channel)
    await message.answer('Ваше повідомлення відправлено')
    await manager.done()