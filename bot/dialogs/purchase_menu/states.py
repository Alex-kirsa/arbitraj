from aiogram.fsm.state import StatesGroup, State


class TopUpOperations(StatesGroup):
    select_pament_method = State()
    confirm_payment = State()
    data_saved = State()
