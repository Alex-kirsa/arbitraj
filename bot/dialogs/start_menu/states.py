from aiogram.fsm.state import StatesGroup, State


class FirstStartWindow(StatesGroup):
    select_your_role = State()


class Cooperation(StatesGroup):
    send_cooperation_message = State()