from aiogram_dialog import Dialog

from . import selected
from . import windows


def purchase_menu_dialogs():
    return [
        Dialog(
            windows.select_payment_method_window(),
            windows.confirm_payment_window(),
            windows.data_save_window()
            # on_start=selected.on_start_purchase
        )
    ]
