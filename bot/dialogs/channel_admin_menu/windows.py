from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Cancel, Back, SwitchTo, Start, Button
from aiogram_dialog.widgets.text import Multi, Const
from magic_filter import F

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import keyboards, states, getters, selected
from ..channel_owner_menu.getters import get_channel_topics, get_selected_topic
from ..channel_owner_menu.keyboards import channel_topics_kb, get_channels_kb, select_payment_method
from ..web_master_menu.getters import get_select_offer_data
from ..web_master_menu.keyboards import select_offer, select_category, select_traffic_source


def main_menu_window():
    return Window(
        I18NFormat('T_traffic_place'),
        keyboards.select_action(),
        Start(I18NFormat('I_back_to_selection'), id='back_to_first_menu',
              state=FirstStartWindow.select_your_role, mode=StartMode.RESET_STACK),
        state=states.ChannelAdminMainMenu.select_action,
    )


def personal_cabinet_window():
    return Window(
        I18NFormat('T_personal_cabinet_admin_channel'),
        SwitchTo(I18NFormat('I_active_orders'), 'I_active_orders',
                 state=states.ChannelAdminPersonalCabinet.select_offer),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelAdminPersonalCabinet.select_action,
    )


def select_active_order_window():
    return Window(
        I18NFormat('I_all_active_offers'),
        select_offer(selected.on_select_offer),
        Back(I18NFormat('I_back')),
        state=states.ChannelAdminPersonalCabinet.select_offer,
        getter=getters.get_active_orders,
    )


def show_offer_info_window():
    return Window(
        Multi(
            I18NFormat('T_offer_info', when=F['selected_category'].in_(['tg_channel_requests'])),
            I18NFormat('T_offer_info_gambling', when=F['selected_category'].in_(['gambling'])),
        ),
        Back(I18NFormat('I_back')),
        state=states.ChannelAdminPersonalCabinet.show_offer_info,
        getter=getters.get_offer_info,
    )


def select_topic_window():
    return Window(
        I18NFormat('T_select_channel_theme'),
        channel_topics_kb(selected.on_select_channel_topic),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelPosterAdminMenu.select_topic,
        getter=get_channel_topics,
    )


def show_channels_window():
    return Window(
        I18NFormat('T_u_open_all_channels'),
        get_channels_kb(),
        Back(I18NFormat('I_back')),
        state=states.ChannelPosterAdminMenu.select_channel,
        getter=get_selected_topic,
    )


def create_offer_window():
    return Window(
        I18NFormat('I_select_target_for_traffic'),
        select_category(selected.on_select_category),
        Cancel(I18NFormat('I_back')),
        state=states.CreateOffer.select_target_source,
        getter=get_select_offer_data,
    )


def select_source_of_traffic():
    return Window(
        I18NFormat('T_select_source_of_traffic'),
        select_traffic_source(selected.on_select_traffic_source),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.select_source,
        getter=getters.get_select_traffic_source_data,

    )


def confirm_offer_window():
    return Window(
        Const("*Повідомлення сформоване з форми. Потрібно нажати підтвердити*"),
        SwitchTo(I18NFormat('I_payment_confirm'), 'confirm',
                 state=states.CreateOffer.select_payment_method),
        Button(I18NFormat('I_edit'), 'I_edit'),
        Back(I18NFormat('I_back')),
        state=states.CreateOffer.confirm,
    )


def select_payment_method_window():
    return Window(
        I18NFormat('T_payment_request'),
        select_payment_method('channel_admin'),
        Cancel(I18NFormat('I_back')),
        state=states.CreateOffer.select_payment_method,
    )


def select_topic_of_tg_traffic_channel_window():
    return Window(
        I18NFormat('T_select_channel_theme'),
        channel_topics_kb(selected.on_select_topic_of_tg_traffic_channel),
        Cancel(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_topic,
        getter=get_channel_topics,
    )


def select_criteria_for_sort_window():
    return Window(
        I18NFormat('T_select_filter_criteria'),
        Button(I18NFormat('I_subscriber_count'), 'I_subscriber_count', on_click=selected.on_select_criteria_for_sort),
        Button(I18NFormat('I_publication_reach'), 'I_publication_reach'),
        Button(I18NFormat('I_min_post_price'), 'I_min_post_price'),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_criteria_for_sort,
    )


def select_channel_window():
    return Window(
        I18NFormat('T_u_open_all_channels'),
        get_channels_kb(selected.on_select_channel),
        Back(I18NFormat('I_back')),
        state=states.CreateOfferFromTGTraffic.select_channel,
        getter=get_selected_topic,
    )


def show_channel_info_window():
    return Window(
        I18NFormat('T_channel_info'),
        Button(I18NFormat('I_accept'), 'I_accept'),
        SwitchTo(I18NFormat('I_back'), 'back_to_criteria', state=states.CreateOfferFromTGTraffic.select_criteria_for_sort),
        state=states.CreateOfferFromTGTraffic.show_channel_info,
        getter=getters.get_channel_info,
    )
