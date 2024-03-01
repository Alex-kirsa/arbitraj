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
            windows.select_new_offer_window(),
            windows.select_traffic_source_window(),
            windows.select_offer_window(),
            windows.show_offer_info_window(),
            windows.take_offer_window()
        ),
        Dialog(
            windows.withdraw_window(),
            windows.save_withdraw_data_window()
        ),
        Dialog(
            windows.referral_system_window(),
        ),
        Dialog(
            windows.my_offers_window(),
            windows.select_my_offer_window(),
            windows.show_my_offer_info_window(),
        ),
    ]

