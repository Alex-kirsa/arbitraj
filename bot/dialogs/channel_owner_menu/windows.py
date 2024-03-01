from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Cancel, Start

from bot.dialogs.start_menu.states import FirstStartWindow
from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import keyboards, states, getters, selected


def channel_owner_main_menu_window():
    return Window(
        I18NFormat('T_traffic_place'),
        keyboards.select_action(),
        Start(I18NFormat('I_back_to_selection'), id='back_to_first_menu',
              state=FirstStartWindow.select_your_role, mode=StartMode.RESET_STACK),
        state=states.ChannelOwnerMainMenu.select_action,
    )


def personal_cabinet_window():
    return Window(
        I18NFormat('T_personal_cabinet_balance'),
        keyboards.personal_cabinet_kb(),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelOwnerPersonalCabinet.select_action,
        getter=getters.get_personal_cabinet_data,
    )


def active_channels_window():
    return Window(
        I18NFormat('T_active_channels_intro'),
        keyboards.channels_kb(selected.on_select_channel),
        Cancel(I18NFormat('I_back')),
        state=states.UserChannels.select_channel,
        getter=getters.get_user_channels,
    )


def channel_info_window():
    return Window(
        I18NFormat('T_channel_info'),
        Cancel(I18NFormat('I_back')),
        state=states.UserChannels.channel_info,
        getter=getters.get_channel_info,
    )


def channel_poster_window():
    return Window(
        I18NFormat('T_select_channel_theme'),
        keyboards.channel_theme_kb(selected.on_select_channel_topic),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelPosterOwnerMenu.select_channel_topic,
        getter=getters.get_channel_themes,
    )


def show_channels_window():
    return Window(
        I18NFormat('T_u_open_all_channels'),
        keyboards.get_channels_kb(),
        Cancel(I18NFormat('I_back')),
        state=states.ChannelPosterOwnerMenu.show_channels,
        getter=getters.get_channels_in_theme,
    )
