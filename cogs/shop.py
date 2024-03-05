import disnake
from disnake.ext import commands

# Создаём ког
class ShoppingCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.channel_to_send_purchase_info = 1195792921379753994  # ID канала, куда отправляется информация после подтверждения покупки
        self.tariff_prices = {'base': '500 руб.', 'premium': '1500 руб.'}  # Примерная стоимость тарифов

    @commands.slash_command()
    async def buy(
        self,
        inter: disnake.ApplicationCommandInteraction,
        email: str,
        tariff: str
    ):
        await inter.response.defer()
        # Права доступа для канала
        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            inter.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        # Создание канала
        channel = await inter.guild.create_text_channel(name=f"purchase-{inter.author.name}", overwrites=overwrites)
    
        # Сохранение данных о покупке
        self.bot.purchase_channels[channel.id] = {'email': email, 'tariff': tariff, 'member_id': inter.author.id}

        # Создание эмбеда с информацией о покупке
        embed = disnake.Embed(
            title=f"Создана заявка на оплату тарифа: {tariff}",
            description=f"**Сумма**: {self.tariff_prices[tariff]}",
            color=disnake.Color.green()
        )

        # Отправка эмбеда в созданный канал
        await channel.send(embed=embed)

        # Подтверждение создания канала и отправки эмбеда автору команды
        await inter.edit_original_message(content=f"Канал {channel.mention} для оформления покупки создан. 🌟")

    @commands.slash_command(
        name='confirm_purchase',
        description='Подтверждение покупки и удаление канала.'
    )
    async def confirm_purchase(self, inter: disnake.ApplicationCommandInteraction):
        channel_id = inter.channel_id
        if channel_id not in self.bot.purchase_channels:
            await inter.response.send_message("Этот канал не предназначен для подтверждения покупок.", ephemeral=True)
            return
        
        purchase_info = self.bot.purchase_channels[channel_id]
        channel_to_send = self.bot.get_channel(self.channel_to_send_purchase_info)
        purchase_message = f"Пользователь {inter.author.name} подтвердил покупку!\nEmail: {purchase_info['email']}\nТариф: {purchase_info['tariff']}"
        
        await channel_to_send.send(purchase_message)
        await inter.channel.delete()
        del self.bot.purchase_channels[channel_id]
        
        await inter.response.send_message("Покупка подтверждена и канал удалён.", ephemeral=True)


def setup(bot):
    bot.add_cog(ShoppingCog(bot))
    if not hasattr(bot, 'purchase_channels'):
        bot.purchase_channels = {}

    @commands.slash_command(
        name='confirm_purchase',
        description='Подтверждение покупки и удаление канала.'
    )
    async def confirm_purchase(self, inter: disnake.ApplicationCommandInteraction):
        channel_id = inter.channel_id
        if channel_id not in self.bot.purchase_channels:
            await inter.response.send_message("Этот канал не предназначен для подтверждения покупок.", ephemeral=True)
            return
        
        purchase_info = self.bot.purchase_channels[channel_id]
        channel_to_send = self.bot.get_channel(self.channel_to_send_purchase_info)
        purchase_message = f"Пользователь {inter.author.mention} подтвердил покупку!\nEmail: {purchase_info['email']}\nТариф: {purchase_info['tariff']}"
        
        await channel_to_send.send(purchase_message)
        await inter.channel.delete()
        del self.bot.purchase_channels[channel_id]
        
        await inter.response.send_message("Покупка подтверждена и канал удалён.", ephemeral=True)


def setup(bot):
    bot.add_cog(ShoppingCog(bot))
    print("[Shop] готов")
    if not hasattr(bot, 'purchase_channels'):
        bot.purchase_channels = {}