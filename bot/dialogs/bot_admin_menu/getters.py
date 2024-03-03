from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.db import Repo
from bot.dialogs.channel_owner_menu.getters import get_channel_themes
from bot.utils.constants import OfferStatus, ChannelStatus, traffic_sources_dict, WithdrawStatus, PaymentMethods, RoleTypes, TopUpStatus, channels_status_named, \
    offers_status_named, TargetSource, casinos_dict


async def get_request_types(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    wait_offers = await repo.offer_repo.get_offers(status=OfferStatus.WAIT_ADMIN_CONFIRM)
    wait_offers = len(wait_offers) if wait_offers else 0
    canceled_offers = await repo.offer_repo.get_offers(status=OfferStatus.CANCELED)
    canceled_offers = len(canceled_offers) if canceled_offers else 0
    channels_wait = await repo.channel_repo.get_channels(status=ChannelStatus.WAIT_ADMIN_CONFIRM)
    channels_wait = len(channels_wait) if channels_wait else 0
    canceled_channels = await repo.channel_repo.get_channels(status=ChannelStatus.CANCELED)
    canceled_channels = len(canceled_channels) if canceled_channels else 0
    text = (f"Кол-во заявок: {wait_offers + channels_wait + canceled_offers + canceled_channels}шт\n"
            f"Отклоненные заявки: {canceled_offers + canceled_channels}шт\n"
            f"Активны: {wait_offers + channels_wait}шт\n")
    return {
        'requests_types': [
            ('offers', 'Офферы'),
            ('channels', 'Каналы'),
        ],
        "requests_data": text
    }


async def get_requests(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    request_type = dialog_manager.dialog_data.get('request_type')
    if request_type == "offers":
        offers = await repo.offer_repo.get_offers(status=OfferStatus.WAIT_ADMIN_CONFIRM)
        offers_list = [
            (offer.id, offer.channel_name)
            for offer in offers
        ]
    elif request_type == "channels":
        channels = await repo.channel_repo.get_channels(status=[ChannelStatus.WAIT_ADMIN_CONFIRM, ChannelStatus.WAIT_CONFIRM_PAYMENT])
        offers_list = [
            (channel.id, channel.channel_title)
            for channel in channels
        ]
    else:
        raise ValueError("Unknown request type")
    return {
        'requests': offers_list
    }


async def get_request_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    request_id = dialog_manager.dialog_data.get('request_id')
    request_type = dialog_manager.dialog_data.get('request_type')
    data = {
        'request_type': request_type,

    }
    if request_type == "offers":
        offer = await repo.offer_repo.get_offers(offer_id=request_id)
        text = (f"ID: {offer.id}\n"
                f"Название канала: {offer.channel_name}\n"
                f"Тематика канала: {offer.channel_theme}\n"
                f"Количество заявок: {offer.target_request_amount}\n"
                f"Цена за заявку: {offer.first_price_per_request}\n"
                F"Зарезервированная сумма: {offer.money_reserved}\n"
                F"Дедлайн оффера: {offer.offer_deadline}\n"
                F"Условие трафика: {offer.traffic_rules}\n"
                f"Источник трафика: {traffic_sources_dict.get(offer.traffic_source)}\n"
                f"Тип трафика: {offer.target_source}\n"
                f"Комментарий: {offer.comment}\n"
                f"Контакт: {offer.contacts}\n"
                )
        payment_model = await repo.payment_repo.get_topup_request(offer_id=request_id)
        if payment_model:
            payment_method = payment_model[0].payment_method
            text += f"Оплачено: {payment_model[0].amount}\n"
            if payment_method == PaymentMethods.CRYPTOPAY:
                text += f"Тип оплаты: CryptoPay\n"
            else:
                text += (f"Последние 4 цифры карты: {payment_model[0].last_4_digits_credit_card}\n"
                         f"ФИО: {payment_model[0].fullname}\n")
    elif request_type == "channels":
        channel = await repo.channel_repo.get_channel(request_id)
        text = (f"ID: {channel.id}\n"
                f"Название канала: {channel.channel_title}\n"
                f"Тематика канала: {channel.channel_theme}\n"
                f"Ссылка на канал: {channel.channel_invite_link}\n"
                f"Количество подписчиков: {channel.subs_amount}\n"
                f"Процент мужчин: {channel.male_percent}\n"
                f"Процент женщин: {channel.female_percent}\n"
                f"Средний охват одной публикации: {channel.avg_reach_one_publication}\n"
                f"Средний охват одной рекламной публикации: {channel.avg_reach_one_ad_publication}\n"
                f"Минимальная цена рекламы: {channel.minimal_ad_price}\n"
                f"Комментарий: {channel.comment}\n"
                f"Контакт: {channel.contact}\n")
    else:
        raise ValueError("Unknown request type")
    data['request_data'] = text
    return data


async def get_withdraw_requests(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    withdraw_requests = await repo.payment_repo.get_withdraw_requests(status=WithdrawStatus.ACTIVE)
    withdraw_requests_list = [
        (withdraw.id, f"№{withdraw.id} - {withdraw.amount} грн")
        for withdraw in withdraw_requests
    ]
    return {
        'withdraw_requests': withdraw_requests_list
    }


async def get_withdraw_request_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    withdraw_request_id = dialog_manager.dialog_data.get('withdraw_request_id')
    withdraw_request_model = await repo.payment_repo.get_withdraw_requests(id_=withdraw_request_id)
    # withdraw_request_in_user = await repo.payment_repo.get_withdraw_request_with_status(user_id=withdraw_request_model.user_id, )
    completed_withdraw_in_user = await repo.payment_repo.get_withdraw_request_with_status(user_id=withdraw_request_model.user_id, status=WithdrawStatus.COMPLETED)
    canceled_withdraw_in_user = await repo.payment_repo.get_withdraw_request_with_status(user_id=withdraw_request_model.user_id, status=WithdrawStatus.CANCELED)
    active_withdraw_in_user = await repo.payment_repo.get_withdraw_request_with_status(user_id=withdraw_request_model.user_id, status=WithdrawStatus.ACTIVE)
    user_model = await repo.user_repo.get_user(withdraw_request_model.user_id)
    text = (f"ID выплаты: {withdraw_request_model.id}\n"
            f"ID пользователя: {withdraw_request_model.user_id}\n"
            f'Дата регистрации: {user_model.registration_date}\n'
            f'Username: {user_model.username}\n'
            f'<b>Баланс: {user_model.balance} грн\n'
            f"Сумма заявки: {withdraw_request_model.amount} грн</b>\n"
            f"Оплачено: {sum([withdraw.amount for withdraw in completed_withdraw_in_user]) if completed_withdraw_in_user else 0} грн\n"
            f"На рассмотрении: {sum([withdraw.amount for withdraw in active_withdraw_in_user])} грн\n"
            # f"Всего заявок: {len(withdraw_request_in_user)}\n"
            f"Кол-во заявок: {len(active_withdraw_in_user)}\n")
    text += f"Реквезиты: {withdraw_request_model.card_number if withdraw_request_model.card_number else withdraw_request_model.crypto_adress}\n"

    return {
        'withdraw_request_data': text
    }


async def get_users_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    users = await repo.user_repo.get_users()
    web_master_users = await repo.user_repo.get_users(user_role=RoleTypes.WEB_MASTER)
    new_bies = await repo.user_repo.get_users(user_role=RoleTypes.NEWBIE)
    channel_owners = await repo.user_repo.get_users(user_role=RoleTypes.CHANNEL_OWNER)
    channel_admins = await repo.user_repo.get_users(user_role=RoleTypes.CHANNEL_ADMIN)

    text = (f"Всего пользователей: {len(users)}\n"
            f"Вебмастеров: {len(web_master_users)}\n"
            f"Админов: {len(channel_admins)}\n"
            f"Новичков: {len(new_bies)}\n"
            f"Владельцев каналов: {len(channel_owners)}\n"
            )

    return {
        'users_data': text,
        'user_types': [
            (RoleTypes.WEB_MASTER, 'Вебмастеры'),
            (RoleTypes.CHANNEL_ADMIN, 'Админы'),
            (RoleTypes.NEWBIE, 'Новички'),
            (RoleTypes.CHANNEL_OWNER, 'Владельцы каналов'),
        ]
    }


async def get_channels_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    channels = await repo.channel_repo.get_channels()
    active_channels = await repo.channel_repo.get_channels(status=ChannelStatus.ACTIVE)
    channel_purchase = await repo.payment_repo.get_topup_request(status=[TopUpStatus.COMPLETED_BY_CRYPTOBOT, TopUpStatus.COMPLETED], channel_id='not null')
    text = (f"Всего каналов: {len(channels) if channels else 0}\n"
            f"Подписки: {len(active_channels) if active_channels else 0}\n"
            f"Оплачено: {sum([purchase.amount for purchase in channel_purchase])} грн\n")

    return {
        'channels_data': text,
        'channel_statuses': [
            ('all', 'Все каналы'),
            (ChannelStatus.ACTIVE, 'Активные'),
            (ChannelStatus.WAIT_ADMIN_CONFIRM, 'На рассмотрении'),
            (ChannelStatus.CANCELED, 'Отклоненные'),
        ]
    }


async def get_channels_and_subs(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    data = await get_channel_themes(dialog_manager)
    selected_channel_status = dialog_manager.dialog_data.get('channel_status')
    if selected_channel_status == 'all':
        channels_in_status = await repo.channel_repo.get_channels()
    else:
        channels_in_status = await repo.channel_repo.get_channels(status=selected_channel_status)
    channel_purchase = await repo.payment_repo.get_topup_request(status=[TopUpStatus.COMPLETED_BY_CRYPTOBOT, TopUpStatus.COMPLETED], channel_id='not null')

    text = (f"Всего каналов: {len(channels_in_status) if channels_in_status else 0}\n"
            f"Оплачено: {sum([purchase.amount for purchase in channel_purchase])} грн\n"
            f"Оплачено: {len(channel_purchase) if channel_purchase else 0} шт")

    data.update(
        {
            'channel_data': text
        }
    )
    return data


async def get_channels(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_channel_status = dialog_manager.dialog_data.get('channel_status')
    selected_channel_theme = dialog_manager.dialog_data.get('selected_channel_theme')
    if selected_channel_status == 'all':
        channels = await repo.channel_repo.get_channels(channel_theme=selected_channel_theme)
    else:
        channels = await repo.channel_repo.get_channels(channel_theme=selected_channel_theme, status=selected_channel_status)
    not_active_channels = await repo.channel_repo.get_channels(channel_theme=selected_channel_theme, status=ChannelStatus.CANCELED)
    channels_list = [
        (channel.id, f"{channel.channel_title}-{channel.subs_amount}")
        for channel in channels
    ]
    text = (f"Кол-во каналов: {len(channels) if channels else 0} шт\n"
            f"Не активные: {len(not_active_channels)} шт")
    return {
        'channels_list': channels_list,
        'channels_data': text
    }


async def get_channel_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    channel_model = await repo.channel_repo.get_channel(dialog_manager.dialog_data['selected_channel_id'])
    channel_owner_model = await repo.user_repo.get_user(channel_model.channel_owner_id)
    channel_data = f"Юзернейм: @{channel_owner_model.username}\n" \
                   f"Подписка: {channels_status_named.get(channel_model.status)}\n" \
                   f"Кол-во пдп: {channel_model.subs_amount}\n" \
                   f"Охват: {channel_model.avg_reach_one_publication}\n" \
                   f"Рекламный охват: {channel_model.avg_reach_one_ad_publication}\n" \
                   f"ЦА: {channel_model.male_percent}/{channel_model.female_percent}\n" \
                   f"Мин цена поста: {channel_model.minimal_ad_price}\n"
    return {
        'channel_data': channel_data
    }


async def get_offers_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    offers = await repo.offer_repo.get_offers()
    offer_purchase = await repo.payment_repo.get_topup_request(status=[TopUpStatus.COMPLETED_BY_CRYPTOBOT, TopUpStatus.COMPLETED], offer_id='not null')

    text = (f"Всего офферов: {len(offers) if offers else 0}\n"
            f"Сумма: {sum([offer.money_reserved for offer in offers])} грн\n")

    return {
        'offers_data': text,
    }


async def get_offer_status(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    active_offers = await repo.offer_repo.get_offers(status=OfferStatus.ACTIVE)
    in_work = await repo.offer_repo.get_offers(status=OfferStatus.IN_WORK)
    completed_offers = await repo.offer_repo.get_offers(status=OfferStatus.COMPLETED)
    canceled_offers = await repo.offer_repo.get_offers(status=OfferStatus.CANCELED)
    offers_status_list = [
        (OfferStatus.COMPLETED, 'Завершенные'),
        (OfferStatus.CANCELED, 'Отклоненные'),
        (OfferStatus.ACTIVE, 'Активные'),
    ]
    text = (f"Активные: {len(active_offers)}\n"
            f"В работе: {len(in_work)}\n"
            f"Завершенные: {len(completed_offers)}\n"
            f"Отклоненные: {len(canceled_offers)}\n")

    return {
        'offer_statuses': offers_status_list,
        'offers_status_data': text
    }


async def get_offers_list_and_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_offer_status = dialog_manager.dialog_data.get('selected_offer_status')
    offers = await repo.offer_repo.get_offers(status=selected_offer_status)
    offers_in_work = await repo.offer_repo.get_offer_in_work()
    text = f"Налито заявок: {sum([offer_in_work.current_reqeusts_amount for offer_in_work in offers_in_work])}"
    offers_list = [
        (offer.id, f"{offer.channel_name}-{offer.target_request_amount}")
        for offer in offers
    ]
    return {
        'offers_list': offers_list,
        'offers_data': text

    }


async def get_offer_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    offer_model = await repo.offer_repo.get_offers(dialog_manager.dialog_data['selected_offer_id'])
    user_model = await repo.user_repo.get_user(offer_model.user_id)
    offer_in_work = await repo.offer_repo.get_offer_in_work(offer_id=offer_model.id)
    offer_data = (f"Юзернейм: @{user_model.username}\n"
                  f"Налито заявок: {sum([took_offer.current_reqeusts_amount for took_offer in offer_in_work])}\n"
                  f"Пополнено: {offer_model.money_reserved}грн \n")
    return {
        'offer_data': offer_data
    }


async def get_webmaster_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    webmaster_users = await repo.user_repo.get_users(user_role=RoleTypes.WEB_MASTER)
    webmaster_users = webmaster_users if webmaster_users else []
    newbie_users = await repo.user_repo.get_users(user_role=RoleTypes.NEWBIE)
    newbie_users = newbie_users if newbie_users else []
    all_users = len(webmaster_users) + len(newbie_users)
    all_offers_in_work = await repo.offer_repo.get_offer_in_work()
    earned_money = sum([offer.earned_money for offer in all_offers_in_work])
    withdraws_model = await repo.payment_repo.get_withdraw_requests(status=WithdrawStatus.COMPLETED)
    withdraws_sum = sum([withdraw.amount for withdraw in withdraws_model])
    text = (f"Всего чел: {all_users}\n"
            f"Всего вебмастеров: {len(webmaster_users)}\n"
            f"Всего новичков: {len(newbie_users)}\n"
            f"Заработано: {earned_money}грн\n"
            f"Выплачено: {withdraws_sum}грн\n")
    return {
        'webmaster_info': text
    }


async def get_offer_statuses_and_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    active_offers = await repo.offer_repo.get_offer_in_work(status=OfferStatus.IN_WORK)
    active_offers = active_offers if active_offers else []
    completed_offers = await repo.offer_repo.get_offer_in_work(status=OfferStatus.COMPLETED)
    completed_offers = completed_offers if completed_offers else []
    text = (f"Активные: {len(active_offers)}\n"
            f"Выполненые: {len(completed_offers)}\n")

    return {
        'offers_status_data': text,
        'offer_statuses': [
            (OfferStatus.IN_WORK, 'В работе'),
            (OfferStatus.COMPLETED, 'Выполненые'),
        ]
    }


async def get_offers_in_work(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_offer_status = dialog_manager.dialog_data.get('selected_offer_status')
    offers_in_work = await repo.offer_repo.get_offer_in_work(status=selected_offer_status)
    offers_list = []
    for offer_in_work in offers_in_work:
        offer_model = await repo.offer_repo.get_offers(offer_id=offer_in_work.offer_id)
        offers_list.append((offer_in_work.id, f"{offer_model.channel_name}-{offer_in_work.current_reqeusts_amount}"))

    text = f'Категория: {offers_status_named.get(selected_offer_status)}\n'
    return {
        'offers_data': text,
        'offers_list': offers_list
    }


async def get_offer_in_work_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    offer_in_work_model = await repo.offer_repo.get_offer_in_work(id_=dialog_manager.dialog_data['selected_offer_id'])
    offer_model = await repo.offer_repo.get_offers(offer_id=offer_in_work_model.offer_id)
    selected_offer_status = dialog_manager.dialog_data.get('selected_offer_status')

    offer_data = (f"Категория: {offers_status_named.get(selected_offer_status)}\n"
                  f"Налито заявок: {offer_in_work_model.current_reqeusts_amount} шт.\n"
                  f"Источник трафика: {traffic_sources_dict.get(offer_model.traffic_source)}\n")
    return {
        'offer_data': offer_data
    }


async def get_statistic(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    all_users = await repo.user_repo.get_users()
    all_users = all_users if all_users else []
    web_masters = [user for user in all_users if user.role == RoleTypes.WEB_MASTER]
    channel_owners = [user for user in all_users if user.role == RoleTypes.CHANNEL_OWNER]
    channel_admins = [user for user in all_users if user.role == RoleTypes.CHANNEL_ADMIN]
    newbies = [user for user in all_users if user.role == RoleTypes.NEWBIE]
    channels = await repo.channel_repo.get_channels()
    channels = channels if channels else []
    channel_for_traffic = await repo.channel_repo.get_channels_for_traffic()
    channel_for_traffic = channel_for_traffic if channel_for_traffic else []
    top_up_offer_purchase = await repo.payment_repo.get_topup_request(offer_id='not null')
    top_up_offer_purchase = top_up_offer_purchase if top_up_offer_purchase else []
    top_up_offer_purchase_sum = sum([purchase.amount for purchase in top_up_offer_purchase])
    top_up_channel_purcase = await repo.payment_repo.get_topup_request(channel_id='not null')
    top_up_channel_purcase = top_up_channel_purcase if top_up_channel_purcase else []
    top_up_channel_purcase_sum = sum([purchase.amount for purchase in top_up_channel_purcase])
    all_offers_in_work = await repo.offer_repo.get_offer_in_work()
    all_offers_in_work = all_offers_in_work if all_offers_in_work else []
    all_channel_requests = sum([offer.current_reqeusts_amount for offer in all_offers_in_work])
    purchase_completed = await repo.payment_repo.get_topup_request(status=[TopUpStatus.COMPLETED_BY_CRYPTOBOT, TopUpStatus.COMPLETED])
    purchase_completed = purchase_completed if purchase_completed else []
    purchase_completed_sum = sum([purchase.amount for purchase in purchase_completed])
    purchase_canceled = await repo.payment_repo.get_topup_request(status=TopUpStatus.CANCELED)
    purchase_canceled = purchase_canceled if purchase_canceled else []
    purchase_canceled = sum([purchase.amount for purchase in purchase_canceled])

    text = (f"Всего пользователей: {len(all_users)}\n"
            f"Вебмастеров: {len(web_masters)}\n"
            f"Владельцев каналов: {len(channel_owners)}\n"
            f"Админов: {len(channel_admins)}\n"
            f"Новичков: {len(newbies)}\n"
            f"Каналов: {len(channels)}\n"
            f"Каналов по подписке: {len(channel_for_traffic)}\n\n"
            f"<b>Финансы</b>\n\n"
            f"Пополнения: {len(top_up_offer_purchase)} шт.\n"
            f"Пополнено: {top_up_offer_purchase_sum} грн\n"
            f"Подписки: {len(top_up_channel_purcase)} шт.\n"
            f"Подписки: {top_up_channel_purcase_sum} грн\n"
            f"Налито подписчиков: {all_channel_requests} шт.\n"
            f"Заработано: {purchase_completed_sum} грн\n"
            f"Отменено: {purchase_canceled} грн\n")

    return {
        'statistic_data': text
    }


async def get_links_amount(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    gambling_link = await repo.offer_repo.get_gambling_offer_links()
    free_links = [link for link in gambling_link if link.user_id is None]
    text = (f"Гемблинг: {len(free_links)}\n"
            f"ОнлиФанс: 0\n"
            f"Интернет-магазин: 0\n")
    sources_list = [
        (TargetSource.GAMBLING.name, 'Гемблинг'),
        (TargetSource.ONLY_FANS.name, 'ОнлиФанс'),
        (TargetSource.WEB_STORE.name, 'Интернет-магазин'),
    ]
    return {
        'sources': sources_list,
        'sources_data': text
    }


async def get_casinos(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_source = dialog_manager.dialog_data.get('selected_source')
    return {
        'casinos_list': [
            (casino_key, casino_name,)
            for casino_key, casino_name in casinos_dict.items()
        ]
    }


async def get_entered_links(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    entered_links = dialog_manager.dialog_data.get('links')
    entered_links_text = ''
    if entered_links:
        for index, link in enumerate(entered_links):
            entered_links_text += f"<a href='{link}'>Ссылка №{index + 1}</a>\n"
    return {
        'entered_links': entered_links_text
    }


async def get_matched_users(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    return {
        'users_list': [
            (user.user_id, f"{user.fullname}|{user.username}")
            for user in await repo.user_repo.get_user_link(dialog_manager.dialog_data['username'])
        ]
    }


async def get_user_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_id = dialog_manager.dialog_data.get('selected_user_id')
    user_model = await repo.user_repo.get_user(user_id)
    success_purchase = await repo.payment_repo.get_topup_request(user_id=user_id, status=TopUpStatus.COMPLETED)
    success_purchase = success_purchase if success_purchase else []
    sum_success_purchase = sum([purchase.amount for purchase in success_purchase])
    channel_purchase = await repo.payment_repo.get_topup_request(user_id=user_id, status=TopUpStatus.COMPLETED, channel_id='not null')
    channel_purchase = channel_purchase if channel_purchase else []
    sum_channel_purchase = sum([purchase.amount for purchase in channel_purchase])
    canceled_purchase = await repo.payment_repo.get_topup_request(user_id=user_id, status=TopUpStatus.CANCELED)
    all_channels_in_user = await repo.channel_repo.get_channels()
    all_channels_in_user = all_channels_in_user if all_channels_in_user else []
    user_offers = await repo.offer_repo.get_offers(user_id=user_id)
    user_offers = user_offers if user_offers else []
    succ_offer_purchase = await repo.payment_repo.get_topup_request(user_id=user_id, status=TopUpStatus.COMPLETED, offer_id='not null')
    succ_offer_purchase = succ_offer_purchase if succ_offer_purchase else []
    canceled_offer_purchase = await repo.payment_repo.get_topup_request(user_id=user_id, status=TopUpStatus.CANCELED, offer_id='not null')
    canceled_offer_purchase = canceled_offer_purchase if canceled_offer_purchase else []
    user_info_text = (
        f"<b>🛒 Количество оплат:</b> {len(success_purchase)}\n"
        f"<b>💵 Сумма оплат:</b> {sum_success_purchase} грн\n"
        f"<b>💰 Баланс:</b> {user_model.balance} грн\n\n"
        f"<b>📺 Количество каналов:</b> {len(all_channels_in_user)}\n"
        f"<b>🟢 Активные подписки:</b> {len([channel for channel in all_channels_in_user if channel.status == ChannelStatus.ACTIVE])}\n"
        f"<b>💳 Сумма оплат за подписки:</b> {sum_channel_purchase} грн\n\n"
        f"<b>👤 Юзер нейм:</b> @{user_model.username}\n"
        f"<b>📋 Всего заявок:</b> {len(user_offers)}\n"
        f"<b>💵 Оплачено:</b> {len(succ_offer_purchase)} грн\n"
        f"<b>❌ Отклонено:</b> {len(canceled_offer_purchase)} грн\n"
        f"<b>⌛ На рассмотрении:</b> {len([offer for offer in user_offers if offer.status == OfferStatus.WAIT_ADMIN_CONFIRM])}"
    )

    return {
        'user_data': user_info_text
    }


async def get_mailing_message(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    return {
        'message': dialog_manager.dialog_data.get('message')
    }