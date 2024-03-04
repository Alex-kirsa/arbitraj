import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.types import Chat
from aiogram_i18n import I18nContext

from bot.db.models.models import Users, Offers
from bot.utils.constants import DEFAULT_CHANNEL_TOPICS
from configreader import config


async def notificate_web_masters_new_offer(webmasters: list[Users], bot: Bot, i18n: I18nContext, offer_model: Offers):
    user_info = await bot.get_chat(offer_model.user_id)
    for web_master in webmasters:
        offer_info = (f"<b>📢 До біржі доданий новий оффер:</b>\n\n"
                      # f"<b>Користувач:</b> {user_info.full_name} @{user_info.username}\n"
                      f"<b>Канал:</b> {offer_model.channel_name}\n"
                      f"<b>Тематика:</b> {DEFAULT_CHANNEL_TOPICS.get(offer_model.channel_theme)}\n"
                      )

        if offer_model.custom_channel_theme:
            offer_info += f"<b>Кастомна тематика:</b> {offer_model.custom_channel_theme}\n"

        offer_info += (f"Необходимое количество заявок: {offer_model.target_request_amount}\n"
                       f"Ціна за заявку: {offer_model.second_price_per_request} грн.\n"
                       # f"Зарезервована сумма: {offer_model.money_reserved}\n"
                       # f"Дедлайн: {offer_model.offer_deadline}\n"
                       f"Вимоги до трафіку: {offer_model.traffic_rules}\n")
        # f"Коментар: {offer_model.comment}\n"
        # f"Контакт: {offer_model.contacts}\n")

        try:
            await bot.send_message(web_master.user_id, i18n.get('new_offer_noty', offer_info=offer_info))
        except Exception as e:
            logging.info(f'Error while sending message to {web_master.user_id}: {e}')


async def notificate_web_master_offer_done(webmasters: list[Users], bot: Bot, i18n: I18nContext, offer_model: Offers):
    text = f'Оффер "{offer_model.channel_name}"  виконано". Перейдіть в Особисті кабінети та оберіть доступні оффери'
    for web_master in webmasters:
        with suppress(Exception):
            await bot.send_message(web_master.user_id, text)


async def send_admins_offer_completed(bot: Bot, i18n: I18nContext, offer_model: Offers):
    text = f'Оффер "{offer_model.channel_name}"  виконано'
    with suppress(Exception):
        await bot.send_message(config.offers_channel_id, text)


async def withdraw_request_notification(bot: Bot, user_info: Chat, amount: int, data: dict,
                                        bank_name: str = None, card_number: str = None,
                                        crypto_adress: str = None):
    text_for_channel = (f"<b>📢 Нова заявка</b>\n\n"
                        f"<b>Користувач:</b> {user_info.full_name} @{user_info.username}\n"
                        f"<b>Сума:</b> {amount}\n"
                        f"<b>Платіжна система:</b> {data['paymentType']['name']}\n")
    if bank_name:
        text_for_channel += f"<b>Банк:</b> {bank_name}\n<b>Номер картки:</b> {card_number}\n"
    if crypto_adress:
        text_for_channel += f"<b>Crypto Adress:</b> {crypto_adress}\n"
    await bot.send_message(config.withdraw_channel_id, text_for_channel)
