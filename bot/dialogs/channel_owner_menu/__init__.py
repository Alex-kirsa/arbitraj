from aiogram_dialog import Dialog

from . import windows


def channel_owner_menu_dialogs():
    return [
        Dialog(
            windows.channel_owner_main_menu_window(),
        ),
        Dialog(
            windows.personal_cabinet_window(),
        ),
        Dialog(
            windows.active_channels_window(),
            windows.channel_info_window(),
        ),
        Dialog(
            windows.channel_poster_window(),
            windows.show_channels_window(),
        ),
    ]
