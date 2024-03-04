from aiogram import Router, Bot
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.dialogs.bot_admin_menu.states import MainAdminMenu
from bot.dialogs.channel_admin_menu.states import ChannelAdminMainMenu as ChannelAdminMainMenu
from bot.dialogs.channel_owner_menu.states import ChannelOwnerMainMenu as ChannelOwnerMainMenu
from bot.dialogs.start_menu.states import FirstStartWindow
from bot.dialogs.web_master_menu.states import MainMenu as WebMasterMainMenu
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.utils.constants import RoleTypes
from configreader import config

router = Router()
router.message.middleware(ThrottlingMiddleware())


@router.message(CommandStart())
async def start(message: Message, command: CommandObject, i18n: I18nContext, dialog_manager: DialogManager, repo: Repo, bot: Bot, state: FSMContext):
    await state.clear()
    user_model = await repo.user_repo.get_user(message.from_user.id)
    if not user_model or not user_model.role:
        refferer_id = command.args
        await repo.user_repo.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username, int(refferer_id) if refferer_id else None,)
        return await dialog_manager.start(FirstStartWindow.select_your_role, mode=StartMode.RESET_STACK, data={'first_init': True})
    menu_mapping = {
        RoleTypes.WEB_MASTER: WebMasterMainMenu.select_action,
        RoleTypes.CHANNEL_OWNER: ChannelOwnerMainMenu.select_action,
        RoleTypes.CHANNEL_ADMIN: ChannelAdminMainMenu.select_action,
        RoleTypes.NEWBIE: WebMasterMainMenu.select_action
    }
    return await dialog_manager.start(menu_mapping[user_model.role], mode=StartMode.RESET_STACK)


@router.message(Command('admin'))
async def admin_start(message: Message, dialog_manager: DialogManager):
    if message.chat.id in config.admins or message.chat.id in config.devs:
        await dialog_manager.start(MainAdminMenu.select_action)