from aiogram_dialog.widgets.kbd import Group, Start

from bot.utils.i18n_utils.i18n_format import I18NFormat
from . import states


def select_action():
    return Group(
        Start(I18NFormat("I_create_offer"), "I_create_offer",
              state=states.CreateOffer.select_target_source),
        Start(I18NFormat("I_channel_poster"), "I_channel_poster",
              state=states.ChannelPosterAdminMenu.select_topic),
        Start(I18NFormat("I_personal_cabinet"), "I_personal_cabinet",
              state=states.ChannelAdminPersonalCabinet.select_action),

    )
