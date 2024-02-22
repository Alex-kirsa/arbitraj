from aiogram.fsm.state import StatesGroup, State


class ChannelAdminMainMenu(StatesGroup):
    select_action = State()


class CreateOffer(StatesGroup):
    select_target_source = State()
    select_source = State()
    confirm = State()
    select_payment_method = State()
    confirm_purchase = State()


class CreateOfferFromTGTraffic(StatesGroup):
    select_topic = State()
    select_criteria_for_sort = State()
    select_channel = State()
    show_channel_info = State()


class ChannelAdminPersonalCabinet(StatesGroup):
    select_action = State()
    select_offer = State()
    show_offer_info = State()


class ChannelPosterAdminMenu(StatesGroup):
    select_topic = State()
    select_channel = State()
