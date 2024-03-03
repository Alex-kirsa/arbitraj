from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Cancel, Back, Start, Row, WebApp, Url, Button
from aiogram_dialog.widgets.text import Multi, Case, Const, Format
from magic_filter import F

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.dialogs.web_master_menu import keyboards, states, getters, selected
from bot.utils.constants import RoleTypes, TargetSource, WebAppUrls
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


def select_new_offer_window():
    return Window(
        Multi(
            I18NFormat('T_available_categories', when=F['user_role'] != RoleTypes.NEWBIE),
            I18NFormat('T_select_target_for_traffic_newbie', when=F['user_role'] == RoleTypes.NEWBIE),
        ),
        keyboards.select_target_source(selected.on_select_target_source),
        Cancel(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.select_category,
        getter=getters.get_target_sources,
    )


def select_traffic_source_window():
    return Window(
        I18NFormat('T_select_traffic_source'),
        keyboards.select_traffic_source(selected.on_select_traffic_source),
        Back(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.select_traffic_source,
        getter=getters.get_select_traffic_source_data,
    )


def select_offer_window():
    return Window(
        I18NFormat('I_all_available_offers'),
        keyboards.select_offer(selected.on_select_offer),
        Back(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.select_webmaster_offer,
        getter=getters.get_offers,
    )


def show_offer_info_window():
    return Window(
        Case(
            {
                TargetSource.TG_CHANNEL.name: Multi(
                    I18NFormat('T_offer_info'),
                    I18NFormat('requests_amount_left'),
                    sep='\n\n'
                ),
                TargetSource.GAMBLING.name: Multi(
                    I18NFormat('T_offer_info_gambling'),
                    # I18NFormat('deposit_and_link'),
                    sep='\n\n'
                )
            },
            selector='selected_target_source'
        ),
        Button(I18NFormat('I_take_offer'), id='take_offer', on_click=selected.on_take_offer),
        Back(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.show_offer_info,
        getter=getters.get_offer_info,
    )


def take_offer_window():
    return Window(
        Multi(
            I18NFormat('offer_took'),
            Case(
                {
                    TargetSource.TG_CHANNEL.name: Multi(
                        I18NFormat('T_offer_info'),
                        I18NFormat('requests_amount_left'),
                        I18NFormat('link_for_offer'),

                        sep='\n\n'
                    ),
                    TargetSource.GAMBLING.name: Multi(
                        I18NFormat('T_offer_info_gambling'),
                        I18NFormat('deposit_and_link'),
                        sep='\n\n'
                    )
                },
                selector='selected_target_source'
            ),
            sep='\n\n'
        ),
        Cancel(I18NFormat('I_back')),
        state=states.SelectWebMasterOffer.took_offer_action,
        getter=getters.get_taked_offer_info,
        disable_web_page_preview=True

    )


def withdraw_window():
    return Window(
        I18NFormat('T_financial_report'),
        WebApp(I18NFormat('ask_for_withdraw'), Const(WebAppUrls.WITHDRAW_FUNDS_WEB_APP.value), when=F['balance'] > 250),
        Row(
            Cancel(I18NFormat('I_back')),
            Start(I18NFormat('I_back_to_menu'),
                  id='back_to_menu', state=states.MainMenu.select_action, mode=StartMode.RESET_STACK)
        ),
        state=states.WithdrawFunds.show_withdraw_menu,
        getter=getters.get_account_info
    )


def save_withdraw_data_window():
    return Window(
        I18NFormat('T_withdraw_data'),
        Start(I18NFormat('main_menu'), id='back_to_menu', state=states.MainMenu.select_action, mode=StartMode.RESET_STACK),
        state=states.WithdrawFunds.save_withdraw_data,
    )


def referral_system_window():
    return Window(
        I18NFormat('T_referral_system'),
        Url(I18NFormat('share_link'), Format("https://telegram.me/share/url?url={link}")),
        Cancel(I18NFormat('back')),
        state=states.ReferalSystem.show_referal_menu,
        getter=getters.get_referral_system_data,
        disable_web_page_preview=True
    )


def my_offers_window():
    return Window(
        I18NFormat('T_user_offers_menu'),
        keyboards.select_target_source(selected.on_select_target_source_in_my_offers),
        Cancel(I18NFormat('I_back')),
        state=states.MyOffers.select_target_source,
        getter=getters.get_target_sources,
    )


def select_my_offer_window():
    return Window(
        I18NFormat('T_active_offers_menu'),
        keyboards.select_offer(selected.on_select_offer_my_offere),
        Back(I18NFormat('I_back')),
        state=states.MyOffers.select_offer,
        getter=getters.get_offers_in_user,
    )


def show_my_offer_info_window():
    return Window(
        Case(
            {
                TargetSource.TG_CHANNEL.name: Multi(
                    I18NFormat('T_offer_info'),
                    I18NFormat('offer_progress'),
                    I18NFormat('link_for_offer'),
                    sep='\n\n'
                ),
                TargetSource.GAMBLING.name: Multi(
                    I18NFormat('T_offer_info_gambling'),
                    I18NFormat('deposit_and_link'),
                    sep='\n\n'
                )
            },
            selector='selected_target_source'
        ),
        Back(I18NFormat('I_back')),
        state=states.MyOffers.show_my_offer_info,
        getter=getters.get_offer_info_in_user,
        disable_web_page_preview=True
    )
