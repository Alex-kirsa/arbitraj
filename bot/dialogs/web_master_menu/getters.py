import datetime
import logging

from aiogram import Bot
from aiogram.types import User
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager

from bot.db import Repo
from bot.utils.constants import categories_for_zaliv, traffic_sources_dict, RoleTypes, TrafficSource, WithdrawStatus, TargetSource, DEFAULT_CHANNEL_TOPPICS, OfferStatus, \
    GamblingOfferStatus, target_sources_dict
from bot.utils.misc import create_link_for_publish


async def get_main_menu_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    # data = dialog_manager.start_data if dialog_manager.start_data else dict()
    data = dict()
    user_model = await repo.user_repo.get_user(event_from_user.id)
    data['user_role'] = user_model.role
    data['have_offer'] = bool(await repo.offer_repo.get_offer_in_work(user_id_web_master=event_from_user.id))
    return data


async def get_personal_cabinet_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    active_withdraw_operations = await repo.payment_repo.get_withdraw_request_with_status(user_id=event_from_user.id,
                                                                                          status=WithdrawStatus.ACTIVE)
    completed_withdraw_operations = await repo.payment_repo.get_withdraw_request_with_status(user_id=event_from_user.id,
                                                                                             status=WithdrawStatus.COMPLETED)
    all_user_took_offers = await repo.offer_repo.get_offer_in_work(user_id_web_master=event_from_user.id)
    list_of_links = [offer.channel_invite_link for offer in all_user_took_offers if offer.channel_invite_link]
    leads_amount = await repo.offer_repo.get_channel_invite_requests(invite_link=list_of_links)
    data = {
        'leads': len(leads_amount) if leads_amount else 0,
        'balance': user_model.balance,
        'earned': user_model.earned,
        'waiting_for_withdraw': sum([p_operation.amount for p_operation in active_withdraw_operations]) if active_withdraw_operations else 0,
        'paid': sum([p_operation.amount for p_operation in completed_withdraw_operations]) if completed_withdraw_operations else 0,
    }
    return data


async def get_select_traffic_source_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        traffic_sources_list = [
            (key.name, value)
            for key, value in traffic_sources_dict.items()
            if key == TrafficSource.TIK_TOK
        ]
    else:
        traffic_sources_list = [
            (key.name, value)
            for key, value in traffic_sources_dict.items() if key != TrafficSource.TG_CHANNEL
        ]
    return {
        'traffic_sources_list': traffic_sources_list
    }


async def get_target_sources(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        target_sources_list = [
            (TargetSource.TG_CHANNEL.name, 'Заявки в Телеграм-каналы')
        ]
    else:
        target_sources_list = []
        for key, value in target_sources_dict.items():
            if key == TargetSource.ONLY_FANS.name:
                target_sources_list.append((TargetSource.GAMBLING.name, TargetSource.GAMBLING.value))
            target_sources_list.append((key, value,))
        # target_sources_list = [
        #     (key, value,)
        #     for key, value in target_sources_dict.items()
        # ]

    return {
        'sources_list': target_sources_list,
        'user_role': user_model.role
    }


async def get_offers(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_target_source = dialog_manager.dialog_data.get('selected_target_source')
    if selected_target_source == TargetSource.TG_CHANNEL.name:
        traffic_source = dialog_manager.dialog_data.get('selected_traffic_source')
        offers_in_work_in_user = await repo.offer_repo.get_offer_in_work(user_id_web_master=event_from_user.id)
        offers_in_work_list = [offer.offer_id for offer in offers_in_work_in_user]
        offers_model = await repo.offer_repo.get_offers_by_target_source_and_traffic_source(target_source=selected_target_source, traffic_source=traffic_source)
        offers_list = [
            (offer.id, f"{offer.channel_name} - {offer.target_request_amount}")
            for offer in offers_model if offer.id not in offers_in_work_list
        ]
    else:
        gambling_offers = await repo.offer_repo.get_gambling_offers(status=GamblingOfferStatus.ACTIVE)
        offers_list = [
            (offer.id, f"{offer.casino_name}")
            for offer in gambling_offers
        ]
    # source = None
    # for target_source in target_sources_dict.items():
    #     if str(target_source) == str(selected_target_source):
    #         source = target_sources_dict.get(target_source)
    return {
        'offers_list': offers_list,
        'source': target_sources_dict.get(selected_target_source),
        'datetime_now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        "offer_status": OfferStatus.COMPLETED
    }


async def get_offer_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_offer_id = dialog_manager.dialog_data.get('selected_offer_id')
    selected_target_source = dialog_manager.dialog_data.get('selected_target_source')
    if selected_target_source == TargetSource.TG_CHANNEL.name:
        offer_model = await repo.offer_repo.get_offers(offer_id=selected_offer_id)
        offers_in_work = await repo.offer_repo.get_offer_in_work(selected_offer_id)
        sum_all_requests = sum([offer.current_reqeusts_amount for offer in offers_in_work])
        requests_amount_left = offer_model.target_request_amount - sum_all_requests
        return {
            'offer_id': selected_offer_id,
            'offer_name': offer_model.channel_name,
            'offer_conditions': offer_model.traffic_rules,
            'price': offer_model.second_price_per_request,
            'target_amount': offer_model.target_request_amount,
            'offer_topic': DEFAULT_CHANNEL_TOPPICS.get(offer_model.channel_theme) if offer_model.channel_theme != 'other'
            else f"{DEFAULT_CHANNEL_TOPPICS.get(offer_model.channel_theme)}: {offer_model.custom_channel_theme}",
            'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
            'selected_target_source': selected_target_source,
            'requests_amount_left': requests_amount_left
        }
    elif selected_target_source == TargetSource.GAMBLING.name:
        gambling_offer_info = await repo.offer_repo.get_gambling_offers(offer_id=selected_offer_id)
        return {
            'offer_id': gambling_offer_info.id,
            'casino_name': gambling_offer_info.casino_name,
            'selected_target_source': selected_target_source,
        }


async def get_account_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    return {
        'balance': user_model.balance,
    }


async def get_taked_offer_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, bot: Bot, **middleware_data):
    data: dict = await get_offer_info(dialog_manager, repo, event_from_user, **middleware_data)
    selected_offer_id = dialog_manager.dialog_data.get('selected_offer_id')
    selected_target_source = dialog_manager.dialog_data.get('selected_target_source')
    if selected_target_source == TargetSource.TG_CHANNEL.name:
        offer_model = await repo.offer_repo.get_offers(offer_id=selected_offer_id)
        try:
            channel_invite_link = await bot.create_chat_invite_link(offer_model.channel_id, creates_join_request=True)
        except Exception as e:
            logging.error(f"Error while getting channel link for offer {offer_model.id}: {e}")
            return
        link_for_publish = await create_link_for_publish(channel_invite_link.invite_link)
        await repo.offer_repo.add_offer_in_work(selected_offer_id, event_from_user.id, channel_invite_link.invite_link, link_for_publish, status=OfferStatus.IN_WORK)
        data['link'] = link_for_publish
    else:
        gambling_offer = await repo.offer_repo.get_gambling_offers(offer_id=selected_offer_id)
        free_offer_link = await repo.offer_repo.get_free_gambling_offer_link(gambling_offer_id=selected_offer_id)
        await repo.offer_repo.update_gambling_offer_link(free_offer_link.id, user_id=event_from_user.id)
        free_offer_link_left = await repo.offer_repo.get_free_gambling_offer_link(gambling_offer_id=selected_offer_id)
        if not free_offer_link_left:
            await repo.offer_repo.update_gambling_offer(selected_offer_id, status=GamblingOfferStatus.NO_ACTIVE_LINK)
        link = free_offer_link.link
        data['link'] = link
        data['deposits'] = free_offer_link.current_deposit
    return data


async def get_referral_system_data(dialog_manager: DialogManager, bot: Bot, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    deep_link = await create_start_link(bot, str(event_from_user.id))
    return {
        'link': deep_link,
        'earned': user_model.earned_from_referals,
    }


async def get_offers_in_user(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    selected_target_source = dialog_manager.dialog_data.get('selected_target_source')
    if selected_target_source == TargetSource.TG_CHANNEL.name:
        offers_in_work_model = await repo.offer_repo.get_offer_in_work(user_id_web_master=event_from_user.id, status=OfferStatus.IN_WORK)
        if not offers_in_work_model:
            offers_list = []
        else:
            offer_models_list = [
                await repo.offer_repo.get_offers(offer_id=offer.offer_id)
                for offer in offers_in_work_model
            ]
            offers_list = [
                (offer_model.id, f"{offer_model.channel_name}-{offer_model.target_request_amount}")
                for offer_model in offer_models_list
            ]
    elif selected_target_source == TargetSource.GAMBLING.name:
        gambling_offers_links = await repo.offer_repo.get_gambling_offer_links(user_id=event_from_user.id)
        gambling_offers = [
            await repo.offer_repo.get_gambling_offers(offer_id=gambling_offer_link.gambling_offer_id)
            for gambling_offer_link in gambling_offers_links
        ]
        offers_list = [
            (offer.id, f"{offer.casino_name}")
            for offer in gambling_offers
        ]
    else:
        raise ValueError(f"Unknown target source: {selected_target_source}")
    return {
        'offers_list': offers_list,
        'category': categories_for_zaliv.get(selected_target_source),
        'datime_now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        "offer_status": OfferStatus.COMPLETED
    }


async def get_offer_info_in_user(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    data: dict = await get_offer_info(dialog_manager, repo, event_from_user, **middleware_data)
    if dialog_manager.dialog_data.get('selected_target_source') == TargetSource.TG_CHANNEL.name:
        selected_offer_id = dialog_manager.dialog_data.get('selected_offer_id')
        offer_model = await repo.offer_repo.get_offers(offer_id=selected_offer_id)
        offers_in_work_model = await repo.offer_repo.get_offer_in_work_in_web_master(offer_id=selected_offer_id, user_id_web_master=event_from_user.id)
        requests_amount = await repo.offer_repo.get_channel_invite_requests(invite_link=offers_in_work_model.channel_invite_link)
        offers_in_work = await repo.offer_repo.get_offer_in_work(selected_offer_id)
        sum_all_requests = sum([offer.current_reqeusts_amount for offer in offers_in_work])
        requests_amount_left = offer_model.target_request_amount - sum_all_requests

        data['reqests_amount_from_user'] = len(requests_amount) if requests_amount else 0
        data['earned'] = offers_in_work_model.earned_money
        data['link'] = offers_in_work_model.redirect_link
        data['requests_amount_left'] = requests_amount_left
    else:
        gambling_offer_link = await repo.offer_repo.get_gambling_offer_links_by_user_id_and_offer_id(user_id=event_from_user.id, offer_id=data['offer_id'])
        data['deposits'] = gambling_offer_link.current_deposit
        data['link'] = gambling_offer_link.link
    return data
