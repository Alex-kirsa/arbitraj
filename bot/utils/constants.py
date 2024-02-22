from enum import StrEnum


class RoleTypes(StrEnum):
    ADMIN = "admin"
    WEB_MASTER = "web_master"
    NEWBIE = "newbie"
    CHANNEL_ADMIN = "channel_admin"
    CHANNEL_OWNER = "channel_owner"


class TrafficSource(StrEnum):
    """Источник трафика"""
    TIK_TOK = "tik_tok"
    REALS = "reals"
    TWITTER = "twitter"
    REDDIT = "reddit"
    TG_CHANNEL = "tg_channel"


categories_for_zaliv = {
    'tg_channel_requests': 'Заявки в Телеграм-каналы',
    'gambling': 'Гемблинг',
    'only_fans': "Анкеты OnlyFans",
    'web_store': "Интернет-магазин"
}

traffic_sources_dict = {
    TrafficSource.TIK_TOK: 'Tik-Tok',
    TrafficSource.REALS: 'Reals',
    TrafficSource.TWITTER: 'Twitter',
    TrafficSource.REDDIT: 'Reddit'
}
