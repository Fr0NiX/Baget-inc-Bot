import io
import disnake
from disnake.ext import commands
from disnake import Option, OptionType
from disnake.ext.commands import has_permissions

class PromoTariffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="tariff",
        description='Создает промо-тариф'
    )
    @has_permissions(administrator=True)
    async def promo_tariff(self, ctx, memory: str, cpu: str, ssd: str, money: str, channel: disnake.TextChannel):
        embed = disnake.Embed(
            title='🎉 Промо-тариф 🎉', 
            description='🎁 Ниже представлены характеристики текущего промо-тарифа. 🎁', 
            color=disnake.Color.orange()
        )
        embed.add_field(name='🔥 ОЗУ 🔥:', value=f"{memory}GB", inline=False)
        embed.add_field(name='🚀 CPU: 🚀', value=f'{cpu}%', inline=False)
        embed.add_field(name='💽 SSD 💽:', value=f'{ssd}GB', inline=False)
        embed.add_field(name='💸 Цена 💸:', value=f'{money}₽', inline=False)
        embed.add_field(name='⏰ Акция!', value='Покупка доступна только 2 дня! Количество покупок ограничено!', inline=False)
        embed.set_footer(text='👇 За покупкой в /report 👇\n✨ Тариф можно разделить на несколько контейнеров под разные задачи ✨')
        
        await channel.send("<@&1099335173058854913>", embed=embed)


def setup(bot):
    bot.add_cog(PromoTariffCog(bot))
    print("[Tariff] готов")
