from aiogram.fsm.state import StatesGroup, State


class MainAdminMenu(StatesGroup):
    select_action = State()


class Users(StatesGroup):
    select_user_role = State()


class ChannelOwnerInfo(StatesGroup):
    select_channel_status = State()
    select_theme = State()
    selet_channel = State()
    show_channel_info = State()


class ChannelAdminsInfo(StatesGroup):
    select_offers = State()
    select_offers_status = State()
    select_offer = State()
    show_offer = State()


class WebMasterInfo(StatesGroup):
    show_general_webmaster_info = State()
    select_offer_status = State()
    select_offer = State()
    show_offer = State()


class SearchUser(StatesGroup):
    enter_username = State()
    select_user = State()
    show_user = State()


class RequestsOnWithdrawal(StatesGroup):
    select_requests = State()
    show_request_info = State()


class AddLink(StatesGroup):
    select_source = State()
    select_casino_name = State()
    enter_link = State()


class Statistic(StatesGroup):
    show_statistic = State()


class Requests(StatesGroup):
    select_request_type = State()
    select_request = State()
    show_request = State()
    enter_second_price_per_request = State()


class Mailing(StatesGroup):
    enter_message = State()
    confirm_mailing = State()