import logging
import requests
import json

from .. import utils, loader

@loader.module('fakedata', 'itzlayz', 1.0)
class FakedataMod(loader.Module):
    """Генерирует рандомные данные"""

    def __init__(self):
        self.base = 'https://random-data-api.com/api/v2/'

    @loader.command()
    async def rnduser(self, message):
        data = json.loads((await utils.run_sync(requests.get, self.base+'/users')).text)
        text = ""

        for k, v in data.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    text += f"<b>{kk}</b> - <code>{vv}</code>\n"

                continue

            text += f"<b>{k}</b> - <code>{v}</code>\n"

        await utils.answer(
            message,
            f'👤 Рандомные данные о человеке\n' + text
        )

    @loader.command()
    async def rndaddress(self, message):
        data = json.loads((await utils.run_sync(requests.get, self.base + '/addresses')).text)
        text = ""

        for k, v in data.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    text += f"<b>{kk}</b> - <code>{vv}</code>\n"

                continue

            text += f"<b>{k}</b> - <code>{v}</code>\n"

        await utils.answer(
            message,
            f'🏚 Рандомный адрес\n' + text
        )

    @loader.command()
    async def rndcard(self, message):
        data = json.loads((await utils.run_sync(requests.get, self.base + '/credit_cards')).text)
        text = ""

        for k, v in data.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    text += f"<b>{kk}</b> - <code>{vv}</code>\n"

                continue

            text += f"<b>{k}</b> - <code>{v}</code>\n"

        await utils.answer(
            message,
            f'💳 Рандомная кредитная карта\n' + text
        )