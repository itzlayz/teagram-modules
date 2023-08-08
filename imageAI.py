import asyncio
import random
import aiohttp

from pyrogram import Client, types

from .. import __version__, loader, utils

async def create_image(prompt: str, key: str) -> dict:
    url = "https://api.prodia.com/v1/job"
    models = [
        'anything-v4.5-pruned.ckpt [65745d25]',
        'Realistic_Vision_V2.0.safetensors [79587710]',
        'openjourney_V4.ckpt [ca2f377f]'
    ]

    model = random.choice(models)
    payload = {
        "prompt": prompt,
        "model": model,
        "sampler": "DPM++ 2M Karras",
        "upscale": False,
        "aspect_ratio": "portrait",
        "steps": 30,
        "seed": random.randint(-1, 9999999)
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": key
    }
    try:
        tries = 60
        async with aiohttp.ClientSession() as ses:
            async with ses.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                jobid = data['job'].strip()

                while tries > 0:
                    tries -= 1

                    async with ses.get(f'{url}/{jobid}', headers=headers) as response:
                        data = await response.json()
                        if data['status'] == 'succeeded':
                            return {
                                'status': 'succeeded',
                                'model': model,
                                'data': data
                            }

                    await asyncio.sleep(1)

                return {
                    'status': 'error',
                    'error': 'Превышено время ожидания'
                }
    except Exception as error:
        return {
                'status': 'error',
                'error': error
            }

@loader.module(name="ImageAI", author='itzlayz', version=1.1)
class ImageAIMod(loader.Module):
    """Сгенерируйте любое фото с помощью AI"""
   
    async def generateImage_cmd(self, app: Client, message: types.Message, args: str):
        key = self.db.get('imageai', 'key')

        if not key:
            return await utils.answer(
                message,
                'Ошибка, у вас нету апи ключа.\nЧтобы получить ключ зайдите на `https://app.prodia.com/api`'
            )
        
        image = await create_image(args, key)
        await utils.answer(message, 'Генерация...')

        if image['status'] == 'succeeded':
            await utils.answer(
                message,
                f"Запрос: {args}\nМодель: {image['model']}\nФото: {image['data']['imageUrl']}"
            )
        else:
            await utils.answer(
                message,
                f'Ошибка: {image["error"]}'
            )
    
    async def setKey_cmd(self, app: Client, message: types.Message, args: str):
        if not args:
            return await utils.answer(
                message,
                'Ошибка, вы не указали ключ\nЧтобы получить ключ зайдите на `https://app.prodia.com/api`'
            )

        self.db.set('imageai', 'key', args.split()[0])

        await utils.answer(message, 'Ключ успешно поставлен')
