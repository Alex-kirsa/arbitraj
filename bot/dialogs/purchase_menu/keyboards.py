import operator

from aiogram_dialog.widgets.kbd import Group, Select, Button, Url
from aiogram_dialog.widgets.text import Format, Const

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import selected


def select_payment_method():
    return Group(
        Url(
            Const("CryptoBot"),
            Format("{pay_url}"),
            when='pay_url'
        ),
        Select(
            Format("{item[1]}"),
            id='pamyment_method',
            item_id_getter=operator.itemgetter(0),
            items='payment_methods',
            on_click=selected.on_select_payment_method,

        ),
        Button(
            I18NFormat("I_support"),
            id='I_support',
        ),
        width=1
    )
