from aiogram_dialog import Dialog

from . import windows


def channel_admin_menu_dialogs():
    return [
        Dialog(
            windows.main_menu_window(),
        ),
        Dialog(
            windows.personal_cabinet_window(),
            windows.select_active_order_window(),
            windows.show_offer_info_window(),
        ),
        Dialog(
            windows.select_topic_window(),
            windows.show_channels_window()
        ),
        Dialog(
            windows.create_offer_window(),
            windows.select_source_of_traffic(),
            windows.confirm_offer_window(),
            windows.select_payment_method_window(),
        ),
        Dialog(
            windows.select_topic_of_tg_traffic_channel_window(),
            windows.select_criteria_for_sort_window(),
            windows.select_channel_window(),
            windows.show_channel_info_window()
        ),
    ]