from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Url, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states, selected, getters, keyboards

FIRST_START_WINDOW = Window(
    I18NFormat('T_traffic_place_intro_2'),
    keyboards.select_your_role(),
    state=states.FirstStartWindow.select_your_role,
)
