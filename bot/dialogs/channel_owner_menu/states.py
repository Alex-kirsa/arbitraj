from aiogram.fsm.state import StatesGroup, State


class ChannelOwnerMainMenu(StatesGroup):
    select_action = State()


class AddChannel(StatesGroup):
    enter_webapp_form = State()
    select_payment_method = State()


class ChannelPosterOwnerMenu(StatesGroup):
    select_channel_topic = State()
    show_channels = State()


class PayViaCard(StatesGroup):
    show_payment_info = State()


class ChannelOwnerPersonalCabinet(StatesGroup):
    select_action = State()


class UserChannels(StatesGroup):
    select_channel = State()
    channel_info = State()
