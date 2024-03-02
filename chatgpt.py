#                            ██╗████████╗███████╗██╗░░░░░░█████╗░██╗░░░██╗███████╗
#                            ██║╚══██╔══╝╚════██║██║░░░░░██╔══██╗╚██╗░██╔╝╚════██║
#                            ██║░░░██║░░░░░███╔═╝██║░░░░░███████║░╚████╔╝░░░███╔═╝
#                            ██║░░░██║░░░██╔══╝░░██║░░░░░██╔══██║░░╚██╔╝░░██╔══╝░░
#                            ██║░░░██║░░░███████╗███████╗██║░░██║░░░██║░░░███████╗
#                            ╚═╝░░░╚═╝░░░╚══════╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
#                                            https://t.me/itzlayz
#
#                                    🔒 Licensed under the GNU AGPLv3
#                                 https://www.gnu.org/licenses/agpl-3.0.html

# required: openai

import openai
from .. import loader, utils

class ChatGPTMod(loader.Module):
    strings = {
        "generating": "🤖 <b>Generating...</b>",
        "no_args": "❌ <b>No question</b>",
        "output": "🤖 <b>Your question: <code>{}</code></b>\n\n{}"
    }

    strings_ru = {
        "generating": "🤖 <b>Генерируем ответ...</b>",
        "no_args": "❌ <b>Вы не указали вопрос</b>",
        "output": "🤖 <b>Ваш запрос: <code>{}</code></b>\n\n{}"
    }

    def __init__(self):
        self.name = "ChatGPT"
        self.config = loader.ModuleConfig(
            "openai_key", None, "OpenAI key",
            "base_url", "https://api.openai.com/v1", "Base API url",
            "model", "gpt-3.5-turbo", "OpenAI model"
        )

    
    @loader.command()
    async def gpt(self, message, args: str = None):
        if not args:
            return await utils.answer(message, self.strings("no_args"))
        
        if not self.get("openai_key"):
            return await utils.answer(message, self.strings("no_key"))

        await utils.answer(message, self.strings("generating"))

        client = openai.AsyncOpenAI(api_key=self.get("openai_key"))
        response = await client.chat.completions.create(
            model=self.get("model"),
            messages=[{"role": "user", "content": args}]
        )

        response = response.choices[0].message.content
        await utils.answer(message, self.strings("output").format(args, response))