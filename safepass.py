import re
import string
import random

from pyrogram import Client, types
from .. import loader, utils

@loader.module(name="SafePass")
class SafePassMod(loader.Module):
    """Модуль для безопасности паролей"""

    async def criteria_cmd(self, app: Client, message: types.Message, args: str):
        if not (password := args):
            return await utils.answer(message, 'Вы не указали пароль')

        criteria = [
            len(password) >= 8,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'\W', password))
        ]
    
        await utils.answer(message, f'Оценка пароля {sum(criteria)}/5')

    async def bestpass_cmd(self, app: Client, message: types.Message, args: str):
        try:
            length = int(args)
        except ValueError:
            return await utils.answer(message, 'Вы не указали длину пароля или указали некоректный тип (Пример: .bestpass 8)')
            
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))

        criteria = [
            len(password) >= 8,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'\W', password))
        ]
    
        await utils.answer(message, f'Пароль - {password}\nОценка пароля {sum(criteria)}/5')
