from aiocryptopay import AioCryptoPay
from aiogram import Bot, Dispatcher
from aiogram_dialog import BgManagerFactory
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from bot.db import Repo
from bot.dialogs.channel_admin_menu.states import CreateOffer
from bot.dialogs.purchase_menu.states import TopUpOperations
from bot.dialogs.web_master_menu.states import WithdrawFunds
from bot.services.cryptopay.requests import check_signature
from bot.utils.constants import DEFAULT_CHANNEL_TOPPICS, PaymentMethods


async def handle_create_offer(request: Request):
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
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]
    dp: Dispatcher = request.app["dp"]
    crypto_bot_client: AioCryptoPay = request.app["crypto_bot_client"]
    data = await request.json()
    header = request.headers
    print(header)
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
    else:
        print(data)
    return json_response({"ok": True})


async def handle_withdraw_request(request: Request):
    bot: Bot = request.app["bot"]
    db_factory = request.app["db_factory"]
    bg_manager: BgManagerFactory = request.app["bg_manager"]
    dp: Dispatcher = request.app["dp"]

    data = await request.json()
    print(data)

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
        await repo.payment_repo.add_withdraw_request(user_id, amount, data['paymentType']['name'], bank_name, card_number, crypto_adress)
        bg = bg_manager.bg(bot, user_id, user_id)
        await bg.switch_to(WithdrawFunds.save_withdraw_data)
    # data = await request.post()  # application/x-www-form-urlencoded
    # logging.info(data)
    # try:
    #     data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    # except ValueError:
    #     return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    return json_response({"ok": True})


async def handle_purchase_confirmation(request: Request):
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
        await repo.payment_repo.add_topup_request(user_id, data['name'], int(data['lastDigits']), float(data['sum']), payment_type=PaymentMethods.ON_CARD)
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
