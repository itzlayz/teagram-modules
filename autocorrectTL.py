#          █░█ █▀█ ▀█▀ █▀▄ █▀█ █ █▀▀ █▄█
#          █▀█ █▄█ ░█░ █▄▀ █▀▄ █ █▀░ ░█░
#          🔒 Licensed under the GNU AGPLv3.
#                    @HotDrify

#         Rewrited to telethon version by itzlayz


from telethon import types
from .. import (
    loader, utils, validators)
from ..types import Config, ConfigValue

import requests

@loader.module(name="auto-correct-tl", author="itzlayz", version=1.1)
class AutoCorrectMod(loader.Module):
    """❤️ Автоматическое исправление текста."""
    def __init__(self):
        self.config = Config(
            ConfigValue(
                'api_base',
                'https://speller.yandex.net/services/spellservice.json/checkText',
                'https://speller.yandex.net/services/spellservice.json/checkText',
                validators.String(),
            ),
            ConfigValue(
                'is_slash',
                True,
                True,
                validators.Boolean(),
            ),
            ConfigValue(
                'is_link',
                True,
                True,
                validators.Boolean(),
            ),
            ConfigValue(
                'is_slash',
                True,
                True,
                validators.Boolean(),
            ),
            ConfigValue(
                'status',
                True,
                True,
                validators.Boolean(),
            ),
            ConfigValue(
                'lang',
                'ru',
                'ru',
                validators.String()
            )
        )
    
    @loader.on(lambda _, msg: msg.out)
    async def watcher(self, message: types.Message):
        if not self.config["status"]:
            return
        if self.config["is_ping"]:
            if "@" in message.text:
                return
        if self.config["is_slash"]:
            if "/" in message.text:
                return
        if self.config["is_link"]:
            if "https" in message.text or "http" in message.text:
                return
                
        response = await utils.run_sync(
            requests.get,
            self.config["api_base"],
            params = {
                'text': message.text,
                'lang': self.config["lang"],
                'options': 512
            }
        )
        
        data = response.json()
        ctext = message.text
        
        for mistake in data:
            ctext = ctext[:mistake['pos']] + mistake['s'][0] + ctext[mistake['pos']+mistake['len']:]
        
        if message.text != ctext:
            await utils.answer(message, ctext)