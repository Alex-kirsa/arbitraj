from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_i18n import I18nContext

from . import states
from ..selected_main import not_working_traffic_source, not_working_zaliv
from ...db import Repo
from ...utils.constants import TrafficSource, RoleTypes, TargetSource


async def on_start_personal_cabinet(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(states.PersonalCabinet.show_personal_info)


async def on_start_select_offer(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(states.SelectWebMasterOffer.select_category)


async def on_select_target_source(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id in [TargetSource.ONLY_FANS.name, TargetSource.WEB_STORE.name]:
        return await not_working_zaliv(call, widget, dialog_manager)
    dialog_manager.dialog_data.update(selected_target_source=item_id)
    repo: Repo = dialog_manager.middleware_data['repo']
    user_model = await repo.user_repo.get_user(call.from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        await call.answer('Наразі вам доступний тільки ТікТок з джерела трафіку, так як це самий простий спосіб заливання трафіку.', show_alert=True)
    await dialog_manager.switch_to(states.SelectWebMasterOffer.select_traffic_source)


async def on_select_traffic_source(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id in [TrafficSource.REDDIT, TrafficSource.TWITTER]:
        return await not_working_traffic_source(call, widget, dialog_manager)
    dialog_manager.dialog_data.update(selected_traffic_source=item_id)
    repo: Repo = dialog_manager.middleware_data['repo']
    user_model = await repo.user_repo.get_user(call.from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        await call.answer('Ви попали в оффери для тіктоку. Виберіть один з них, щоб переглянути інформацію', show_alert=True)
    await dialog_manager.switch_to(states.SelectWebMasterOffer.select_webmaster_offer)


async def on_select_offer(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_offer_id=int(item_id))
    repo: Repo = dialog_manager.middleware_data['repo']
    user_model = await repo.user_repo.get_user(call.from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        await call.answer('Ви отримали детальну інформацію про оффер. Нажміть кнопку для отримання посилання для заливання', show_alert=True)
    await dialog_manager.switch_to(states.SelectWebMasterOffer.show_offer_info)


async def on_select_offer_my_offere(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_offer_id=int(item_id))
    repo: Repo = dialog_manager.middleware_data['repo']
    user_model = await repo.user_repo.get_user(call.from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        await call.answer('Ви отримали детальну інформацію про оффер. Нажміть кнопку для отримання посилання для заливання', show_alert=True)
    await dialog_manager.switch_to(states.MyOffers.show_my_offer_info)


async def on_take_offer(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    repo: Repo = dialog_manager.middleware_data['repo']
    i18n: I18nContext = dialog_manager.middleware_data['i18n']
    if dialog_manager.dialog_data.get('selected_target_source') == TargetSource.GAMBLING.name:
        already_took_offers = await repo.offer_repo.get_gambling_offer_links(user_id=call.from_user.id)
        if already_took_offers:
            return await call.answer(i18n.get('u_already_took_gambling_offer'), show_alert=True)
    await dialog_manager.switch_to(states.SelectWebMasterOffer.took_offer_action)


async def on_select_my_offer(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(states.MyOffers.select_target_source, data={'personal_offers': True})


async def on_select_withdraw_funds(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(states.WithdrawFunds.show_withdraw_menu)


async def on_select_target_source_in_my_offers(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id in [TargetSource.ONLY_FANS.name, TargetSource.WEB_STORE.name]:
        return await not_working_zaliv(call, widget, dialog_manager)
    dialog_manager.dialog_data.update(selected_target_source=item_id)
    await dialog_manager.switch_to(states.MyOffers.select_offer)
