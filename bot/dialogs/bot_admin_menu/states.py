from aiogram.fsm.state import StatesGroup, State


class MainAdminMenu(StatesGroup):
    select_action = State()


class Users(StatesGroup):
    select_user_role = State()

#
# class Search