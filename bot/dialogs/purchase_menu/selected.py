from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Data
from aiogram_dialog.widgets.kbd import Select

from . import states


async def on_select_payment_method(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(selected_payment_method=item_id)
    await dialog_manager.switch_to(states.TopUpOperations.confirm_payment)


async def on_start_purchase(result: dict, dialog_manager: DialogManager):
    print(dialog_manager.dialog_data)
    print(result)
