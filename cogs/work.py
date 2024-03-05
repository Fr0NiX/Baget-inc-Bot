import disnake
from disnake.ext import commands

from disnake.ui import Modal
from disnake.interactions.modal import ModalInteraction

channel_id = 1189226210945945722
role_id = 1189214441221406740

class Button1(disnake.ui.View):
    def __init__(self, user_id, message=None):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.message = message
        self.moderator_id = None  # ID модератора, который взял заявку в обработку
        self.owner = '806151791146041344'
        self.allowed_role_id = '1189296785957601360'
        
    @disnake.ui.button(label='На рассмотрение', style=disnake.ButtonStyle.blurple)
    async def consider(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer()
        role = disnake.utils.get(interaction.guild.roles, id='1189296785957601360')
        self.moderator_id = interaction.user.id
        self.status = "На рассмотрении"
        embed = self.message.embeds[0]
        embed.description = (embed.description or "") + "\n\nСтатус: На рассмотрении"
        view = ViewButton(interaction.user.id, message=self.message)
        await interaction.edit_original_message(embed=embed, view=view)

class ViewButton(disnake.ui.View):
    def __init__(self, user_id, message):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.message = message

    @disnake.ui.button(label='Принять', style=disnake.ButtonStyle.green)
    async def approve(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user.id != self.user_id:
            return  # проверка, чтобы кнопки мог использовать только пользователь который создал заявку
        
        await interaction.response.defer()
        guild = interaction.guild
        member = guild.get_member(self.user_id)
        role = guild.get_role(role_id)
        await member.add_roles(role)
        original_embed = interaction.message.embeds[0]

        # Обновляем описание (или другое поле, которое содержит статус)
        original_embed.description = original_embed.description.replace('Статус: На рассмотрении', '')

        # Добавляем информацию о новом статусе
        original_embed.add_field(name="Статус", value="Принято")

        # Отправляем обновленный embed обратно в канал
        await interaction.edit_original_message(embed=original_embed, view=None)


    @disnake.ui.button(label='Отклонить', style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user.id != self.user_id:
            return  # проверка, чтобы кнопки мог использовать только пользователь который создал заявку
        
        await interaction.response.defer()
        embed = self.message.embeds[0]
        embed.description = (embed.description or "") + "\n\nСтатус: ❌ Отказано!"
        await interaction.edit_original_message(embed=embed, view=None)
        await interaction.response.defer()

class Modal2(disnake.ui.Modal):
    def __init__(self, user_id):
        components = [
            disnake.ui.TextInput(label="Ваше имя?", placeholder="Введите ваше имя", custom_id="name"),
            disnake.ui.TextInput(label="Ваш возраст?", placeholder="Введите ваш возраст", custom_id="age"),
            disnake.ui.TextInput(label="На какую работу идёте?", placeholder="Опишите желаемую работу", custom_id="job"),
            disnake.ui.TextInput(label="Знания русского языка (от 1 до 10)", placeholder="Оцените свои знания", custom_id="russian"),
            disnake.ui.TextInput(label="Знания английского языка (от 1 до 10)", placeholder="Оцените свои знания", custom_id="english"),
        ]
        super().__init__(title="Заявка на работу", components=components, custom_id="a")
        self.user_id = user_id

    async def callback(self, interaction: ModalInteraction) -> None:
        a = interaction.text_values["name"]
        b = interaction.text_values["age"]
        c = interaction.text_values["job"]
        d = interaction.text_values["russian"]
        e = interaction.text_values["english"]
        
        member = interaction.guild.get_member(self.user_id)
        user_name = member.display_name  # Это имя пользователя на сервере
        user_tag = str(member)  # Это имя пользователя с тэгом, например User#1234
        user_mention = member.mention

        embed = disnake.Embed(
            title="Заявка на работу",
            description="",
            color=disnake.Color.purple()
        )
        embed.add_field(name="👤 Имя", value=f"{a}", inline=False)
        embed.add_field(name="🎂 Возраст", value=f"{b}", inline=False)
        embed.add_field(name="💼 Желаемая работа", value=f"{c}", inline=False)
        embed.add_field(name="🇷🇺 Знание русского", value=f"{d}/10", inline=False)
        embed.add_field(name="🌏 Знание английского", value=f"{e}/10", inline=False)
        embed.add_field(name="👦/ 👩 Пользователь:", value=f"{user_mention}", inline=False)
        
        channel = interaction.guild.get_channel(channel_id)

        # Важно: создаем Button1 и ViewButton в этом методе до отдачи message
        view1 = Button1(interaction.user.id)
        # view нужно создать, но не использовать здесь
        # view = ViewButton(interaction.user.id)
        
        # Убираем view из send
        message = await channel.send(embed=embed, view=view1)
        
        # Присваиваем message только к view1
        view1.message = message  # Вот здесь вы должны назначить сообщение

        # Отвечаем пользователю, что заявка получена
        await interaction.response.send_message("Спасибо за заявку!", ephemeral=True)

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='work', description='Подача заявки на работу')
    async def work(self, interaction: disnake.ApplicationCommandInteraction):
        # Получаем user_id вызывающего пользователя
        user_id = interaction.user.id
        # Создаем экземпляр модального окна, передавая user_id как аргумент
        modal = Modal2(user_id)
        # Отправляем модальное окно пользователю
        await interaction.response.send_modal(modal)

def setup(bot):
    bot.add_cog(Join(bot))
    print("[Work] готов")