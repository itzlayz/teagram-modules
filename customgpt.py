from .. import utils, loader, validators
from ..types import Config, ConfigValue

import openai
import asyncio
import requests
from random import choice

# required: openai

@loader.module('customgpt', 'itzlayz', 1)
class CustomGPTMod(loader.Module):
    def __init__(self):
        self.config = Config(
            ConfigValue(
                option='apikey',
                docstring='OpenAI key',
                default='',
                value=self.db.get('customgpt', 'apikey', ''),
                validator=validators.String()
            ),
            ConfigValue(
                option='apibase',
                docstring='Api base',
                default='https://api.openai.com/v1',
                value=self.db.get('customgpt', 'apibase', 'https://api.openai.com/v1'),
                validator=validators.String()
            ),
            ConfigValue(
                option='model',
                docstring='Api model',
                default='gpt-3.5-turbo',
                value=self.db.get('customgpt', 'model', 'gpt-3.5-turbo'),
                validator=validators.String()
            ),
            ConfigValue(
                option='prodiakey',
                docstring='Prodia Api key',
                default='',
                value=self.db.get('customgpt', 'prodiakey', ''),
                validator=validators.String()
            )
            ,
            ConfigValue(
                option='prodiamodel',
                docstring='Prodia Api model',
                default='',
                value=self.db.get('customgpt', 'prodiamodel', ''),
                validator=validators.String()
            )
        )

    @loader.command('Generate prompt')
    async def aicmd(self, message, args):
        if not (prompt := args):
            return await utils.answer(
                message,
                '❌ <b>Ошибка, вы не указали промпт</b>'
            )
        
        if not self.config['apikey']:
            return await utils.answer(
                message,
                '❌ <b>Ошибка, вы не указали ключ</b>'
            )
        
        await utils.answer(
            message,
            '🤖 <b>Генерация...</b>'
        )

        try:
            openai.api_base = self.config['apibase']
            openai.api_key = self.config['apikey']
            owner = self.manager.me.username
            
            answer = await openai.ChatCompletion.acreate(
                model=self.config['model'], 
                messages=[
                    {'role': 'system', 'content': f"You are in userbot Teagram, your owner is {owner}"},
                    {"role": "user", "content": prompt}
                ]
            )

            await utils.answer(
                message,
                f'🤖 <b>{self.config["model"]}</b>\n\n'
                f'<code>{answer.choices[0].message.content}</code>'
            )
        except Exception as error:
            await utils.answer(
                message,
                f'❌ Ошибка: {error}'
            )
    
    @loader.command('Generate prompt')
    async def image(self, message, args):
        if not (prompt := args):
            return await utils.answer(
                message,
                '❌ <b>Ошибка, вы не указали промпт</b>'
            )
        
        if not self.config['apikey']:
            return await utils.answer(
                message,
                '❌ <b>Ошибка, вы не указали ключ</b>'
            )
        
        await utils.answer(
            message,
            '🤖 <b>Генерация...</b>'
        )

        try:
            openai.api_base = self.config['apibase']
            openai.api_key = self.config['apikey']
            
            answer = await openai.Image.acreate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image = answer['data'][0]['url']

            await utils.answer(
                message,
                image,
                True,
                f'🤖 Генерация картинки\n'
                f'<code>{prompt}</code>'
            )
        except Exception as error:
            await utils.answer(
                message,
                f'❌ Ошибка: {error}'
            )

    @loader.command()
    async def prodia(self, message, args):
        await utils.answer(message, 'Генерирую')
        
        key = self.config['prodiakey']
        url = "https://api.prodia.com/v1/sd/generate"
        models = [
            "anythingv3_0-pruned.ckpt [2700c435]",
            "anything-v4.5-pruned.ckpt [65745d25]",
            "anythingV5_PrtRE.safetensors [893e49b9]",
            "dreamlike-anime-1.0.safetensors [4520e090]",
            "dreamlike-diffusion-1.0.safetensors [5c9fd6e0]",
            "dreamlike-photoreal-2.0.safetensors [fdcf65e7]",
            "dreamshaper_6BakedVae.safetensors [114c8abb]",
            "dreamshaper_7.safetensors [5cf5ae06]",
            "dreamshaper_8.safetensors [9d40847d]",
            "openjourney_V4.ckpt [ca2f377f]",
            "Realistic_Vision_V1.4-pruned-fp16.safetensors [8d21810b]",
            "Realistic_Vision_V2.0.safetensors [79587710]",
            "Realistic_Vision_V4.0.safetensors [29a7afaa]",
            "Realistic_Vision_V5.0.safetensors [614d1063]"
            ]
        
        if self.config['prodiamodel'] and self.config['prodiamodel'] not in models:
            return await utils.answer(
                message,
                '❌ Вы указали неправильную модель, список: ' + '\n'.join(model for model in models)
            )
        
        payload = {
            "model": self.config['prodiamodel'] or choice(models),
            "prompt": args,
            "negative_prompt": "badly drawn",
            "steps": 30,
            "cfg_scale": 7,
            "seed": -1,
            "upscale": False,
            "sampler": "DPM++ 2S a Karras",
            "aspect_ratio": "square"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": key
        }

        try:
            url = (await utils.run_sync(requests.post, url, json=payload, headers=headers)).json()
            url = (await utils.run_sync(
                    requests.get,
                    f"https://api.prodia.com/v1/job/{url.get('job')}", 
                    headers=headers)
                ).json()
            
            while (
                url.get('status') == 'generating'
            ):
                
                await asyncio.sleep(0.5)
                url = (await utils.run_sync(
                    requests.get,
                    f"https://api.prodia.com/v1/job/{url.get('job')}", 
                    headers=headers)
                ).json()
        except Exception as error:
            return await utils.answer(
                message,
                '❌ ' + error
            )

        cfgs = ''
        for k, v in payload.items():
            if k == 'prompt':
                continue

            cfgs += f'<i>{k}</i>: <code>{v}</code>\n'

        await utils.answer(
            message,
            url['imageUrl'],
            True,
            caption=f"""
🎉 <b>Ваше изображение готово!</b>
<b>Запрос</b>: <code>{args}</code>

""" + cfgs
        )