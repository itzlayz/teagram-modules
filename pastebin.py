import aiohttp
import requests

from telethon import types
from .. import loader, utils

# required: aiohttp

@loader.module('Pastebin API', 'itzlayz', 1.1)
class PastebinMod(loader.Module):
    """Взаимодействуйте с Pastebin API в teagram"""

    async def pastesave_cmd(self, message: types.Message, args: str):
        """Записать код/текст на pastebin"""
        text = None

        if not args and not (text := message.reply_to_message.text):
            return await utils.answer(
                message,
                '❌ Вы не указали текст (Вы можете сделать реплай)'
            )

        if not (key := self.db.get('pastebin', 'key')):
            return await utils.answer(
                message, 
                '❌ Ключ не найден'
            )
        
        if not text:
            text = args
        
        async with aiohttp.ClientSession() as Session:
            async with Session.post(
                url='https://pastebin.com/api/api_post.php',
                data={
                    'api_dev_key': key,
                    'api_paste_code': text,
                    'api_option': 'paste'
                }) as response:

                response_text = await response.text()

                await utils.answer(
                    message,
                    f'❔ Статус **{response.status}**\n✈ Ответ API: <code>{response_text}</code>'
                )
    
    async def pasteread_cmd(self, message: types.Message, args: str):
        """Прочитать содержимое pastebin-ссылки"""

        if not (url := args.split('/')[-1]):
            return await utils.answer(
                message,
                '❌ Вы не указали ссылку'
            )
        
        url = f'https://pastebin.com/raw/{url}'
        response = await utils.run_sync(requests.get, url)
        text = response.content.decode()

        if 'not found' in text.lower():
            text = '❌ Страница не найдена'

        await utils.answer(
            message,
            f'❔ Статус **{response.status_code}**\n✈ Текст:\n\n<code>{text}</code>'
        )

    
    async def pastekey_cmd(self, message: types.Message, args: str):
        """Установить api-key (`https://pastebin.com/doc_api#1`)"""
        if not (key := args.split(maxsplit=1)[0]):
            return await utils.answer(
                message,
                'Вы не указали ключ'
            )
        
        self.db.set('pastebin', 'key', key)

        await utils.answer(
            message,
            'Вы успешно установили ключ Pastebin API'
        )
