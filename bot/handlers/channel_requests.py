from aiogram import Router
from aiogram.types import ChatJoinRequest
from aiogram_dialog import DialogManager

from bot.db import Repo

router = Router()


@router.chat_join_request()
async def chat_join_handler(request: ChatJoinRequest, repo: Repo, dialog_manager: DialogManager):
    invite_link = request.invite_link.invite_link
    print('invite_link', invite_link)