import operator

from aiogram_dialog.widgets.kbd import Group, Start, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states, selected


def select_action():
    return Group(
        Start(I18NFormat("I_create_offer"), "I_create_offer",
              state=states.CreateOffer.select_target_source),
        Start(I18NFormat("I_channel_poster"), "I_channel_poster",
              state=states.ChannelPosterAdminMenu.select_topic),
        Start(I18NFormat("I_personal_cabinet"), "I_personal_cabinet",
              state=states.ChannelAdminPersonalCabinet.select_offer_status),

    )


def criterias_kb(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id="criterias",
            items="criteria_list",
            item_id_getter=operator.itemgetter(0),
            on_click=on_click,
        ),
        width=1,
    )


def offers_statuses(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id="offer_status",
            items="offer_statuses",
            item_id_getter=operator.itemgetter(0),
            on_click=on_click,
        ),
        width=1,
    )


def offers_kb(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[1]}'),
            id="offers",
            items="offers",
            item_id_getter=operator.itemgetter(0),
            on_click=on_click,
        ),
        id='offers_scrolling',
        height=6,
        width=1,
        hide_on_single_page=True,
    )