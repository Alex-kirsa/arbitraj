from enum import StrEnum, Enum


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


class TargetSource(Enum):
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
    TrafficSource.TWITTER: TrafficSource.TWITTER.value,
    TrafficSource.REDDIT: TrafficSource.REDDIT.value,
    TrafficSource.TG_CHANNEL: TrafficSource.TG_CHANNEL.value
}

target_sources_dict = {
    TargetSource.ONLY_FANS: TargetSource.ONLY_FANS.value,
    TargetSource.WEB_STORE: TargetSource.WEB_STORE.value,
    TargetSource.TG_CHANNEL: TargetSource.TG_CHANNEL.value
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
    ACTIVE = "active"


class OfferStatus(StrEnum):
    WAIT_FOR_PAYMENT = "wait_for_payment"
    WAIT_CONFIRM_PAYMENT = "wait_confirm_payment"
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"
    IN_WORK = "in_work"


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
