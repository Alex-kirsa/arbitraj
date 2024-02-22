from aiogram_dialog import Dialog

from bot.dialogs.web_master_menu import windows


def web_master_menu_dialogs():
    return [
        Dialog(
            windows.main_menu(),
        ),
        Dialog(
            windows.personal_cabinet_window(),
        ),
        Dialog(
            windows.select_offer_window(),
            windows.select_traffic_source_window(),
            windows.select_offer(),
            windows.offer_info_window(),
        ),
        Dialog(
            windows.withdraw_window(),
        )
    ]

