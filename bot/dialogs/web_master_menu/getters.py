import datetime

from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.db import Repo
from bot.utils.constants import categories_for_zaliv, traffic_sources_dict, RoleTypes, TrafficSource
from bot.utils.test_data import offers


async def get_main_menu_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    data = dialog_manager.start_data if dialog_manager.start_data else dict()
    user_model = await repo.user_repo.get_user(event_from_user.id)
    data['user_role'] = user_model.role
    return data


async def get_personal_cabinet_data(dialog_manager: DialogManager, **middleware_data):
    data = {
        'leads': 3,
        'balance': 1000,
        'earned': 2000,
        'waiting_for_payment': 3242,
        'paid': 7504,
    }
    return data


async def get_select_offer_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        categories_list = [(category_key, category_value,) for category_key, category_value in categories_for_zaliv.items() if category_key == 'tg_channel_requests']
    else:
        categories_list = [(category_key, category_value,) for category_key, category_value in categories_for_zaliv.items()]
    return {
        'categories_list': categories_list,
        'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
        'user_role': user_model.role,
    }


async def get_select_traffic_source_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    if user_model.role == RoleTypes.NEWBIE:
        traffic_sources_list = [
            (key, value)
            for key, value in traffic_sources_dict.items()
            if key == TrafficSource.TIK_TOK
        ]
    else:
        traffic_sources_list = [
            (key, value)
            for key, value in traffic_sources_dict.items()
        ]
    return {
        'traffic_sources_list': traffic_sources_list
    }


async def get_offers(dialog_manager: DialogManager, **middleware_data):
    selected_category = dialog_manager.dialog_data.get('selected_category')
    if selected_category == 'tg_channel_requests':
        offers_list = [
            (offer_key, f"{offer_value['offer_name']}-{offer_value['target_amount']}")
            for offer_key, offer_value in offers.items() if offer_value['offer_type'] == selected_category
        ]
    else:
        offers_list = [
            (offer_key, f"{offer_value['casino_name']}")
            for offer_key, offer_value in offers.items() if offer_value['offer_type'] == selected_category
        ]

    return {
        'offers_list': offers_list,
        'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
        'source': traffic_sources_dict.get(dialog_manager.dialog_data.get('selected_traffic_source')),
        'datime_now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    }


async def get_offer_info(dialog_manager: DialogManager, **middleware_data):
    selected_offer_id = dialog_manager.dialog_data.get('selected_offer')
    selected_category = dialog_manager.dialog_data.get('selected_category')
    if selected_category == 'tg_channel_requests':
        offer_info = offers.get(selected_offer_id, dict())
        return {
            'offer_id': selected_offer_id,
            'offer_name': offer_info['offer_name'],
            'offer_conditions': offer_info['offer_conditions'],
            'price': offer_info['price'],
            'target_amount': offer_info['target_amount'],
            'offer_topic': offer_info['offer_topic'],
            'link': offer_info['link'],
            'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
            'selected_category': selected_category,
        }
    elif selected_category == 'gambling':
        offer_info = offers.get(selected_offer_id, dict())
        return {
            'offer_id': selected_offer_id,
            'casino_name': offer_info['casino_name'],
            'link': offer_info['link'],
            'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
            'selected_category': selected_category,
        }


async def get_account_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    return {
        'balance': user_model.balance,
    }
