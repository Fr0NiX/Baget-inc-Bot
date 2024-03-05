import disnake
from disnake.ext import commands
from datetime import datetime
from pytz import timezone

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="embed", description="Получить настроящее время персонала")
    async def rewards_embed(ctx):
        embed = disnake.Embed(title="🌟 Награды за Приглашения! 🌟", description="Приглашай друзей и получи классные бонусы!", color=disnake.Colour.gold())
        rewards = {
            10: {'ram': '+3 ГБ ОЗУ', 'cpu': '+30% CPU', 'ssd': '+2 ГБ SSD'},
            20: {'ram': '+6 ГБ ОЗУ', 'cpu': '+80% CPU', 'ssd': '+4 ГБ SSD'},
            30: {'ram': '+10 ГБ ОЗУ', 'cpu': '+120% CPU', 'ssd': '+6 ГБ SSD'},
            40: {'ram': '+16 ГБ ОЗУ', 'cpu': '+160% CPU', 'ssd': '+8 ГБ SSD'},
            50: {'ram': '+20 ГБ ОЗУ', 'cpu': '+200% CPU', 'ssd': '+10 ГБ SSD'}
        }
    
        for invites, reward in rewards.items():
            embed.add_field(
                name=f"🎫 {invites} инвайтов:",
                value=f"🔸 ОЗУ: {reward['ram']}\n"
                      f"🔸 CPU: {reward['cpu']}\n"
                      f"🔸 SSD: {reward['ssd']}",
                inline=False
            )

        embed.add_field(
            name="📜 Условия и информация:",
            value="Награды автоматически выдаются при достижении указанного количества приглашений. Учтите, что приглашения должны быть действительными и уникальными, боты и фейковые аккаунты не учитываются.",
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Embed(bot))
    print("[Embed] готов")