import operator

from aiogram_dialog.widgets.kbd import Group, Start, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states


def select_action():
    return Group(
        Start(
            I18NFormat("I_add_channel"),
            id='I_add_channel',
            state=states.AddChannel.enter_webapp_form,
        ),
        Start(
            I18NFormat("I_channel_poster"),
            id='I_channel_poster',
            state=states.ChannelPosterOwnerMenu.select_channel_topic,
        ),
        Start(
            I18NFormat("I_personal_cabinet"),
            id='I_personal_cabinet',
            state=states.ChannelOwnerPersonalCabinet.select_action
        ),
        width=1
    )


def personal_cabinet_kb():
    return Group(
        Start(
            I18NFormat("I_add_channel"),
            id='I_add_channel',
            state=states.AddChannel.enter_webapp_form,
        ),
        Start(
            I18NFormat("I_active_channels"),
            id='I_active_channels',
            state=states.UserChannels.select_channel,
        ),
        Button(I18NFormat("I_withdraw_funds"), id='I_withdraw_funds')
    )


def select_payment_method(user_type: str):
    return Group(
        Button(
            Const("CryptoPay"),
            id='I_pay_via_cryptopay',
        ),
        Start(
            I18NFormat("I_payment_card"),
            id='I_payment_card',
            state=states.PayViaCard.show_payment_info,
            data={'user_type': user_type}
        ),
        Button(
            I18NFormat("I_support"),
            id='I_support',
        ),
        width=1
    )


def channels_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='channel',
            items='user_channels',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        id='channels_kb_s_g',
        width=1,
        height=6,
        hide_on_single_page=True
    )


def channel_topics_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='channel_topic',
            items='channel_topics',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        id='channel_topics_kb_s_g',
        width=1,
        height=6,
        hide_on_single_page=True
    )


def get_channels_kb(on_click=None):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='channel',
            items='channels_list',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        id='channels_kb_s_g',
        width=1,
        height=6,
        hide_on_single_page=True
    )


