from aiogram_dialog import Dialog

from . import windows


def channel_admin_menu_dialogs():
    return [
        Dialog(
            windows.main_menu_window(),
        ),
        Dialog(
            windows.personal_cabinet_window(),
        ),
        Dialog(
            windows.select_offer_window(),
            windows.show_offer_info_window(),
        ),
        Dialog(
            windows.select_topic_window(),
            windows.select_channels_window(),
        ),
        Dialog(
            windows.create_offer_window(),
            windows.select_source_of_traffic(),
            windows.enter_offer_data_window(),
            windows.confirm_offer_window(),
            windows.add_channel_window(),
        ),
        Dialog(
            windows.select_theme_of_tg_traffic_channel_window(),
            windows.select_criteria_for_sort_window(),
            windows.select_channel_window(),
            windows.show_channel_info_window(),
            windows.enter_comment_for_owner_window(),

        )
    ]
