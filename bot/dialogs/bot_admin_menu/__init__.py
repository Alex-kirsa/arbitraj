from aiogram_dialog import Dialog

from . import windows


def bot_admin_menu_dialogs():
    return [
        Dialog(
            windows.main_admin_menu_window()
        ),
        Dialog(
            windows.select_request_type_window(),
            windows.select_request_window(),
            windows.show_request_info_window(),
            windows.enter_second_price_per_request_window()
        ),
        Dialog(
            windows.withdraw_request_window(),
            windows.show_withdraw_request_info_window(),
        ),
        Dialog(
            windows.users_window(),
        ),
        Dialog(
            windows.channel_owners_channel_window(),
            windows.select_channel_theme_window(),
            windows.select_channel_window(),
            windows.show_channel_info_window(),
        ),
        Dialog(
            windows.channel_admins_info_window(),
            windows.select_offer_status_window(),
            windows.select_offer_window(),
            windows.show_offer_info_window(),
        ),
        Dialog(
            windows.show_general_webmaster_info_window(),
            windows.select_offer_status_webmaster_window(),
            windows.select_webmaster_offer_window(),
            windows.show_webmaster_offer_info_window(),
        ),
        Dialog(
            windows.statistic_window(),
        ),
        Dialog(
            windows.add_link_window(),
            windows.select_casino_name_window(),
            windows.enter_casino_link_window()
        ),
        Dialog(
            windows.search_user_window(),
            windows.select_user_window(),
            windows.show_user_info_window(),
        ),
        Dialog(
            windows.mailing_window(),
            windows.confirm_mailing_window()
        )


    ]
