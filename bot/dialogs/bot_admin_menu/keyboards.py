import operator

from aiogram_dialog.widgets.kbd import Group, Start, Select, ScrollingGroup, Column, Button
from aiogram_dialog.widgets.text import Format, Const

from . import states, selected


def select_action_kb():
    return Group(
        Start(Const("Статистика"), id="statistic", state=states.Statistic.show_statistic),
        Start(Const("Пользователи"), id="users",  state=states.Users.select_user_role),
        Start(Const("Поиск"), id="search_user",  state=states.SearchUser.enter_username),
        Start(Const("Заявки"), id="requests",  state=states.Requests.select_request_type),
        Start(Const("Заявки на выплаты"), id="withdrawal_requests",  state=states.RequestsOnWithdrawal.select_requests),
        Start(Const("Сделать рассылку"), id="make_mailing",  state=states.Mailing.enter_message),
        Start(Const("Добавить ссылку"), id='add_link', state=states.AddLink.select_source),
        Button(Const("Обновить гугл таблицу"), id="update_google_table", on_click=selected.on_update_google_table),
        width=2
    )


def select_request_type_kb(on_click):
    return Column(
            Select(
                Format('{item[1]}'),
                id="withdrawal_requests",
                on_click=on_click,
                item_id_getter=operator.itemgetter(0),
                items='requests_types'
            )
        )


def requests_kb(on_clicl):
    return Column(
        Select(
            Format('{item[1]}'),
            id="withdrawal_requests",
            on_click=on_clicl,
            item_id_getter=operator.itemgetter(0),
            items='requests'
        )
    )


def withdraw_request_kb(on_click):
    return Column(
        Select(
            Format('{item[1]}'),
            id="withdrawal_requests",
            on_click=on_click,
            item_id_getter=operator.itemgetter(0),
            items='withdraw_requests'
        )
    )


def user_types():
    return Group(
        Select(
            Format('{item[1]}'),
            id="user_role",
            on_click=selected.on_select_user_role,
            item_id_getter=operator.itemgetter(0),
            items='user_types'
        ),
        width=2
    )


def get_channels_status_kb(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id="channel_status",
            on_click=on_click,
            item_id_getter=operator.itemgetter(0),
            items='channel_statuses'
        ),
        width=2
    )


def offers_statuses(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id="offer_status",
            on_click=on_click,
            item_id_getter=operator.itemgetter(0),
            items='offer_statuses'
        ),
        width=2
    )


def add_link_kb(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id="source",
            on_click=on_click,
            item_id_getter=operator.itemgetter(0),
            items='sources'
        ),
        width=2
    )


def select_casino_name_kb(on_clicks):
    return ScrollingGroup(
        Select(
            Format('{item[1]}'),
            id="casino_name",
            on_click=on_clicks,
            item_id_getter=operator.itemgetter(0),
            items='casinos_list'
        ),
        width=2,
        height=6,
        id='casinos_s_g',
        hide_on_single_page=True
    )


def select_user_kb(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[1]}'),
            id="user",
            on_click=on_click,
            item_id_getter=operator.itemgetter(0),
            items='users_list'
        ),
        width=1,
        height=6,
        id='users_s_g',
        hide_on_single_page=True
    )