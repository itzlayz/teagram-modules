# TELETHON VERSION
# REWRITED FROM https://raw.githubusercontent.com/HotDrify/tea-modules/main/filters.py

import json
import logging
import asyncio
from telethon import types
from .. import (
    loader, utils, validators)
from ..types import Config, ConfigValue


@loader.module(name="Filters", author="itzlayz")
class FiltersMod(loader.Module):
  """импортированы фильтры из известного юзербота FTG"""
  def __init__(self):
    self.config = Config(
        ConfigValue(
            'waitTime',
            0.0,
            0.0,
            validators.Integer(minimum=0.0, maximum=10.0)
        )
    )

    @loader.command()
    async def addfcmd(self, message: types.Message, args: str):
        """добавить фильтр"""
        filters = self.db.get("Filters", "filters", {})
        data = json.loads(str(filters))
        if not message.reply_to_message:
            return await utils.answer(message, "🚫 Нету реплая на сообщение.")
        if message.reply_to_message.text in filters:
            return await utils.answer(message, "🚫 Фильтр уже есть.")
        if not args:
            return await utils.answer(message, "🚫 Нету агрументов!")
        data[str(message.chat.id)] = {args: message.reply_to_message.text}
        upd = json.dumps(data)
        self.db.set("Filters", "filters", upd)
        await utils.answer(message, f"✅ Фильтр <b>{args}</b> сохранен.")

    @loader.command()
    async def stopall(self, message: types.Message, args: str):
        """остановить фильтры"""
        filters = self.db.get("Filters", "filters", {})
        if message.chat.id not in filters:
            return await utils.answer(message, "🚫 Нету в фильтрах!")
        if not args:
            return await utils.answer(message, "🚫 Нужны аргументы!")
        del data[message.chat.id]
        upd = json.dumps(data)
        self.db.set("Filters", "filters", upd)
        await utils.answer(message, f"✅ Фильтры чата удалены")

    async def watcher(self, message: types.Message):
        filters = self.db.get("Filters", "filters", {})
        if str(message.chat.id) in filters:
            if message.text in filters:
                await message.reply(filters[message.chat.id][message.text])
    
