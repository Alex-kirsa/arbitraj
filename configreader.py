from arq.connections import RedisSettings
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot settings
    bot_token: str
    bot_fsm_storage: str
    bot_username: str
    # Bot Webhook settings
    webhook_path: str
    webhook_host: str
    webhook_port: int
    webhook_secret: str
    webhook_base_url: str
    # I18N
    i18n_format_key: str

    # Google Sheets
    sheet_id: str

    # Info channels
    withdraw_channel_id: int
    offers_channel_id: int
    channels_channel_id: int
    cooperation_channel_id: int

    # CryptoBot
    crypto_api_key: str
    crypto_bot_webhook_path: str

    # WebApp path
    create_offer: str
    add_channel: str
    withdraw_request: str
    payment_confirm: str

    # Redirector Settings
    redirect_token: str
    redirect_base_url: str

    # Devs
    devs: list
    admins: list


    # DB
    postgredsn: PostgresDsn

    # Redis
    redis_db: int
    redis_host: str
    redis_port: int

    @field_validator("bot_fsm_storage")
    def validate_bot_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Config()


class RedisConfig:
    pool_settings = RedisSettings(
        host=config.redis_host,
        port=config.redis_port,
        database=config.redis_db,
    )
