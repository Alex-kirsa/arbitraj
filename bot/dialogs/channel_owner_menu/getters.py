from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.db import Repo
from bot.utils.constants import DEFAULT_CHANNEL_TOPICS, ChannelStatus


async def get_personal_cabinet_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    user_model = await repo.user_repo.get_user(event_from_user.id)
    channels_model = await repo.channel_repo.get_channels(channel_owner_id=event_from_user.id)
    data = {
        'balance': user_model.balance,
        'channels_amount': len(channels_model) if channels_model else 0
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
    user_channels_model = await repo.channel_repo.get_channels(channel_owner_id=event_from_user.id)
    return {
        'user_channels': [
            (channel.id, f"{channel.channel_title}-{channel.subs_amount}")
            for channel in user_channels_model if channel.status == ChannelStatus.ACTIVE
        ]
    }


async def get_channel_info(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    channel_model = await repo.channel_repo.get_channel(dialog_manager.dialog_data['selected_channel_id'])
    return {
        'channel_name': channel_model.channel_title,
        'channel_theme': channel_model.channel_theme,
        'min_price': channel_model.minimal_ad_price,
        'amount_subs': channel_model.subs_amount,
        'audience': f"{channel_model.male_percent}/{channel_model.female_percent}",
        'reach_1_public': channel_model.avg_reach_one_publication,
        'reach_ad_1_public': channel_model.avg_reach_one_ad_publication,
        'comment': channel_model.comment,

    }


async def get_channel_themes(dialog_manager: DialogManager, **middleware_data):
    return {
        'channel_topics': [(topic_key, topic_value) for topic_key, topic_value in DEFAULT_CHANNEL_TOPICS.items()]
    }


async def get_channels_in_theme(dialog_manager: DialogManager,  repo: Repo, event_from_user: User, **middleware_data):
    selected_topic = dialog_manager.dialog_data['selected_channel_topic']
    channels_list = await repo.channel_repo.get_channels(channel_theme=selected_topic)
    return {
        'category': DEFAULT_CHANNEL_TOPICS.get(selected_topic),
        'channels_list': [(channel.id, f"{channel.channel_title}-{channel.subs_amount}") for channel in channels_list]
    }


async def get_channel_owner_main_menu_data(dialog_manager: DialogManager, repo: Repo, event_from_user: User, **middleware_data):
    channels_model = await repo.channel_repo.get_channels(channel_owner_id=event_from_user.id)
    return {
        'have_channel': bool(channels_model)
    }