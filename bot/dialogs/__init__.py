from aiogram import Router

from . import start_menu, web_master_menu, channel_owner_menu, channel_admin_menu, purchase_menu


def dialogs_includer(router: Router):
    router.include_routers(
        *start_menu.start_dialogs(),
        *channel_admin_menu.channel_admin_menu_dialogs(),
        *channel_owner_menu.channel_owner_menu_dialogs(),
        *purchase_menu.purchase_menu_dialogs(),
        *web_master_menu.web_master_menu_dialogs(),
    )
