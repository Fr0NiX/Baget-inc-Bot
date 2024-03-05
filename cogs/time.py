import disnake
from disnake.ext import commands
from datetime import datetime
from pytz import timezone

class TimeInCountryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="time", description="Получить настроящее время персонала")
    async def getTime(self, ctx):
        # Список пользователей и их таймзоны
        user_timezone = {
            "ikdan": "Europe/Moscow",
            "malix": "Europe/Moscow",
            "Baget35": "Europe/Tallinn",
            "PM-Kirill": "Europe/Moscow"
        }

        # Создаем эмбед
        embed = disnake.Embed(title="Время пользователей", color=disnake.Color.blue())

        for user, tz in user_timezone.items():
            # Получаем текущее время пользователя
            user_time = datetime.now(tz=timezone(tz))

            # Добавляем поле в эмбед для каждого пользователя
            embed.add_field(name=user, value=user_time.strftime('Дата: %Y-%m-%d Время: %H:%M:%S'), inline=False)

        # Отправляем эмбед
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TimeInCountryCog(bot))
    print("[Time] готов")