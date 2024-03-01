from aiogram.fsm.state import StatesGroup, State


class ChannelAdminMainMenu(StatesGroup):
    select_action = State()


class CreateOffer(StatesGroup):
    select_target_source = State()
    select_traffic_source = State()
    enter_offer_data = State()
    confirm_offer_data = State()
    add_channel = State()


class CreateOfferFromTGTraffic(StatesGroup):
    select_topic = State()
    select_criteria_for_sort = State()
    select_channel = State()
    show_channel_info = State()
    enter_comment = State()


class ChannelAdminPersonalCabinet(StatesGroup):
    select_offer_status = State()


class AdminOffers(StatesGroup):
    select_offer = State()
    show_offer_info = State()


class ChannelPosterAdminMenu(StatesGroup):
    select_topic = State()
    select_channel = State()
