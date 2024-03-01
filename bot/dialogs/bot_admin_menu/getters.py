from aiogram import Bot, Dispatcher
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from bot.db import Repo
from bot.utils.constants import traffic_sources_dict, target_sources_dict, OfferStatus, DEFAULT_CHANNEL_TOPPICS

