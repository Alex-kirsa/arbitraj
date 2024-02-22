from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo, Start, Row
from aiogram_dialog.widgets.text import Multi
from magic_filter import F

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.dialogs.web_master_menu import keyboards, states, getters, selected
from bot.utils.constants import RoleTypes
from bot.utils.i18n_utils.i18n_format import I18NFormat


def main_menu():
    return Window(
        I18NFormat('T_traffic_place'),
        keyboards.select_action(),
        Start(I18NFormat('I_back_to_selection'), id='back_to_first_menu',
              state=FirstStartWindow.select_your_role, mode=StartMode.RESET_STACK),
        state=states.MainMenu.select_action,
        getter=getters.get_main_menu_data,
    )


def personal_cabinet_window():
    return Window(
        I18NFormat('T_personal_cabinet_intro'),
        keyboards.personal_cabinet_menu(),
        Cancel(I18NFormat('I_back')),
        state=states.PersonalCabinet.show_personal_info,
        getter=getters.get_personal_cabinet_data,
    )


def select_offer_window():
    return Window(
        Multi(
            Multi(
                I18NFormat('T_available_categories', when=~F['personal_offers']),
                I18NFormat('T_user_offers_menu', when=F['personal_offers']),
                when=F['user_role'] != RoleTypes.NEWBIE
            ),
            I18NFormat('T_select_target_for_traffic_newbie', when=F['user_role'] == RoleTypes.NEWBIE),
        ),
        keyboards.select_category(selected.on_select_category),
        Cancel(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.select_category,
        getter=getters.get_select_offer_data,
    )


def select_traffic_source_window():
    return Window(
        I18NFormat('T_select_traffic_source'),
        keyboards.select_traffic_source(selected.on_select_traffic_source),
        Back(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.select_traffic_source,
        getter=getters.get_select_traffic_source_data,
    )


def select_offer():
    return Window(
        Multi(
            I18NFormat('I_all_available_offers', when=~F['personal_offers']),
            I18NFormat('T_active_offers_menu', when=F['personal_offers']),
        ),
        keyboards.select_offer(selected.on_select_offer),
        Back(I18NFormat('I_back'), when=~F['personal_offers']),
        SwitchTo(I18NFormat('I_back'), id='back_to_select_category', state=states.SelectWebMasterOffer.select_category, when=F['personal_offers']),
        state=states.SelectWebMasterOffer.select_webmaster_offer,
        getter=getters.get_offers,
    )


def offer_info_window():
    return Window(
        Multi(
            I18NFormat('T_offer_info', when=F['selected_category'].in_(['tg_channel_requests'])),
            I18NFormat('T_offer_info_gambling', when=F['selected_category'].in_(['gambling'])),
        ),
        Button(I18NFormat("I_take_link"), id='I_take_link', on_click=selected.on_take_offer, when=~F['personal_offers']),
        Back(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.show_offer_info,
        getter=getters.get_offer_info,
    )


def withdraw_window():
    return Window(
        I18NFormat('T_financial_report'),
        Button(I18NFormat('I_withdraw_request'), id='I_withdraw_request', on_click=None),
        Row(Cancel(I18NFormat('I_back')), Start(I18NFormat('I_back_to_menu'),
                                                id='back_to_menu', state=states.MainMenu.select_action, mode=StartMode.RESET_STACK)),
        state=states.WithdrawFunds.show_withdraw_menu,
        getter=getters.get_account_info
    )
