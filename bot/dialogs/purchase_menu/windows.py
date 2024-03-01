from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Cancel, Start, WebApp
from aiogram_dialog.widgets.text import Case, Const
from magic_filter import F

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states, getters, keyboards
from bot.dialogs.channel_admin_menu import states as channel_admin_states
from bot.dialogs.channel_owner_menu import states as channel_owner_states
from ...utils.constants import RoleTypes, WebAppUrls


def select_payment_method_window():
    return Window(
        Case(
            {
                RoleTypes.CHANNEL_ADMIN: I18NFormat('T_payment_request'),
                RoleTypes.CHANNEL_OWNER: I18NFormat('T_channel_placement_fee'),
            },
            selector='role'
        ),
        keyboards.select_payment_method(),
        Cancel(I18NFormat('I_back')),
        state=states.TopUpOperations.select_pament_method,
        getter=getters.get_price
    )


def confirm_payment_window():
    return Window(
        I18NFormat('T_payment_instruction'),
        WebApp(I18NFormat('I_paid'), Const(WebAppUrls.CONFIRM_PAYMENT_WEB_APP.value)),
        Start(I18NFormat('T_denie'), id='denie_payment',
              state=channel_admin_states.ChannelAdminMainMenu.select_action, mode=StartMode.RESET_STACK,
              when=F['payment_for'] == 'offer_purchase'),
        Start(I18NFormat('T_denie'), id='denie_payment',
              state=channel_owner_states.ChannelOwnerMainMenu.select_action, mode=StartMode.RESET_STACK,
              when=F['payment_for'] == 'account_purchase'),
        state=states.TopUpOperations.confirm_payment,
        getter=getters.get_payment_info
    )


def data_save_window():
    return Window(
        I18NFormat('T_data_saved'),
        Start(I18NFormat('main_menu'), id='denie_payment',
              state=channel_admin_states.ChannelAdminMainMenu.select_action, mode=StartMode.RESET_STACK,
              when=F['payment_for'] == 'offer_purchase'),
        Start(I18NFormat('main_menu'), id='denie_payment',
              state=channel_owner_states.ChannelOwnerMainMenu.select_action, mode=StartMode.RESET_STACK,
              when=F['payment_for'] == 'account_purchase'),
        state=states.TopUpOperations.data_saved,
        getter=getters.get_data_for_save
    )
