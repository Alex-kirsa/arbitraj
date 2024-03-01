from sqlalchemy import ForeignKey, Enum
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, FLOAT, TEXT
from sqlalchemy.orm import mapped_column

from bot.db.base import Base
from bot.utils.constants import RoleTypes, TrafficSource, ChannelStatus, OfferStatus, WithdrawStatus, GamblingOfferStatus, TopUpStatus


class Users(Base):
    __tablename__ = "users"

    user_id = mapped_column(BIGINT, primary_key=True)
    username = mapped_column(VARCHAR(255), nullable=True, doc='Username в Telegram', name='Username в Telegram')
    fullname = mapped_column(VARCHAR(255), nullable=False)
    role = mapped_column(Enum(RoleTypes), nullable=True, doc='Роль пользователя', name='Роль пользователя')
    balance = mapped_column(FLOAT, nullable=False, doc='Баланс пользователя', name='Баланс пользователя', default=0)
    earned = mapped_column(FLOAT, nullable=False, doc='Заработано денег', name='Заработано денег', default=0)
    earned_from_referals = mapped_column(FLOAT, nullable=False, doc='Заработано денег с рефералов', name='Заработано денег с рефералов', default=0)
    refferer_id = mapped_column(BIGINT, nullable=True, doc='ID реферала', name='ID реферала')


class ChannelsForTraffic(Base):
    __tablename__ = "channels_for_traffic"

    id = mapped_column(BIGINT, primary_key=True)
    channel_id = mapped_column(BIGINT, nullable=False, unique=True, doc='ID канала', name='ID канала')
    channel_owner_id = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID владельца канала', name='ID владельца канала')
    channel_title = mapped_column(VARCHAR(255), nullable=False, doc='Название канала', name='Название канала')
    status = mapped_column(Enum(ChannelStatus), nullable=False, default=ChannelStatus.WAIT_FOR_PAYMENT)


class Channels(Base):
    __tablename__ = "channels"

    id = mapped_column(BIGINT, primary_key=True)
    channel_title = mapped_column(VARCHAR(255), nullable=False, doc='Название канала', name='Название канала')
    channel_owner_id = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID владельца канала', name='ID владельца канала')
    channel_theme = mapped_column(VARCHAR(255), nullable=False, doc='Тематика канала', name='Тематика канала')
    custom_channel_theme = mapped_column(VARCHAR(255), nullable=True, doc='Кастомна Тематика канала', name='Кастомна Тематика канала')
    channel_invite_link = mapped_column(VARCHAR(255), nullable=False, doc='Ссылка на канал', name='Ссылка на канал')
    subs_amount = mapped_column(BIGINT, nullable=False, doc='Количество подписчиков', name='Количество подписчиков')
    male_percent = mapped_column(FLOAT, nullable=False, doc='Процент мужчин', name='Процент мужчин')
    female_percent = mapped_column(FLOAT, nullable=False, doc='Процент женщин', name='Процент женщин')
    avg_reach_one_publication = mapped_column(FLOAT, nullable=False, doc='Средний охват одной публикации', name='Средний охват одной публикации')
    avg_reach_one_ad_publication = mapped_column(FLOAT, nullable=False, doc='Средний охват одной рекламной публикации', name='Средний охват одной рекламной публикации')
    minimal_ad_price = mapped_column(FLOAT, nullable=False, doc='Минимальная цена рекламы', name='Минимальная цена рекламы')
    comment = mapped_column(TEXT, nullable=False, doc='Комментарий', name='Комментарий')
    contact = mapped_column(VARCHAR(255), nullable=False, doc='Контакт', name='Контакт')
    status = mapped_column(Enum(ChannelStatus), nullable=False, default=ChannelStatus.WAIT_ADMIN_CONFIRM)


class Offers(Base):
    __tablename__ = "offers"

    id = mapped_column(BIGINT, primary_key=True)
    user_id = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID пользователя', name='ID пользователя')
    target_source = mapped_column(VARCHAR(255), nullable=False, doc='Источник трафика', name='Источник трафика')
    traffic_source = mapped_column(Enum(TrafficSource), nullable=False, doc='Тип трафика', name='Тип трафика')
    # offer_type = mapped_column(VARCHAR(255), nullable=False, doc='Тип оффера', name='Тип оффера')
    channel_id = mapped_column(BIGINT, ForeignKey(ChannelsForTraffic.channel_id), nullable=False, doc='ID канала', name='ID канала')
    channel_name = mapped_column(VARCHAR(255), nullable=False, doc='Название канала', name='Название канала')
    channel_theme = mapped_column(VARCHAR(255), nullable=False, doc='Тематика канала', name='Тематика канала')
    custom_channel_theme = mapped_column(VARCHAR(255), nullable=True, doc='Кастомна Тематика канала', name='Кастомна Тематика канала')
    target_request_amount = mapped_column(FLOAT, nullable=False, doc='Сумма запроса', name='Сумма запроса')
    first_price_per_request = mapped_column(FLOAT, nullable=False, doc='Цена за запрос от админа канала', name='Цена за запрос от админа канала')
    second_price_per_request = mapped_column(FLOAT, nullable=True, doc='Цена за запрос от админа бота', name='Цена за запрос от админа бота')
    money_reserved = mapped_column(FLOAT, nullable=False, doc='Зарезервированная сумма', name='Зарезервированная сумма')
    offer_deadline = mapped_column(VARCHAR(255), nullable=False, doc='Дедлайн оффера', name='Дедлайн оффера')
    traffic_rules = mapped_column(TEXT, nullable=False, doc='Правила трафика', name='Правила трафика')
    comment = mapped_column(TEXT, nullable=True, doc='Комментарий', name='Комментарий')
    contacts = mapped_column(VARCHAR(255), nullable=False)
    status = mapped_column(Enum(OfferStatus), nullable=False, default=OfferStatus.WAIT_FOR_PAYMENT)


class GamblingOffers(Base):
    __tablename__ = "gambling_offers"

    id = mapped_column(BIGINT, primary_key=True)
    casino_name = mapped_column(VARCHAR(255), nullable=False, doc='Название оффера', name='Название оффера')
    status = mapped_column(Enum(GamblingOfferStatus), nullable=False, doc='Статус оффера', name='Статус оффера')


class GamblingOffersLinks(Base):
    __tablename__ = "gambling_offers_links"

    id = mapped_column(BIGINT, primary_key=True)
    gambling_offer_id = mapped_column(BIGINT, ForeignKey(GamblingOffers.id), nullable=False, doc='ID оффера', name='ID оффера')
    link = mapped_column(VARCHAR(255), nullable=False, doc='Ссылка на оффер', name='Ссылка на оффер')
    user_id = mapped_column(BIGINT, nullable=True, doc='ID пользователя', name='ID пользователя')
    current_deposit = mapped_column(FLOAT, nullable=False, doc='Текущий депозит', name='Текущий депозит', default=0)


class OffersInWork(Base):
    __tablename__ = "offers_in_work"

    id = mapped_column(BIGINT, primary_key=True)
    offer_id = mapped_column(BIGINT, ForeignKey(Offers.id), nullable=False, doc='ID оффера', name='ID оффера')
    user_id_web_master = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID вебмастера', name='ID вебмастера')
    current_reqeusts_amount = mapped_column(FLOAT, nullable=False, doc='Текущая сумма запросов', name='Текущая сумма запросов', default=0)
    earned_money = mapped_column(FLOAT, nullable=False, doc='Заработано денег', name='Заработано денег', default=0)
    channel_invite_link = mapped_column(VARCHAR(255), nullable=False, unique=True, doc='Ссылка на канал', name='Ссылка на канал')
    redirect_link = mapped_column(VARCHAR(255), nullable=False, unique=True, doc='Ссылка на редирект', name='Ссылка на редирект')
    status = mapped_column(Enum(OfferStatus), nullable=False, doc='Статус оффера', name='Статус оффера')


class ChannelInviteRequests(Base):
    __tablename__ = "channel_invite_requests"

    id = mapped_column(BIGINT, primary_key=True)
    offer_id = mapped_column(BIGINT, ForeignKey(Offers.id), nullable=False, doc='ID оффера', name='ID оффера')
    channel_id = mapped_column(BIGINT, ForeignKey(ChannelsForTraffic.channel_id), nullable=False, doc='ID канала', name='ID канала')
    invite_link = mapped_column(VARCHAR(255), nullable=False, unique=True, doc='Ссылка на канал', name='Ссылка на канал')
    user_id = mapped_column(BIGINT, nullable=False, doc='ID пользователя', name='ID пользователя')


class TopUpRequests(Base):
    __tablename__ = "top_up_requests"

    id = mapped_column(BIGINT, primary_key=True)
    user_id = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID пользователя', name='ID пользователя')
    offer_id = mapped_column(BIGINT, ForeignKey(Offers.id), nullable=True, doc='ID оффера', name='ID оффера')
    payment_method = mapped_column(VARCHAR(255), nullable=False, doc='Тип пополнения', name='Тип пополнения')
    fullname = mapped_column(VARCHAR(255), nullable=True, doc='ФИО', name='ФИО')
    last_4_digits_credit_card = mapped_column(VARCHAR(4), nullable=True, doc='Последние 4 цифры карты', name='Последние 4 цифры карты')
    amount = mapped_column(FLOAT, nullable=False, doc='Сумма пополнения', name='Сумма пополнения')
    status = mapped_column(VARCHAR(255), nullable=False, doc='Статус запроса', name='Статус запроса', default=TopUpStatus.ACTIVE)


class WithdrawRequests(Base):
    __tablename__ = "withdraw_requests"

    id = mapped_column(BIGINT, primary_key=True)
    user_id = mapped_column(BIGINT, ForeignKey(Users.user_id), nullable=False, doc='ID пользователя', name='ID пользователя')
    payment_system = mapped_column(VARCHAR(255), nullable=False, doc='Тип выплаты', name='Тип выплаты')
    bank_name = mapped_column(VARCHAR(255), nullable=True, doc='Название банка', name='Название банка')
    card_number = mapped_column(VARCHAR(255), nullable=True, doc='Номер карты', name='Номер карты')
    crypto_adress = mapped_column(VARCHAR(255), nullable=True, doc='Криптовалютный адрес', name='Криптовалютный адрес')
    amount = mapped_column(FLOAT, nullable=False, doc='Сумма выплаты', name='Сумма выплаты')
    status = mapped_column(Enum(WithdrawStatus), nullable=False, doc='Статус запроса', name='Статус запроса', default=WithdrawStatus.ACTIVE)
