import requests
import disnake
from disnake.ext import commands

class ImageProcessCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):  # Check if bot is mentioned
            image_url = None  # default value

            if message.attachments:
                for attachment in message.attachments:
                    image_url = attachment.url

            url = 'https://www.llama2.ai/api'
            headers = {
            }

            data = {
                "prompt": f"[INST] {message.content} [/INST]\n",
                "version": "c6ad29583c0b29dbd42facb4a474a0462c15041b78b1ad70952ea46b5e249591",
                "systemPrompt": "Speak only Russia lang",
                "temperature": 0.75,
                "topP": 0.9,
                "maxTokens": 800,
                "image": image_url,
                "audio": None
            }

            response = requests.post(url, headers=headers, json=data)
            if len(response.text) > 2000:  # Проверка длины сообщения
                # Сохраняем сообщение в строку
                message_content = response.text
                # Преобразуем строку в байтовый поток
                message_bytes = io.BytesIO(message_content.encode('utf-8'))
                # Создаем файловый объект с названием 'message.txt', содержащий сообщение
                file = disnake.File(message_bytes, filename="message.txt")
                # Отправляем файл в тот же канал
                await message.channel.send(file=file)
            else:
                await message.channel.send(response.text)
def setup(bot):
    bot.add_cog(ImageProcessCog(bot))
    print("[BagetGPT_LLaVA] готов")