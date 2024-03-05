import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from disnake.ui import Modal, TextInput, View
import json
from disnake.interactions.modal import ModalInteraction

file_name = 'counter.json'

report_counts = {}

def load_counter_from_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_counter_to_json(file_name, counter_value):
    with open(file_name, 'w') as file:
        json.dump(counter_value, file)

def increment_counter(file_name):
    counter_value = load_counter_from_json(file_name)
    if counter_value is None:
        counter_value = 1
    else:
        counter_value += 1
    
    save_counter_to_json(file_name, counter_value)
    global report_counts
    report_counts[file_name] = counter_value
    return counter_value

# Путь к файлу JSON
file_name = 'counter.json'

# Считываем значение счетчика при старте программы
counter = load_counter_from_json(file_name)

channel_id_report = []
channel_id = 1172874906690666587

class Modal(disnake.ui.Modal):
    def __init__(self):
        self.channel_topic = "48567023564502364536374"
        components = [
            disnake.ui.TextInput(label="Тема открытия репорта?", placeholder="Тема открытия репорта?", custom_id="tema"),
            disnake.ui.TextInput(label="Подробное описание нарушения?", placeholder="Подробное описание нарушения?", custom_id="podrobnoe")
        ]
        super().__init__(title="Создание репорта!", components=components, custom_id="a", timeout=10)

    async def callback(self, interaction: ModalInteraction) -> None:      
        user_id = interaction.user.id
        
        global counter
        if user_id in report_counts:
            counter = increment_counter(file_name)
        else:
            report_counts[user_id] = 1
        
        a = interaction.text_values["tema"]
        b = interaction.text_values["podrobnoe"]
        embed = disnake.Embed(
            title="Репорт создан",
            description=f"",
            color=disnake.Color.purple()
        )     
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print('сообщение отправленно загружен')
        
        guild = interaction.guild
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(read_messages=False),  # Отключение доступа для всех ролей по умолчанию
            guild.me: disnake.PermissionOverwrite(read_messages=True),  # Разрешение доступа для бота
            interaction.user: disnake.PermissionOverwrite(read_messages=True)  # Разрешение доступа для пользователя, заполнившего модальное окно
        }
        if guild.me.guild_permissions.manage_channels:
            channel = await guild.create_text_channel(f'report {counter}', overwrites=overwrites, topic=self.channel_topic)
        else:
            print("Бот не имеет разрешения на создание каналов")
        await channel.send(f"Здравствуйте, вы открыли репорт. Опишите подробно что у вас произошло? После обьяснения пингуйте модератора. Тема открытия репорта: {a}, подробное описания: {b}")
        channel_id_report = channel.id

class ViewButton(disnake.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @disnake.ui.button(label='Создать репорт', style=disnake.ButtonStyle.grey)
    async def approve(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        modal = Modal()
        await interaction.response.send_modal(modal=modal) 

class CloseReportModal(disnake.ui.Modal):
    def __init__(self, user, channel):
        self.user = user
        self.channel = channel  # Теперь канал будет передаваться через конструктор
        components = [
                disnake.ui.TextInput(label="Причина закрытия", placeholder="Введите причину...", custom_id="reason")
        ]
        super().__init__(title="Закрытие Репорта", components=components, custom_id="custom_id_for_modal")

    async def callback(self, interaction: disnake.Interaction):  # Параметр channel был удален, так как не нужен тут
        reason = interaction.text_values['reason']  # Получаем причину закрытия из введенного текста в модальном окне
        await self.channel.delete(reason=reason)  # И используем переменную reason для указания причины
        await self.user.send(f'Ваш репорт был закрыт по причине: {reason}')

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='report', description="Написать в репорт")
    async def report(self, ctx):
        view = ViewButton()  # Убедитесь, что ViewButton определен как класс с кнопками
        embed = disnake.Embed(
            title="Открытие репорт",
            description=f"Нажмите кнопку что бы открыть репорт",
            color=disnake.Color.purple()
        ) 
        await ctx.send(embed=embed, view=view) 
        
    @commands.slash_command(name="close")
    @commands.has_permissions(administrator=True)  # Проверка на права администратора
    async def close_report(self, interaction: ApplicationCommandInteraction, member: disnake.Member):
        channel = interaction.channel # получаем объект канала
        description = channel.topic # получаем описание канала (тему)
        if description == "48567023564502364536374":
            modal = CloseReportModal(user=member, channel=channel)  # Передаем канал в модалку
            await interaction.response.send_modal(modal)  # Открываем модалку для админа
        else:
            await ctx.send("Этот канал не является репортом")

                   

def setup(bot):
    bot.add_cog(Report(bot))
    print("[Report] готов")