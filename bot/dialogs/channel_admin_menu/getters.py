from aiogram import Bot, Dispatcher
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.utils.constants import traffic_sources_dict, target_sources_dict, OfferStatus, DEFAULT_CHANNEL_TOPPICS, ChannelStatus


async def get_main_menu_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    return {
        'have_offers': bool(await repo.offer_repo.get_offers(user_id=event_from_user.id))
    }


async def get_admin_offers(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):

    admin_offers = await repo.offer_repo.get_offers(status=dialog_manager.start_data['selected_offer_status'], user_id=event_from_user.id)

    return {
        "offers_list": [
            (offer.id, f"{offer.channel_name}", offer.target_request_amount) for offer in admin_offers
        ],
        'offer_status': dialog_manager.start_data['selected_offer_status']
    }


async def get_offer_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_offer_id = dialog_manager.start_data.get('selected_offer_id')
    offer_info = await repo.offer_repo.get_offers(offer_id=selected_offer_id)
    return {
        'offer_id': offer_info.id,
        'offer_name': offer_info.channel_name,
        'offer_conditions': offer_info.traffic_rules,
        'price': offer_info.first_price_per_request,
        'target_amount': offer_info.target_request_amount,
        'offer_topic': DEFAULT_CHANNEL_TOPPICS.get(offer_info.channel_theme),
        'first_window': True if not dialog_manager.start_data.get('selected_offer_status') else False
    }


async def get_select_traffic_source_data(dialog_manager: DialogManager, **middleware_data):
    return {
        'traffic_sources_list': [
            (key, value)
            for key, value in traffic_sources_dict.items()
        ]
    }


async def get_channel_info(dialog_manager: DialogManager, repo: Repo, **middleware_data):
    selected_channel_id = dialog_manager.dialog_data.get('selected_channel_id')
    channel_model = await repo.channel_repo.get_channel(selected_channel_id)
    return {
        'channel_name': channel_model.channel_title,
        'channel_topic': channel_model.channel_theme,
        'amount_subs': channel_model.subs_amount,
        'min_price': channel_model.minimal_ad_price,
        'audience': f"{channel_model.male_percent}/{channel_model.female_percent}",
        'reach_1_public': channel_model.avg_reach_one_publication,
        'reach_ad_1_public': channel_model.avg_reach_one_ad_publication,
        'comment': channel_model.comment,
    }


async def get_target_sources(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    return {
        'sources_list': [
            (key, value) for key, value in target_sources_dict.items()
        ]
    }


async def get_entered_offer_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    dialog_data = dialog_manager.dialog_data
    text = (f"Назва каналу: {dialog_data['channel_title']}\n"
            f"Тематика каналу: {dialog_data['channel_theme']}\n"
            f"Необхідна кількість заявок: {dialog_data['amount_requests']}\n"
            f"Терміни виконання: {dialog_data['deadline']}\n"
            f"Ціна за заявку: {dialog_data['price_per_request']}\n"
            f"Вимоги до трафіку: {dialog_data['traffic_rules']}\n"
            f"Коментар: {dialog_data['comment']}\n"
            f"Контакти для звязку: {dialog_data['contact']}\n"
            )

    return {
        'offer_info': text
    }


async def get_add_channel_url(dialog_manager: DialogManager, bot: Bot, dp: Dispatcher, event_from_user: User, **middleware_data):
    dialog_manager.dialog_data.update(payment_type='offer_purchase')
    state = dp.fsm.get_context(bot=bot, user_id=event_from_user.id, chat_id=event_from_user.id)
    await state.set_state('CreateOffer')
    await state.update_data(dialog_manager.dialog_data)
    bot_info = await bot.get_me()
    url = f"https://t.me/{bot_info.username}?startchannel&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
    return {
        'add_channel_url': url
    }


async def get_criteria_for_sort(dialog_manager: DialogManager, **middleware_data):
    return {
        'criteria_list': [
            ('amount_subs', 'К-ть підписників'),
        ]
    }


async def get_channels_with_criteria(dialog_manager: DialogManager, repo: Repo, **middleware_data):
    sort_criteria = dialog_manager.dialog_data.get('sort_criteria', 'asc')
    channels_model = await repo.channel_repo.get_channels(sort_type=sort_criteria, status=ChannelStatus.ACTIVE)
    return {
        'channels_list': [
            (channel.id, f"{channel.channel_title} - {channel.subs_amount} підпис.") for channel in channels_model
        ],
        'sort_criteria': sort_criteria,
        'category': DEFAULT_CHANNEL_TOPPICS.get(dialog_manager.dialog_data.get('selected_channel_theme'))
    }


async def get_personal_cabinet_data(dialog_manager: DialogManager, repo: Repo, i18n: I18nContext, event_from_user: User, **middleware_data):
    user_offers = await repo.offer_repo.get_offers(user_id=event_from_user.id)
    all_reserved_money = [order.money_reserved for order in user_offers if user_offers]
    return {
        'active_offers': len(user_offers) if user_offers else 0,
        'money_in_reserv': sum(all_reserved_money) if all_reserved_money else 0,
        'offer_statuses': [(OfferStatus.ACTIVE, i18n.get('I_active_orders')), (OfferStatus.COMPLETED, i18n.get('I_finished_orders'))],
    }


async def get_offers_with_theme(dialog_manager: DialogManager, repo: Repo, **middleware_data):
    channels_model = await repo.offer_repo.get_offers(channel_theme=dialog_manager.dialog_data.get('selected_channel_theme'), )
    return {
        'offers': [
            (channel.id, f"{channel.channel_name} - {channel.target_request_amount}") for channel in channels_model
        ] if channels_model else [],
        'category': DEFAULT_CHANNEL_TOPPICS.get(dialog_manager.dialog_data.get('selected_channel_theme'))
    }


