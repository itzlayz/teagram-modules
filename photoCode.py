import requests
import io

from .. import utils, loader
from telethon import types

@loader.module('PhotoCode', 'itzlayz', 1.1)
class PhotoCodeMod(loader.Module):
    """Данный модуль превратит код в картинку"""

    @loader.command()
    async def makephoto(self, message: types.Message, args: str):
        """Сделать картинку"""
        if not args:
            if not (args := (await message.get_reply_message())):
                return await utils.answer(
                    message, 
                    '❌ Вы не указали текст или реплай с текстом'
                )

        text = args.text.rstrip('`').lstrip('`')

        params = 'theme=vsc-dark-plus&language=python&line-numbers=true&background-color=gray'
        url = 'https://code2img.vercel.app/api/to-image?' + params
        
        await utils.answer(
            message,
            '🕒 Подождите...'
        )

        photo = io.BytesIO(
            (
                await utils.run_sync(
                    requests.post, # type: ignore
                    url,
                    headers={"content-type": "text/plain"},
                    data=bytes(text, "utf-8"),
                )
            ).content
        )
        photo.name = "photo.jpg"
        
        await utils.answer(
            message,
            photo,
            photo=True
        )
