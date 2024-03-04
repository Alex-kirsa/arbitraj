import operator

from aiogram_dialog.widgets.kbd import Group, Start, Button, ScrollingGroup, Select, WebApp, Url
from aiogram_dialog.widgets.text import Const, Format

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import selected
from . import states
from ..channel_admin_menu.states import ChannelAdminMainMenu
from ..web_master_menu.states import MainMenu
from ...utils.constants import WebAppUrls, SUPPORT_URL


def select_action():
    return Group(
        WebApp(
            I18NFormat("I_add_channel"),
            Const(WebAppUrls.ADD_CHANNEL_WEB_APP.value)
        ),
        Start(
            I18NFormat("I_channel_poster"),
            id='I_channel_poster',
            state=states.ChannelPosterOwnerMenu.select_channel_topic,
        ),
        Start(
            I18NFormat("I_personal_cabinet"),
            id='I_personal_cabinet',
            state=states.ChannelOwnerPersonalCabinet.select_action,
            when='have_channel'
        ),
        width=2
    )


def personal_cabinet_kb():
    return Group(

        WebApp(
            I18NFormat("I_add_channel"),
            Const(WebAppUrls.ADD_CHANNEL_WEB_APP.value)
        ),
        Start(
            I18NFormat("I_active_channels"),
            id='I_active_channels',
            state=states.UserChannels.select_channel,
        ),
        Start(
            I18NFormat("I_buy_traffic"),
            id='i_buy_traffic',
            on_click=selected.on_select_buy_traffic,
            state=ChannelAdminMainMenu.select_action
        ),
        Start(
            I18NFormat("I_webmaster"),
            id='I_webmaster',
            on_click=selected.on_select_webmaster,
            state=MainMenu.select_action
        ),
        Url(
            I18NFormat('I_support'),
            Const(SUPPORT_URL)

        ),
        width=2

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


def channel_theme_kb(on_click):
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
