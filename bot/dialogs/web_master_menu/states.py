from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    select_action = State()


class SelectWebMasterOffer(StatesGroup):
    select_category = State()
    select_traffic_source = State()
    select_webmaster_offer = State()
    show_offer_info = State()
    took_offer_action = State()


class PersonalCabinet(StatesGroup):
    show_personal_info = State()


class WithdrawFunds(StatesGroup):
    show_withdraw_menu = State()
    save_withdraw_data = State()


class ReferalSystem(StatesGroup):
    show_referal_menu = State()


class MyOffers(StatesGroup):
    select_target_source = State()
    select_offer = State()
    show_my_offer_info = State()
