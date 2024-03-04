from aiocryptopay import AioCryptoPay
from aiogram import Bot, Dispatcher
from aiogram_dialog import BgManagerFactory
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from bot.db import Repo
from bot.dialogs.channel_admin_menu.states import CreateOffer
from bot.dialogs.purchase_menu.states import TopUpOperations
from bot.dialogs.web_master_menu.states import WithdrawFunds
from bot.services.notification import withdraw_request_notification
from bot.utils.constants import DEFAULT_CHANNEL_TOPICS, PaymentMethods
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
    user_id = int(data['tg_user_id'])

    custom_channel_theme = None
    if data.get('channelThemeAdditional'):
        custom_channel_theme = data['channelThemeAdditional']
        channel_theme = 'other'
    else:
        channel_theme = 'news'
        for key, value in DEFAULT_CHANNEL_TOPICS.items():
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

    web_app_data = await request.json()

    user_id = int(web_app_data['tg_user_id'])

    if web_app_data['paymentType']['name'] == 'Банківська картка':
        bank_name = web_app_data['bankName']
        card_number = web_app_data['requisites']
        crypto_adress = None
        amount = int(web_app_data['sum'])
    elif web_app_data['paymentType']['name'] == 'Крипта':
        bank_name = None
        card_number = None
        crypto_adress = web_app_data['requisites']
        amount = int(web_app_data['sum'])
    else:
        raise ValueError(f"Unknown payment type {web_app_data['paymentType']['name']}")
    async with db_factory() as session:
        repo = Repo(session)
        user_model = await repo.user_repo.get_user(user_id)
        bg = bg_manager.bg(bot, user_id, user_id)
        if user_model.balance < amount:
            await bot.send_message(chat_id=user_id, text="<b>❗️ Недостатньо коштів на балансі.</b>")
            await bg.done()
            return json_response({"ok": True})
        user_info = await bot.get_chat(user_id)
        await withdraw_request_notification(bot, user_info, amount, web_app_data, bank_name, card_number, crypto_adress)
        await repo.payment_repo.add_withdraw_request(user_id, amount, web_app_data['paymentType']['name'], bank_name, card_number, crypto_adress)

        await bg.switch_to(WithdrawFunds.save_withdraw_data)
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
            for key, value in DEFAULT_CHANNEL_TOPICS.items():
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
    return json_response({"ok": True})
