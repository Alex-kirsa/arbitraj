from aiocryptopay import AioCryptoPay
from aiogram import Bot, Dispatcher
from aiogram_dialog import BgManagerFactory
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from bot.db import Repo
from bot.dialogs.channel_admin_menu.states import CreateOffer
from bot.dialogs.purchase_menu.states import TopUpOperations
from bot.dialogs.web_master_menu.states import WithdrawFunds
from bot.utils.constants import DEFAULT_CHANNEL_TOPPICS, PaymentMethods
from configreader import config


async def handle_create_offer(request: Request):
    """
    Handle create offer request from webapp
    :param request:
    :return:
    """
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]

    data = await request.json()
    # data = {'channelName': 'test', 'channelTheme': {'id': 9, 'name': 'Інше '}, 'channelThemeAdditional': '223', 'channelUrl': '1234', 'requiredApplications': '235',
    #         'deadline': 'до завтра', 'pricePerApplication': '3', 'trafficRequirements': 'тока укр', 'comment': 'тест', 'contactInfo': '@aboba', 'tg_user_id': '387375605'}
    user_id = int(data['tg_user_id'])

    custom_channel_theme = None
    if data.get('channelThemeAdditional'):
        custom_channel_theme = data['channelThemeAdditional']
        channel_theme = 'other'
    else:
        channel_theme = 'news'
        for key, value in DEFAULT_CHANNEL_TOPPICS.items():
            if value == data['channelTheme']['name']:
                channel_theme = key
                break

    dialog_data = {
        'channel_title': data['channelName'],
        'channel_theme': channel_theme,
        'custom_channel_theme': custom_channel_theme,
        'amount_requests': int(data['requiredApplications']),
        'deadline': data['deadline'],
        'price_per_request': int(data['pricePerApplication']),
        'traffic_rules': data['trafficRequirements'],
        'comment': data['comment'],
        'contact': data['contactInfo'],
    }
    user_info = await bot.get_chat(user_id)
    # text_for_channel = (f"<b>📢 Новий оффер</b>\n\n"
    #                     f"<b>Канал:</b> {dialog_data['channel_title']}\n"
    #                     f"<b>Тематика:</b> {data['channelTheme']['name']}\n"
    #                     f"<b>Кількість заявок:</b> {dialog_data['amount_requests']}\n"
    #                     f"<b>Термін:</b> {dialog_data['deadline']}\n"
    #                     f"<b>Ціна за заявку:</b> {dialog_data['price_per_request']}\n"
    #                     f"<b>Вимоги до трафіку:</b> {dialog_data['traffic_rules']}\n"
    #                     f"<b>Коментар:</b> {dialog_data['comment']}\n"
    #                     f"<b>Контактна інформація:</b> {dialog_data['contact']}\n"
    #                     )
    # await bot.send_message(config.offers_channel_id, text_for_channel)
    bg = bg_manager.bg(bot, user_id, user_id)
    await bg.update(dialog_data)
    await bg.switch_to(CreateOffer.confirm_offer_data)

    # data = await request.post()  # application/x-www-form-urlencoded
    # logging.info(data)
    # try:
    #     data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    # except ValueError:
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    return json_response({"ok": True})


async def handle_cryptopay_updates(request: Request):
    """
    Handle cryptopay updates
    :param request:
    :return:
    """
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]
    dp: Dispatcher = request.app["dp"]
    crypto_bot_client: AioCryptoPay = request.app["crypto_bot_client"]
    data = await request.json()
    header = request.headers
    # if not await check_signature(crypto_bot_client, data, header['Crypto-Pay-Api-Signature']):
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    if data['payload']['status'] == 'paid':
        async with db_factory() as session:
            repo = Repo(session)
            user_id = int(data['payload']['payload'])
            state = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=user_id)
            dialog_data = await state.get_data()
            dialog_data.update(payment_method=PaymentMethods.CRYPTOPAY, reserved_amount=int(data['payload']['amount']))
            await repo.payment_repo.add_topup_request(user_id, amount=int(data['payload']['amount']), payment_method=PaymentMethods.CRYPTOPAY)
            bg = bg_manager.bg(bot, user_id, user_id)
            await bg.update(dialog_data)
            await bg.switch_to(TopUpOperations.data_saved)
    return json_response({"ok": True})


async def handle_withdraw_request(request: Request):
    """
    Handle withdraw request from webapp
    :param request:
    :return:
    """
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]
    dp: Dispatcher = request.app["dp"]

    data = await request.json()

    user_id = int(data['tg_user_id'])

    if data['paymentType']['name'] == 'Банківська картка':
        bank_name = data['bankName']
        card_number = data['requisites']
        crypto_adress = None
        amount = int(data['sum'])
    elif data['paymentType']['name'] == 'Крипта':
        bank_name = None
        card_number = None
        crypto_adress = data['requisites']
        amount = int(data['sum'])
    else:
        raise ValueError(f"Unknown payment type {data['paymentType']['name']}")
    async with db_factory() as session:
        repo = Repo(session)
        user_model = await repo.user_repo.get_user(user_id)
        bg = bg_manager.bg(bot, user_id, user_id)
        if user_model.balance < amount:
            await bot.send_message(chat_id=user_id, text="<b>❗️ Недостатньо коштів на балансі.</b>")
            await bg.done()
            return json_response({"ok": True})
        user_info = await bot.get_chat(user_id)
        text_for_channel = (f"<b>📢 Нова заявка</b>\n\n"
                            f"<b>Користувач:</b> {user_info.full_name} @{user_info.username}\n"
                            f"<b>Сума:</b> {amount}\n"
                            f"<b>Платіжна система:</b> {data['paymentType']['name']}\n")
        if bank_name:
            text_for_channel += f"<b>Банк:</b> {bank_name}\n<b>Номер картки:</b> {card_number}\n"
        if crypto_adress:
            text_for_channel += f"<b>Crypto Adress:</b> {crypto_adress}\n"
        await bot.send_message(config.withdraw_channel_id, text_for_channel)
        await repo.payment_repo.add_withdraw_request(user_id, amount, data['paymentType']['name'], bank_name, card_number, crypto_adress)

        await bg.switch_to(WithdrawFunds.save_withdraw_data)
    # data = await request.post()  # application/x-www-form-urlencoded
    # logging.info(data)
    # try:
    #     data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    # except ValueError:
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    return json_response({"ok": True})


async def handle_purchase_confirmation(request: Request):
    """
    Handle purchase confirmation from webapp
    :param request:
    :return:
    """
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]
    dp: Dispatcher = request.app["dp"]
    data = await request.json()  # application/x-www-form-urlencoded
    async with db_factory() as session:
        repo = Repo(session)
        user_id = int(data['tg_user_id'])
        state = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=user_id)
        dialog_data = await state.get_data()
        dialog_data.update(payment_method=PaymentMethods.ON_CARD, reserved_amount=float(data['sum']))
        if dialog_data.get('payment_for') == 'offer_purchase':
            await repo.payment_repo.add_topup_request(user_id,
                                                      fullname=data['name'],
                                                      last_4_digits_credit_card=str(data['lastDigits']),
                                                      amount=float(data['sum']),
                                                      payment_method=PaymentMethods.ON_CARD,
                                                      offer_id=dialog_data['offer_id']
                                                      )
        else:
            await repo.payment_repo.add_topup_request(
                user_id,
                fullname=data['name'],
                last_4_digits_credit_card=str(data['lastDigits']),
                amount=float(data['sum']),
                payment_method=PaymentMethods.ON_CARD,
                channel_id=dialog_data['channel_id']
            )

        bg = bg_manager.bg(bot, user_id, user_id)
        await bg.update(dialog_data)
        await bg.switch_to(TopUpOperations.data_saved)

    # logging.info(data)
    # try:
    #     data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    # except ValueError:
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    return json_response({"ok": True})


async def handle_add_channel(request: Request):
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]

    # data: MultiDictProxy = await request.post()  # application/x-www-form-urlencoded
    data = await request.json()
    async with db_factory() as session:
        repo = Repo(session)

        custom_channel_theme = None
        if data.get('channelThemeAdditional'):
            custom_channel_theme = data['channelThemeAdditional']
            channel_theme = 'other'
        else:
            channel_theme = 'news'
            for key, value in DEFAULT_CHANNEL_TOPPICS.items():
                if value == data['channelTheme']['name']:
                    channel_theme = key
                    break

        user_id = int(data['tg_user_id'])
        data_for_db = {
            "channel_title": data['channelName'],
            'channel_owner_id': user_id,
            'channel_theme': channel_theme,
            'custom_channel_theme': custom_channel_theme,
            'channel_invite_link': data['channelUrl'],
            'subs_amount': int(data['subscriberCount']),
            'male_percent': int(data['maleAudiencePercentage']),
            'female_percent': int(data['femaleAudiencePercentage']),
            'avg_reach_one_publication': int(data['averageReachPerPost']),
            'avg_reach_one_ad_publication': int(data['averageReachOfAdPost']),
            'minimal_ad_price': int(data['minimumAdPrice']),
            'comment': data['comment'],
            'contact': data['contactInfo'],

        }
        await repo.channel_repo.add_channel(**data_for_db)

    await bot.send_message(chat_id=user_id, text="<b>✅Канал успішно додано.</b>\n\nОчікуйте підтвердження адміністратора бота.")
    await bg_manager.bg(bot, user_id, user_id).done()
    # try:
    #     data = check_webapp_signature(token=bot.token, init_data=data)
    # except ValueError:
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    return json_response({"ok": True})
