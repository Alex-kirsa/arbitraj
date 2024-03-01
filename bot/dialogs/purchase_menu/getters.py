import logging

from aiocryptopay import AioCryptoPay
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.services.cryptopay.requests import create_invoice
from bot.utils.admins import send_admins
from bot.utils.constants import PAYMENT_METHODS, CHANNEL_ADD_PRICE, CARD_NUBMER, WebAppUrls, OfferStatus, ChannelStatus, PaymentMethods


async def get_price(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
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
    elif payment_for == 'account_purchase':
        price = CHANNEL_ADD_PRICE
        description_for_invoice = i18n.get('T_description_for_channel_invoice')
    else:
        raise ValueError(f'Unknown payment type {payment_for}. user-id:{event_from_user.id} ')
    dialog_manager.dialog_data.update(price=price)
    crypto_invoice = await create_invoice(crypto_bot_client, price, description_for_invoice, event_from_user.id)

    return {
        'price': price,
        'payment_methods': [(key, value) for key, value in PAYMENT_METHODS.items()],
        'role': user_model.role,
        'pay_url': crypto_invoice.bot_invoice_url,
    }


async def get_payment_info(dialog_manager: DialogManager,  repo: Repo, event_from_user: User, **middleware_data):
    start_data = dialog_manager.start_data
    payment_for = start_data.get('payment_for')

    return {
        'price': dialog_manager.dialog_data['price'],
        'card_number': CARD_NUBMER,
        'payment_for': payment_for

    }


async def get_data_for_save(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):

    start_data = dialog_manager.start_data
    payment_for = start_data.get('payment_for')
    data = {
        'payment_for': payment_for
    }
    if dialog_manager.start_data['payment_for'] == 'offer_purchase':
        await repo.offer_repo.update_offer(dialog_manager.start_data['offer_id'], status=OfferStatus.WAIT_CONFIRM_PAYMENT,
                                           money_reserved=dialog_manager.dialog_data['reserved_amount'])
        offer_model = await repo.offer_repo.get_offers(offer_id=dialog_manager.start_data['offer_id'])
        await repo.channel_repo.update_channel_for_traffic_status(channel_id=offer_model.channel_id, status=ChannelStatus.WAIT_CONFIRM_PAYMENT)

    return data
