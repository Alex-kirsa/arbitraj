from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, SwitchTo, Start, Button, Group, WebApp, Url
from aiogram_dialog.widgets.text import Multi, Const, Format, Case
from magic_filter import F

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import keyboards, states, getters, selected
from ..channel_owner_menu.getters import get_channel_themes
from ..channel_owner_menu.keyboards import channel_theme_kb, get_channels_kb
from ..channel_owner_menu.states import ChannelOwnerMainMenu
from ..web_master_menu.keyboards import select_offer, select_target_source, select_traffic_source
from ..web_master_menu.states import MainMenu
from ...utils.constants import WebAppUrls, OfferStatus, SUPPORT_URL


def main_menu_window():
    return Window(
        I18NFormat('T_traffic_place'),
        keyboards.select_action(),
        Start(I18NFormat('I_back_to_selection'), id='back_to_first_menu',
              state=FirstStartWindow.select_your_role, mode=StartMode.RESET_STACK),
        state=states.ChannelAdminMainMenu.select_action,
        getter=getters.get_main_menu_data,
    )


def personal_cabinet_window():
    return Window(
        I18NFormat('T_personal_cabinet_admin_channel'),
        Group(
            Start(I18NFormat("I_create_offer"), "I_create_offer",
                  state=states.CreateOffer.select_target_source),
            Start(
                I18NFormat("I_sell_traffic"),
                id='I_sell_traffic',
                on_click=selected.on_select_sell_traffic,
                state=ChannelOwnerMainMenu.select_action
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
        ),
        keyboards.offers_statuses(selected.on_select_offer_status),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelAdminPersonalCabinet.select_offer_status,
        getter=getters.get_personal_cabinet_data,
    )


def select_offer_window():
    return Window(
        Case(
            {
                OfferStatus.ACTIVE.value: I18NFormat('I_all_active_offers'),
                OfferStatus.COMPLETED.value: I18NFormat('I_all_completed_offers'),
            },
            selector='offer_status'
        ),
        select_offer(selected.on_select_offer),
        Cancel(I18NFormat('I_back')),
        state=states.AdminOffers.select_offer,
        getter=getters.get_admin_offers,
    )


def show_offer_info_window():
    return Window(
        I18NFormat('T_offer_info'),
        Cancel(I18NFormat('I_back'), when='first_window'),
        Back(I18NFormat('I_back'), when=~F['first_window']),
        state=states.AdminOffers.show_offer_info,
        getter=getters.get_offer_info,
    )


def select_topic_window():
    return Window(
        I18NFormat('T_select_channel_theme'),
        channel_theme_kb(selected.on_select_channel_theme),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelPosterAdminMenu.select_topic,
        getter=get_channel_themes,
    )


def select_channels_window():
    return Window(
        I18NFormat('T_u_open_all_channels'),
        keyboards.offers_kb(selected.on_select_offer),
        Back(I18NFormat('I_back')),
        state=states.ChannelPosterAdminMenu.select_channel,
        getter=getters.get_offers_with_theme,
    )


def create_offer_window():
    return Window(
        I18NFormat('I_select_target_for_traffic'),
        select_target_source(selected.on_select_target_source),
        Cancel(I18NFormat('I_back')),
        state=states.CreateOffer.select_target_source,
        getter=getters.get_target_sources,
    )


def select_source_of_traffic():
    return Window(
        I18NFormat('T_select_source_of_traffic'),
        select_traffic_source(selected.on_select_traffic_source),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.select_traffic_source,
        getter=getters.get_select_traffic_source_data,

    )


def enter_offer_data_window():
    return Window(
        I18NFormat('T_enter_offer_data'),
        WebApp(I18NFormat("I_enter_offer_data"), Const(WebAppUrls.CREATE_OFFER_WEB_APP.value)),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.enter_offer_data,
    )


def confirm_offer_window():
    return Window(
        Multi(
            I18NFormat("T_confirm_entered_data"),
            Format("{offer_info}"),
            sep='\n\n'
        ),
        SwitchTo(I18NFormat('I_payment_confirm'), 'confirm',
                 state=states.CreateOffer.add_channel),
        WebApp(I18NFormat('I_edit'), Const(WebAppUrls.CREATE_OFFER_WEB_APP.value)),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.confirm_offer_data,
        getter=getters.get_entered_offer_data
    )


def add_channel_window():
    return Window(
        I18NFormat('T_add_channel'),
        Url(I18NFormat('I_add_channel'), Format("{add_channel_url}")),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.add_channel,
        getter=getters.get_add_channel_url
    )


def select_theme_of_tg_traffic_channel_window():
    return Window(
        I18NFormat('T_select_channel_theme'),
        channel_theme_kb(selected.on_select_topic_of_tg_traffic_channel),
        Cancel(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_theme,
        getter=get_channel_themes,
    )


def select_criteria_for_sort_window():
    return Window(
        I18NFormat('T_select_filter_criteria'),
        keyboards.criterias_kb(selected.on_select_criteria_for_sort),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_criteria_for_sort,
        getter=getters.get_criteria_for_sort,
    )


def select_channel_window():
    return Window(
        I18NFormat('T_u_open_all_channels'),
        Button(
            Case(
                {
                    'asc': I18NFormat('I_change_filter_from_max_to_min'),
                    'desc': I18NFormat('I_change_filter_from_min_to_max'),
                },
                selector='sort_criteria'
            ),
            id='change_sort_criteria',
            on_click=selected.on_change_sort_criteria
        ),
        get_channels_kb(selected.on_select_channel),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_channel,
        getter=getters.get_channels_with_criteria,
    )


def show_channel_info_window():
    return Window(
        I18NFormat('T_channel_info'),
        Button(I18NFormat('I_accept'), 'I_accept', on_click=selected.on_accept_channel),
        # SwitchTo(I18NFormat('I_back'), 'back_to_criteria', state=states.CreateOfferFromTGTraffic.select_criteria_for_sort),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.show_channel_info,
        getter=getters.get_channel_info,
    )


def enter_comment_for_owner_window():
    return Window(
        I18NFormat("T_enter_comment_for_request"),
        TextInput(id='enter_comment', on_success=selected.on_enter_comment),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.enter_comment
    )
