import logging

from aiocryptopay import AioCryptoPay
from aiogram import Dispatcher, Bot
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.services.cryptopay.requests import create_invoice
from bot.utils.constants import PAYMENT_METHODS, CHANNEL_ADD_PRICE, CARD_NUBMER, OfferStatus, ChannelStatus, DEFAULT_CHANNEL_TOPPICS
from configreader import config


async def get_price(dialog_manager: DialogManager, repo: Repo, event_from_user: User, dp: Dispatcher, bot: Bot, **middleware_data):
    start_data = dialog_manager.start_data
    i18n: I18nContext = middleware_data['i18n']
    crypto_bot_client: AioCryptoPay = dialog_manager.middleware_data['crypto_bot_client']
    if not start_data:
        logging.error(f'Start data is empty user-id:{event_from_user.id}')
        raise ValueError('Start data is empty')
    user_model = await repo.user_repo.get_user(event_from_user.id)
    payment_for = start_data.get('payment_for')
    if not payment_for:
        logging.error(f'Payment type is empty user-id:{event_from_user.id}')
        raise ValueError('Payment type is empty')
    if payment_for == 'offer_purchase':
        price = int(start_data['first_price_per_request']) * int(start_data['target_request_amount'])
        description_for_invoice = i18n.get('T_description_for_offer_invoice')
    elif payment_for == 'channel_purchase':
        price = CHANNEL_ADD_PRICE
        description_for_invoice = i18n.get('T_description_for_channel_invoice')
        fsm = dp.fsm.get_context(bot, event_from_user.id, event_from_user.id)
        await fsm.set_state('TopUpOperations')
        await fsm.update_data({
            'payment_for': 'channel_purchase',
            'channel_id': start_data['channel_id']
        })
    else:
        raise ValueError(f'Unknown payment type {payment_for}. user-id:{event_from_user.id} ')
    dialog_manager.dialog_data.update(price=price)
    crypto_invoice = await create_invoice(crypto_bot_client, price, description_for_invoice, event_from_user.id)

    return {
        'price': price,
        'payment_methods': [(key, value) for key, value in PAYMENT_METHODS.items()],
        'role': user_model.role,
        'pay_url': crypto_invoice.bot_invoice_url if crypto_invoice else False,
    }


async def get_payment_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    start_data = dialog_manager.start_data
    payment_for = start_data.get('payment_for')
    return {
        'price': dialog_manager.dialog_data['price'],
        'card_number': CARD_NUBMER,
        'payment_for': payment_for

    }


async def get_data_for_save(dialog_manager: DialogManager, repo: Repo, event_from_user: User, bot: Bot, **middleware_data):
    start_data = dialog_manager.start_data
    payment_for = start_data.get('payment_for')
    data = {
        'payment_for': payment_for
    }
    if dialog_manager.start_data['payment_for'] == 'offer_purchase':
        await repo.offer_repo.update_offer(dialog_manager.start_data['offer_id'], status=OfferStatus.WAIT_ADMIN_CONFIRM,
                                           money_reserved=dialog_manager.dialog_data['reserved_amount'])
        offer_model = await repo.offer_repo.get_offers(offer_id=dialog_manager.start_data['offer_id'])
        user_info = await bot.get_chat(event_from_user.id)
        text_for_channel = (f"<b>📢 Нова заявка</b>\n\n"
                            f"<b>Користувач:</b> {user_info.full_name} @{user_info.username}\n"
                            f"<b>Канал:</b> {offer_model.channel_name}\n"
                            f"<b>Тематика:</b> {DEFAULT_CHANNEL_TOPPICS.get(offer_model.channel_theme)}\n"
                            )
        if offer_model.custom_channel_theme:
            text_for_channel += f"<b>Кастомна тематика:</b> {offer_model.custom_channel_theme}\n"
        text_for_channel += (f"Необхідна кількість заявок: {offer_model.target_request_amount}\n"
                             f"Ціна за заявку: {offer_model.first_price_per_request} грн.\n"
                             f"Зарезервована сума: {offer_model.money_reserved}\n"
                             f"Дедлайн: {offer_model.offer_deadline}\n"
                             f"Вимоги до трафіку: {offer_model.traffic_rules}\n"
                             f"Коментар: {offer_model.comment}\n"
                             f"Контакт: {offer_model.contacts}\n")
        await bot.send_message(config.offers_channel_id, text_for_channel)
        await repo.channel_repo.update_channel_for_traffic_status(channel_id=offer_model.channel_id, status=ChannelStatus.WAIT_CONFIRM_PAYMENT)
    elif dialog_manager.start_data['payment_for'] == 'channel_purchase':
        channel_model = await repo.channel_repo.get_channel(dialog_manager.start_data['channel_id'])
        user_info = await bot.get_chat(event_from_user.id)
        text_for_channel = (f'<b>📢Нова заявка</b>\n\n'
                            f'<b>Користувач:</b> {user_info.full_name} @{user_info.username}\n'
                            f'<b>Канал:</b> {channel_model.channel_title}\n'
                            f'<b>Тематика:</b> {DEFAULT_CHANNEL_TOPPICS.get(channel_model.channel_theme)}\n')
        if channel_model.custom_channel_theme:
            text_for_channel += f"<b>Кастомна тематика:</b> {channel_model.custom_channel_theme}\n"
        text_for_channel += (f"Посилання на канал: {channel_model.channel_invite_link}\n"
                             f"Кількість підписників: {channel_model.subs_amount}\n"
                             f"Відсотко аудиторії: {channel_model.male_percent}/{channel_model.female_percent}\n"
                             f"Середній охват публікації: {channel_model.avg_reach_one_publication}\n"
                             f"Середній охват рекламної публікації: {channel_model.avg_reach_one_ad_publication}\n"
                             f"Мінімальна вартість реклами: {channel_model.minimal_ad_price}\n"
                             f"Коментарій: {channel_model.comment}\n"
                             f"Контакти: {channel_model.contacts}\n")
        await bot.send_message(config.channels_channel_id, text_for_channel)

        await repo.channel_repo.update_channel(id_=dialog_manager.start_data['channel_id'], status=ChannelStatus.WAIT_CONFIRM_PAYMENT)
    return data
