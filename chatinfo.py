from .. import loader, utils
from pyrogram import Client, types, enums

@loader.module('ChatInfo', author='Layz')
class ChatInfoMod(loader.Module):
    async def chat_cmd(self, app: Client, message: types.Message):
        chatId = message.chat.id

        bots = [bot.user.username async for bot in app.get_chat_members(
            chatId, 
            filter=enums.ChatMembersFilter.BOTS # type: ignore
        )]

        owners = [owner.user.username async for owner in app.get_chat_members(
            chatId, 
            filter=enums.ChatMembersFilter.ADMINISTRATORS # type: ignore
        ) if owner.user.username not in bots]

        members = [member.user.username async for member in app.get_chat_members(
            chatId # type: ignore
        ) if member.user.username not in bots]

        total = members + owners

        # это так для pylance, а то бесит                   ^^^

        await utils.answer(
            message,
            f'📝 Информация о чате "{message.chat.title}"\n\n'
            f'Всего **{len(total)}** участников\n\n'
            '👨‍✈️ Администраторы: ' + ', '.join(owner for owner in owners) + '\n\n'
            '🧍‍♂️ Участники: ' + ', '.join(member for member in members)
        )