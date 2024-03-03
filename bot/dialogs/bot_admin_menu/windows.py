from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, SwitchTo, Button
from aiogram_dialog.widgets.text import Multi, Const, Format
from magic_filter import F

from . import keyboards, states, getters, selected
from ..channel_owner_menu.keyboards import channel_theme_kb, get_channels_kb
from ..web_master_menu.keyboards import select_offer


def main_admin_menu_window():
    return Window(
        Const("Админ панель"),
        keyboards.select_action_kb(),
        Cancel(Const("Назад")),
        state=states.MainAdminMenu.select_action,
        # getter=getters.select_action,
    )


def select_request_type_window():
    return Window(
        Multi(
            Const("Выберите тип заявки"),
            Format('{requests_data}'),
            sep='\n\n'
        ),
        keyboards.select_request_type_kb(selected.on_select_request_type),
        Cancel(Const("Назад")),
        state=states.Requests.select_request_type,
        getter=getters.get_request_types,
    )


def select_request_window():
    return Window(
        Const("Выберите заявку"),
        keyboards.requests_kb(selected.on_select_request),
        Back(Const("Назад")),
        state=states.Requests.select_request,
        getter=getters.get_requests

    )


def show_request_info_window():
    return Window(
        Format('{request_data}'),
        Button(
            Const("Принять"),
            id="accept_request",
            on_click=selected.on_accept_request,
        ),
        Button(
            Const("Отклонить"),
            id="reject_request",
            on_click=selected.on_reject_request
        ),
        Back(Const("Назад")),
        state=states.Requests.show_request,
        getter=getters.get_request_info
    )


def enter_second_price_per_request_window():
    return Window(
        Const("Введите новую цену за заявку"),
        TextInput(
            id="second_price_per_request",
            type_factory=int,
            on_success=selected.on_enter_second_price_per_request
        ),
        Back(Const("Назад")),
        state=states.Requests.enter_second_price_per_request,
    )


def withdraw_request_window():
    return Window(
        Const("Выберите заявку на выплату"),
        keyboards.withdraw_request_kb(selected.on_select_withdraw_request),
        Cancel(Const("Назад")),
        state=states.RequestsOnWithdrawal.select_requests,
        getter=getters.get_withdraw_requests
    )


def show_withdraw_request_info_window():
    return Window(
        Format('{withdraw_request_data}'),
        Button(
            Const("Выплатить"),
            id="accept_withdraw_request",
            on_click=selected.on_accept_withdraw_request
        ),
        Button(
            Const("Отклонить"),
            id="reject_withdraw_request",
            on_click=selected.on_reject_withdraw_request
        ),
        Back(Const("Назад")),
        state=states.RequestsOnWithdrawal.show_request_info,
        getter=getters.get_withdraw_request_info
    )


def users_window():
    return Window(
        Format("{users_data}"),
        keyboards.user_types(),
        Cancel(Const("Назад")),
        state=states.Users.select_user_role,
        getter=getters.get_users_data
    )


def channel_owners_channel_window():
    return Window(
        Format("{channels_data}"),
        keyboards.get_channels_status_kb(selected.on_select_channel_status),
        Cancel(Const("Назад")),
        state=states.ChannelOwnerInfo.select_channel_status,
        getter=getters.get_channels_data
    )


def select_channel_theme_window():
    return Window(
        Multi(
            Const("Выберите тематику"),
            Format('{channel_data}'),
            sep='\n\n'
        ),
        channel_theme_kb(selected.on_select_channel_theme),
        Back(Const("Назад")),
        state=states.ChannelOwnerInfo.select_theme,
        getter=getters.get_channels_and_subs
    )


def select_channel_window():
    return Window(
        Format("{channels_data}"),
        get_channels_kb(selected.on_select_channel),
        Back(Const("Назад")),
        state=states.ChannelOwnerInfo.selet_channel,
        getter=getters.get_channels
    )


def show_channel_info_window():
    return Window(
        Format("{channel_data}"),
        Back(Const("Назад")),
        state=states.ChannelOwnerInfo.show_channel_info,
        getter=getters.get_channel_info
    )


def channel_admins_info_window():
    return Window(
        Format("{offers_data}"),
        SwitchTo(Const("Офферы"), id="offers", state=states.ChannelAdminsInfo.select_offers_status),
        Cancel(Const("Назад")),
        state=states.ChannelAdminsInfo.select_offers,
        getter=getters.get_offers_data
    )


def select_offer_status_window():
    return Window(
        Multi(
            Const("Выберите статус оффера"),
            Format('{offers_status_data}'),
            sep='\n\n'
        ),
        keyboards.offers_statuses(selected.on_select_offer_status),
        Back(Const("Назад")),
        state=states.ChannelAdminsInfo.select_offers_status,
        getter=getters.get_offer_status
    )


def select_offer_window():
    return Window(
        Format("{offers_data}"),
        select_offer(selected.on_select_offer),
        Back(Const("Назад")),
        state=states.ChannelAdminsInfo.select_offer,
        getter=getters.get_offers_list_and_data
    )


def show_offer_info_window():
    return Window(
        Format("{offer_data}"),
        Back(Const("Назад")),
        state=states.ChannelAdminsInfo.show_offer,
        getter=getters.get_offer_info
    )


def show_general_webmaster_info_window():
    return Window(
        Format("{webmaster_info}"),
        SwitchTo(Const("Офферы"), id="offers", state=states.WebMasterInfo.select_offer_status),
        Cancel(Const("Назад")),
        state=states.WebMasterInfo.show_general_webmaster_info,
        getter=getters.get_webmaster_info
    )


def select_offer_status_webmaster_window():
    return Window(
        Multi(
            Const("Выберите статус оффера"),
            Format('{offers_status_data}'),
            sep='\n\n'
        ),
        keyboards.offers_statuses(selected.on_select_webmaster_offer_status),
        Back(Const("Назад")),
        state=states.WebMasterInfo.select_offer_status,
        getter=getters.get_offer_statuses_and_data
    )


def select_webmaster_offer_window():
    return Window(
        Format("{offers_data}"),
        select_offer(selected.on_select_offer_in_work),
        Back(Const("Назад")),
        state=states.WebMasterInfo.select_offer,
        getter=getters.get_offers_in_work
    )


def show_webmaster_offer_info_window():
    return Window(
        Format("{offer_data}"),
        Back(Const("Назад")),
        state=states.WebMasterInfo.show_offer,
        getter=getters.get_offer_in_work_info
    )


def statistic_window():
    return Window(
        Format("{statistic_data}"),
        Cancel(Const("Назад")),
        state=states.Statistic.show_statistic,
        getter=getters.get_statistic
    )


def add_link_window():
    return Window(
        Format("{sources_data}"),
        keyboards.add_link_kb(selected.on_select_source_for_link),
        Cancel(Const("Назад")),
        state=states.AddLink.select_source,
        getter=getters.get_links_amount
    )


def select_casino_name_window():
    return Window(
        Format("Выберите казино"),
        keyboards.select_casino_name_kb(selected.on_select_casino_name),
        Back(Const("Назад")),
        state=states.AddLink.select_casino_name,
        getter=getters.get_casinos
    )


def enter_casino_link_window():
    return Window(
        Multi(
            Const("Введите ссылку на казино.\n\n"
                  "Вы можете загружать ссылки до тех пор пока не нажмете Готово.\n"
                  "Вы можете загрузить ссылки одним сообщением. Ссылки должныть быть разделены пробелом"),
            Format(
                "Введенные ссылки:\n\n"
                "{entered_links}"
            ),
            sep='\n\n'
        ),
        TextInput(
            id="casino_link",
            on_success=selected.on_enter_casino_link
        ),
        Button(
            Const("Готово"),
            id="done",
            on_click=selected.on_done_entering_links,
            when=F['entered_links']
        ),
        Back(Const("Назад")),
        state=states.AddLink.enter_link,
        getter=getters.get_entered_links,
        disable_web_page_preview=True
    )


def search_user_window():
    return Window(
        Const("Введите имя пользователя"),
        TextInput(
            id="enter_username",
            on_success=selected.on_enter_username
        ),
        Cancel(Const("Назад")),
        state=states.SearchUser.enter_username,
    )


def select_user_window():
    return Window(
        Format("Выберите пользователя"),
        keyboards.select_user_kb(selected.on_select_user),
        Back(Const("Назад")),
        state=states.SearchUser.select_user,
        getter=getters.get_matched_users
    )


def show_user_info_window():
    return Window(
        Format("{user_data}"),
        Back(Const("Назад")),
        state=states.SearchUser.show_user,
        getter=getters.get_user_info
    )


def mailing_window():
    return Window(
        Const("Введите сообщение"),
        TextInput(
            id="message",
            on_success=selected.on_enter_mailing_message
        ),
        Cancel(Const("Назад")),
        state=states.Mailing.enter_message,
    )


def confirm_mailing_window():
    return Window(
        Format("Сообщение:\n\n{message}"),
        Button(
            Const("Отправить"),
            id="send_mailing",
            on_click=selected.on_send_mailing
        ),
        Back(Const("Назад")),
        state=states.Mailing.confirm_mailing,
        getter=getters.get_mailing_message
    )