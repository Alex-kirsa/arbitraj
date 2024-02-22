from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    select_action = State()


class SelectWebMasterOffer(StatesGroup):
    select_category = State()
    select_traffic_source = State()
    select_webmaster_offer = State()
    show_offer_info = State()


class PersonalCabinet(StatesGroup):
    show_personal_info = State()


class WithdrawFunds(StatesGroup):
    show_withdraw_menu = State()
