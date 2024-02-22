import aiohttp
from aiogram import Router, Bot
from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

router = Router()


