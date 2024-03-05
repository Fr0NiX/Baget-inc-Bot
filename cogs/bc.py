import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Embed, TextChannel
from disnake.ext.commands import has_permissions

class BroadcastCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="broadcast",
        description="Создает эмбед сообщение на основе предоставленных данных и отправляет в указанный канал"
    )
    @has_permissions(administrator=True)
    async def broadcast(
        self,
        inter: ApplicationCommandInteraction,
        channel: TextChannel,
        color: str = commands.Param(description="Введите HEX код цвета", default=None),
        title: str = commands.Param(description="Введите заголовок", default=None),
        text: str = commands.Param(description="Введите текст эмбеда", default=None),
        footer: str = commands.Param(description="Введите маленький текст для угла", default=None)
    ):
        # Проверка валидности HEX цвета (должен начинаться с # и содержать 6 символов)
        if color and not (color.startswith('#') and len(color) == 7):
            await inter.response.send_message("Цвет должен быть в HEX формате, например #FFFFFF.", ephemeral=True)
            return
        
        # Преобразование строки HEX цвета в число
        color_value = int(color[1:], 16) if color else Embed.Empty

        # Создание эмбед с параметрами, полученными из команд
        embed = Embed(
            title=title or Embed.Empty,
            description=text or Embed.Empty,
            color=color_value or Embed.Empty
        )

        # Установка footer, если он передан
        if footer:
            embed.set_footer(text=footer)

        # Отправка эмбед в указанный канал
        await channel.send("<@&1099335173058854913>", embed=embed)
        # Ответ в канале, где была использована команда
        await inter.response.send_message(f"Уведомление отправлено в канал {channel.mention}.", ephemeral=True)

def setup(bot):
    bot.add_cog(BroadcastCog(bot))
    print("[BroadCast] готов")