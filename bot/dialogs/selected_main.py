from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def not_working_category(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await call.answer("Ця категорія зараз не доступна")


async def not_working_zaliv(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await call.answer("Цей вид заливу зараз не доступний")


async def not_working_topic(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await call.answer("Ця тематика зараз не доступна")


async def not_working_criteria(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await call.answer("Цей критерій зараз не доступний")


async def not_working_traffic_source(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await call.answer("Цей джерело трафіку зараз не доступне")