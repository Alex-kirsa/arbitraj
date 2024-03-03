import os.path

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.models import *
from configreader import config


class Sheet:
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    path_to_cred = os.path.join(os.path.dirname(__file__), "cred.json")
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(path_to_cred, scopes).authorize(
        httplib2.Http())
    service = build('sheets', 'v4', http=creds_service)
    sheet = service.spreadsheets()
    tables_translation = {
        "Users": "Пользователи",
        "ChannelsForTraffic": "Каналы для Трафика",
        "Channels": "Каналы",
        "Offers": "Офферы",
        "GamblingOffers": "Азартные Офферы",
        "GamblingOffersLinks": "Ссылки на Азартные Офферы",
        "OffersInWork": "Офферы в Работе",
        "ChannelInviteRequests": "Запросы на Приглашения в Каналы",
        "TopUpRequests": "Запросы на Пополнение",
        "WithdrawRequests": "Запросы на Вывод Средств"
    }

    @classmethod
    def rewrite_sheet(cls, table: str, val: list[list]):
        table = cls.tables_translation.get(table, table)
        try:
            cls.service.spreadsheets().values().clear(spreadsheetId=config.sheet_id, range=f"{table}!A2:Z100000").execute()
            cls.sheet.values().append(
                spreadsheetId=config.sheet_id,
                range=f"{table}!A2",
                valueInputOption="RAW",
                # insertDataOption="INSERT_ROWS",
                body={'values': val}).execute()
        except HttpError:
            pass


async def write_to_google_sheets(session: AsyncSession):
    sheet = Sheet()
    result = await session.execute(select(Users))
    users = result.scalars().all()
    user_values = [
        [user.user_id, user.username, user.fullname, user.role.value if user.role else None, user.balance, user.earned,
         user.earned_from_referals, str(user.registration_date), user.refferer_id] for user in users
    ]
    sheet.rewrite_sheet("Users", user_values)

    # Получаем данные из таблицы ChannelsForTraffic и записываем их в Google Sheets
    result = await session.execute(select(ChannelsForTraffic))
    channels_for_traffic = result.scalars().all()
    channels_for_traffic_values = [
        [channel.id, channel.channel_id, channel.channel_owner_id, channel.channel_title, channel.status.value] for channel
        in channels_for_traffic
    ]
    sheet.rewrite_sheet("ChannelsForTraffic", channels_for_traffic_values)

    # Получаем данные из таблицы Channels и записываем их в Google Sheets
    result = await session.execute(select(Channels))
    channels = result.scalars().all()
    channels_values = [
        [channel.id, channel.channel_title, channel.channel_owner_id, channel.channel_theme, channel.custom_channel_theme,
         channel.channel_invite_link, channel.subs_amount, channel.male_percent, channel.female_percent,
         channel.avg_reach_one_publication, channel.avg_reach_one_ad_publication, channel.minimal_ad_price, channel.comment,
         channel.contact, channel.status.value] for channel in channels
    ]
    sheet.rewrite_sheet("Channels", channels_values)

    # Получаем данные из таблицы Offers и записываем их в Google Sheets
    result = await session.execute(select(Offers))
    offers = result.scalars().all()
    offers_values = [
        [offer.id, offer.user_id, offer.target_source, offer.traffic_source.value, offer.channel_id, offer.channel_name,
         offer.channel_theme, offer.custom_channel_theme, offer.target_request_amount, offer.first_price_per_request,
         offer.second_price_per_request, offer.money_reserved, offer.offer_deadline, offer.traffic_rules, offer.comment,
         offer.contacts, offer.status.value] for offer in offers
    ]
    sheet.rewrite_sheet("Offers", offers_values)

    # Получаем данные из таблицы GamblingOffers и записываем их в Google Sheets
    result = await session.execute(select(GamblingOffers))
    gambling_offers = result.scalars().all()
    gambling_offers_values = [
        [offer.id, offer.casino_name, offer.status.value] for offer in gambling_offers
    ]
    sheet.rewrite_sheet("GamblingOffers", gambling_offers_values)

    # Получаем данные из таблицы GamblingOffersLinks и записываем их в Google Sheets
    result = await session.execute(select(GamblingOffersLinks))
    gambling_offers_links = result.scalars().all()
    gambling_offers_links_values = [
        [link.id, link.gambling_offer_id, link.link, link.user_id, link.current_deposit] for link in gambling_offers_links
    ]
    sheet.rewrite_sheet("GamblingOffersLinks", gambling_offers_links_values)

    result = await session.execute(select(OffersInWork))
    offers_in_work = result.scalars().all()
    offers_in_work_values = [
        [offer.id, offer.offer_id, offer.user_id_web_master, offer.current_reqeusts_amount, offer.earned_money,
         offer.channel_invite_link, offer.redirect_link, offer.status.value] for offer in offers_in_work
    ]
    sheet.rewrite_sheet("OffersInWork", offers_in_work_values)

    # Получаем данные из таблицы ChannelInviteRequests и записываем их в Google Sheets
    result = await session.execute(select(ChannelInviteRequests))
    channel_invite_requests = result.scalars().all()
    channel_invite_requests_values = [
        [request.id, request.offer_id, request.channel_id, request.invite_link, request.user_id] for request in channel_invite_requests
    ]
    sheet.rewrite_sheet("ChannelInviteRequests", channel_invite_requests_values)

    # Получаем данные из таблицы TopUpRequests и записываем их в Google Sheets
    result = await session.execute(select(TopUpRequests))
    top_up_requests = result.scalars().all()
    top_up_requests_values = [
        [request.id, request.user_id, request.offer_id, request.channel_id, request.payment_method, request.fullname,
         request.last_4_digits_credit_card, request.amount, request.status] for request in top_up_requests
    ]
    sheet.rewrite_sheet("TopUpRequests", top_up_requests_values)

    # Получаем данные из таблицы WithdrawRequests и записываем их в Google Sheets
    result = await session.execute(select(WithdrawRequests))
    withdraw_requests = result.scalars().all()
    withdraw_requests_values = [
        [request.id, request.user_id, request.payment_system, request.bank_name, request.card_number,
         request.crypto_adress, request.amount, request.status.value] for request in withdraw_requests
    ]
    sheet.rewrite_sheet("WithdrawRequests", withdraw_requests_values)
    return "https://docs.google.com/spreadsheets/d/15j8fl_NQDQNYV9jNuXIIQU09LQO7flK3xyppO1TRCy4/edit#gid=0"
