from aiogram import Dispatcher, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import ChatMemberUpdated

from configreader import config


class AddBotOnCreateOffer(Filter):
    async def __call__(self, update: ChatMemberUpdated, dp: Dispatcher, bot: Bot) -> bool:
        inviter_id = update.from_user.id
        state = dp.fsm.get_context(bot=bot, user_id=inviter_id, chat_id=inviter_id)
        current_state = str(await state.get_state())
        return current_state in 'CreateOffer' and (
                update.new_chat_member.user.id == int(config.bot_token.split(":")[0])
                and update.new_chat_member.status is ChatMemberStatus.ADMINISTRATOR
        )


class DelBotFilter(Filter):
    async def __call__(self, update: ChatMemberUpdated, dp: Dispatcher, bot: Bot) -> bool:
        return (update.new_chat_member.user.id == int(config.bot_token.split(":")[0]) and update.new_chat_member.status in
                (ChatMemberStatus.MEMBER, ChatMemberStatus.KICKED, ChatMemberStatus.LEFT, ChatMemberStatus.RESTRICTED, ChatMemberStatus.ADMINISTRATOR))
