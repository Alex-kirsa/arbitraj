from enum import StrEnum


class RoleTypes(StrEnum):
    ADMIN = "admin"
    WEB_MASTER = "web_master"
    NEWBIE = "newbie"
    CHANNEL_ADMIN = "channel_admin"
    CHANNEL_OWNER = "channel_owner"


class TrafficSource(StrEnum):
    """Источник трафика"""
    TIK_TOK = "Tik-Tok"
    REELS = "Reels"
    TWITTER = "Twitter"
    REDDIT = "Reddit"
    TG_CHANNEL = "Телеграм канал"


class TargetSource(StrEnum):
    """Источник трафика"""
    ONLY_FANS = "Сторінка OnlyFans"
    WEB_STORE = "Інтернет магазин"
    TG_CHANNEL = "Телеграм канал"
    GAMBLING = "Гемблинг"


categories_for_zaliv = {
    TargetSource.TG_CHANNEL.name: 'Заявки в Телеграм-каналы',
    TargetSource.GAMBLING.name: 'Гемблинг',
    TargetSource.ONLY_FANS.name: "Анкеты OnlyFans",
    TargetSource.WEB_STORE.name: "Интернет-магазин"
}

traffic_sources_dict = {
    TrafficSource.TIK_TOK: TrafficSource.TIK_TOK.value,
    TrafficSource.REELS: TrafficSource.REELS.value,
    TrafficSource.TG_CHANNEL: TrafficSource.TG_CHANNEL.value,
    TrafficSource.TWITTER: TrafficSource.TWITTER.value,
    TrafficSource.REDDIT: TrafficSource.REDDIT.value,
}

target_sources_dict = {
    TargetSource.TG_CHANNEL.name: TargetSource.TG_CHANNEL.value,
    TargetSource.ONLY_FANS.name: TargetSource.ONLY_FANS.value,
    TargetSource.WEB_STORE.name: TargetSource.WEB_STORE.value,
}


class WebAppUrls(StrEnum):
    CREATE_OFFER_WEB_APP = "https://webapp-forms.netlify.app/traffic-requirements-form"
    CONFIRM_PAYMENT_WEB_APP = "https://webapp-forms.netlify.app/payment-verification-form"
    ADD_CHANNEL_WEB_APP = "https://webapp-forms.netlify.app/channel-addition-form"
    WITHDRAW_FUNDS_WEB_APP = "https://webapp-forms.netlify.app/payment-request-form"


class PaymentMethods(StrEnum):
    CRYPTOPAY = "cryptopay"
    ON_CARD = "on_card"


PAYMENT_METHODS = {
    # PaymentMethods.CRYPTOPAY: "Crytopay",
    PaymentMethods.ON_CARD: "Оплата картою",
}

CHANNEL_ADD_PRICE = 100
CARD_NUBMER = "4242 4242 4242 4242"


class ChannelStatus(StrEnum):
    WAIT_ADMIN_CONFIRM = "wait_admin_confirm"
    WAIT_FOR_PAYMENT = "wait_for_payment"
    WAIT_CONFIRM_PAYMENT = "wait_confirm_payment"
    CANCELED = "canceled"
    ACTIVE = "active"


class OfferStatus(StrEnum):
    WAIT_FOR_PAYMENT = "wait_for_payment"
    WAIT_ADMIN_CONFIRM = "wait_admin_confirm"
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"
    IN_WORK = "in_work"


channels_status_named = {
    ChannelStatus.ACTIVE.value: 'Активний',
    ChannelStatus.WAIT_ADMIN_CONFIRM.value: 'Очікує підтвердження',
    ChannelStatus.WAIT_FOR_PAYMENT.value: 'Очікує оплату',
    ChannelStatus.WAIT_CONFIRM_PAYMENT.value: 'Очікує підтвердження оплати',
    ChannelStatus.CANCELED.value: 'Скасований'
}

offers_status_named = {
    OfferStatus.ACTIVE.value: 'Активний',
    OfferStatus.WAIT_ADMIN_CONFIRM.value: 'Очікує підтвердження',
    OfferStatus.WAIT_FOR_PAYMENT.value: 'Очікує оплату',
    OfferStatus.CANCELED.value: 'Скасований',
    OfferStatus.COMPLETED.value: 'Виконаний',
    OfferStatus.IN_WORK.value: 'В роботі'

}


class GamblingOfferStatus(StrEnum):
    ACTIVE = "active"
    NO_ACTIVE_LINK = "no_active_link"


DEFAULT_CHANNEL_TOPPICS = {
    'news': 'Новини',
    'cryptocurrency': 'Криптовалюта',
    'recruiting': 'Рекрутинг',
    'meets': 'Знайомства',
    'linguistics': 'Лінгвістика',
    'sport': 'Спорт',
    'trades': 'Торгівля',
    'services': 'Послуги',
    'other': 'Інше',
}


class WithdrawStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"


class TopUpStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    COMPLETED_BY_CRYPTOBOT = "completed_by_cryptobot"
    CANCELED = "canceled"


casinos_dict = {
    '1': "Casino 1",
}
