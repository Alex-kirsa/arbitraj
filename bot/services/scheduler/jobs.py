import datetime

from arq import ArqRedis

from bot.utils.constants import DEFER_NOTIFICATE_WEBMASTER_TIME, DEFER_CLOSE_OFFER_TIME


async def create_send_message_job(arqredis: ArqRedis, offer_id: int, web_master_id: int, locale='uk'):
    job = await arqredis.enqueue_job(
        "send_scheduled_message",
        _job_id=f"send_scheduled_message:{offer_id}",
        _defer_until=datetime.timedelta(hours=DEFER_NOTIFICATE_WEBMASTER_TIME),
        offer_id=offer_id,
        web_master_id=web_master_id,
        locale=locale,
        _job_try=5
    )
    return


async def create_close_offer_job(arqredis: ArqRedis, offer_id: int, web_master_id: int, locale='uk'):
    job = await arqredis.enqueue_job(
        "check_current_requests_amount",
        _job_id=f"check_current_requests_amount:{offer_id}",
        _defer_until=datetime.timedelta(hours=DEFER_CLOSE_OFFER_TIME),
        offer_id=offer_id,
        web_master_id=web_master_id,
        locale=locale,
        _job_try=5
    )
    return
