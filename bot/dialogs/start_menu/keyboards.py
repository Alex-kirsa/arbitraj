from aiogram_dialog.widgets.kbd import Group, Button, Start
from aiogram_dialog.widgets.text import Const

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import selected, states
from ..bot_admin_menu.states import MainAdminMenu


def select_your_role():
    return Group(
        Button(
            I18NFormat("I_buy_traffic"),
            id='i_buy_traffic',
            on_click=selected.on_select_buy_traffic,
        ),
        Button(
            I18NFormat("I_sell_traffic"),
            id='I_sell_traffic',
            on_click=selected.on_select_sell_traffic,
        ),
        Button(
            I18NFormat("I_webmaster"),
            id='I_webmaster',
            on_click=selected.on_select_webmaster,
        ),
        Button(
            I18NFormat("I_traffic_newbie"),
            id='I_traffic_newbie',
            on_click=selected.on_select_newbie,
        ),
        Button(
            I18NFormat("I_more_about_bot"),
            id='I_more_about_bot',
            on_click=None,
        ),
        Start(
            Const("Співпраця"),
            id='cooperation',
            state=states.Cooperation.send_cooperation_message,
        ),
        # Start(
        #     Const("Админ панель"),
        #     id='admin_panel',
        #     state=MainAdminMenu.select_action,
        # ),
        width=2
    )