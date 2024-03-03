from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states, selected, keyboards

FIRST_START_WINDOW = Window(
    I18NFormat('T_traffic_place_intro_2'),
    keyboards.select_your_role(),
    state=states.FirstStartWindow.select_your_role,
)


COOPERATION = Window(
    I18NFormat('T_cooperation'),
    TextInput(
        id='cooperation_message',
        on_success=selected.on_send_coop_message,
    ),
    Cancel(I18NFormat('I_back')),
    state=states.Cooperation.send_cooperation_message,
)