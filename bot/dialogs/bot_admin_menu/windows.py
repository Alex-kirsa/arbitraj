from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, SwitchTo, Start, Button, Group, WebApp, Url
from aiogram_dialog.widgets.text import Multi, Const, Format, Case
from magic_filter import F

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import keyboards, states, getters, selected
from ..channel_owner_menu.getters import get_channel_themes
from ..channel_owner_menu.keyboards import channel_theme_kb, get_channels_kb
from ..web_master_menu.keyboards import select_offer, select_target_source, select_traffic_source
from ...utils.constants import WebAppUrls, OfferStatus

