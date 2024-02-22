from aiogram_dialog import DialogManager

from bot.utils.constants import traffic_sources_dict, TrafficSource
from bot.utils.test_data import offers, channels


async def get_active_orders(dialog_manager: DialogManager, **middleware_data):
    offers_list = [
        (offer_key, f"{offer_value['offer_name'] if offer_value['offer_type'] == 'tg_channel_requests' else offer_value['casino_name']}")
        for offer_key, offer_value in offers.items()
    ]
    return {
        "offers_list": offers_list
    }


async def get_offer_info(dialog_manager: DialogManager, **middleware_data):
    selected_offer_id = dialog_manager.dialog_data.get('selected_offer')
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
        'selected_category': offer_info['offer_type'],
    } if offer_info['offer_type'] == 'tg_channel_requests' else {
            'offer_id': selected_offer_id,
            'casino_name': offer_info['casino_name'],
            'link': offer_info['link'],
            'personal_offers': 'personal_offers' in dialog_manager.start_data if dialog_manager.start_data else False,
            'selected_category': offer_info['offer_type'],
        }


async def get_select_traffic_source_data(dialog_manager: DialogManager, **middleware_data):
    traffic_sources_dict[TrafficSource.TG_CHANNEL] = 'Telegram канал'
    return {
        'traffic_sources_list': [
            (key, value)
            for key, value in traffic_sources_dict.items()
        ]
    }


async def get_channel_info(dialog_manager: DialogManager, **middleware_data):
    selected_channel = dialog_manager.dialog_data.get('selected_channel')
    return channels[selected_channel]
