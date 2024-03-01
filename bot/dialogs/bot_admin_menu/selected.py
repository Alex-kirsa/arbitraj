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
from ...utils.constants import TrafficSource, TargetSource
from ...utils.misc import get_link_on_tg_user

