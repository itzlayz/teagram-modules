import requests
import io

from .. import utils, loader, validators
from ..types import ConfigValue, Config

from telethon import types

@loader.module('PhotoCode', 'itzlayz', 2.0)
class PhotoCodeMod(loader.Module):
    """Данный модуль превратит код в картинку"""
    def __init__(self):
        self.config = Config(
            ConfigValue(
                'image',
                'Background image url',
                'https://images.hdqwalls.com/download/minimalist-mountains-landscape-scenery-n4-1920x1080.jpg',
                self.db.get('PhotoCode', 'image', None),
                validators.String()
            )
        )

    @loader.command()
    async def makephoto(self, message: types.Message, args: str):
        """Сделать картинку"""
        if not args:
            if not (reply := (await message.get_reply_message())):
                return await utils.answer(
                    message, 
                    '❌ <b>Вы не указали текст или реплай с текстом</b>'
                )

        text = args.rstrip('`').lstrip('`') or reply.text.rstrip('`').lstrip('`')

        params = f'theme=vsc-dark-plus' +\
            f'&language=python&line-numbers=true' + (
                f'&background-image={self.config["image"]}' 
                if self.config['image']
                else '&background-color=gray'
            )
        
        url = 'https://code2img.vercel.app/api/to-image?' + params
        
        await utils.answer(
            message,
            '🕒 <b>Подождите...</b>'
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
