from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.db import Repo
from bot.utils.test_data import channels, topics


async def get_personal_cabinet_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    data = {
        'balance': user_model.balance,
        'channels_amount': 3
    }
    return data


async def get_payment_method_data(dialog_manager: DialogManager, **middleware_data):
    return {
        'price': 190
    }


async def get_payment_data(dialog_manager: DialogManager, **middleware_data):
    return {
        'price': 190
    }


async def get_user_channels(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    return {
        'user_channels': [
            (channel_id, f"{channel_data['channel_name']}-{channel_data['amount_subs']}")
            for channel_id, channel_data in channels.items()
        ]
    }


async def get_channel_info(dialog_manager: DialogManager, **middleware_data):

    return channels[dialog_manager.dialog_data['selected_channel']]


async def get_channel_topics(dialog_manager: DialogManager, **middleware_data):
    return {
        'channel_topics': topics
    }


async def get_selected_topic(dialog_manager: DialogManager, **middleware_data):
    selected_topic = ''
    for topic in topics:
        if topic[0] == dialog_manager.dialog_data['selected_channel_topic']:
            selected_topic = topic[1]
            break
    return {
        'category': selected_topic,
        'channels_list': [(channel_id, f"{channel_data['channel_name']}-{channel_data['amount_subs']}") for channel_id, channel_data in channels.items()]
    }