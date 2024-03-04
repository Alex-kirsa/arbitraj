import os

from aiogram import Bot
from aiogram_i18n.cores import FluentRuntimeCore
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from bot.db.base import metadata
from bot.services.scheduler.func import send_scheduled_message
from configreader import config, RedisConfig


async def startup(ctx):
    engine = create_async_engine(
        str(config.postgredsn), future=True, echo=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    # Creating DB connections pool
    db_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    ctx["db_factory"] = db_factory
    ctx['bot'] = Bot(token=config.bot_token, parse_mode='HTML')
    path_to_locales = os.path.join("bot", "locales", "{locale}", "LC_MESSAGES")
    core = FluentRuntimeCore(path=path_to_locales, default_locale="ru")
    await core.startup()
    ctx["core"] = core


async def shutdown(ctx):
    bot: Bot = ctx['bot']
    await bot.session.close()


class WorkerSettings:
    redis_settings = RedisConfig.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_scheduled_message, ]
