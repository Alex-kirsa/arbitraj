import operator

from aiogram_dialog.widgets.kbd import Group, Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from bot.dialogs.web_master_menu import selected
from bot.utils.constants import RoleTypes
from bot.utils.i18n_utils.i18n_format import I18NFormat


def select_action():
    return Group(
        Button(
            I18NFormat("I_select_offer"),
            id='I_select_web_master_offer',
            # state=states.SelectWebMasterOffer.select_category
            on_click=selected.on_start_select_offer
        ),
        Group(
            Button(
                I18NFormat("I_bot_info"),
                id='I_bot_info',
                on_click=None,
            ),
            Button(
                I18NFormat('I_personal_cabinet'),
                id='I_personal_cabinet',
                on_click=selected.on_start_personal_cabinet,
                when=~F['first_init']
            ),
            when=F['user_role'] != RoleTypes.NEWBIE
        ),
        width=1

    )


def personal_cabinet_menu():
    return Group(
        Button(
            I18NFormat('I_select_new_offer'),
            id='I_select_new_offer',
            on_click=selected.on_start_select_offer,
        ),
        Button(
            I18NFormat('I_my_offers'),
            id='I_my_offers',
            on_click=selected.on_select_my_offer,
        ),
        Button(
            I18NFormat('I_withdraw_funds'),
            id='I_withdraw_funds',
            on_click=selected.on_select_withdraw_funds,
        ),
        Button(
            I18NFormat('I_referral_system'),
            id='I_referral_system',
            on_click=None,
        ),
        Button(
            I18NFormat('I_support'),
            id='I_support',
            on_click=None,
        ),

        width=1
    )


def select_category(on_click):
    return Group(
        Select(
            Format("{item[1]}"),
            id='categories_kb',
            items='categories_list',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        width=1
    )


def select_traffic_source(on_click):
    return Group(
        Select(
            Format("{item[1]}"),
            id='traffic_sources_kb',
            items='traffic_sources_list',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        width=1
    )


def select_offer(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='offers_kb',
            items='offers_list',
            item_id_getter=operator.itemgetter(0),
            on_click=on_click
        ),
        id='offers_kb_s_g',
        width=1,
        height=6,
        hide_on_single_page=True
    )
