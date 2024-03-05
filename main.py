import disnake
from os import listdir
from disnake.ext import commands
from config import settings
import requests
from io import BytesIO


bot = commands.Bot(
    command_prefix=settings['prefix'],
    intents=disnake.Intents.all(),
    owner_ids=[701011594913775697, 806151791146041344, 599252253404299316, 928361369651265536]
    )
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Запущен {bot.user.name}#{bot.user.discriminator}!")
    activity = disnake.Activity(name='client.baget-inc.online 🦊', type=disnake.ActivityType.listening)
    await bot.change_presence(activity=activity)

list_cogs = [filename[:-3] for filename in listdir("./cogs") if filename.endswith(".py")]
for cog in list_cogs: bot.load_extension(f"cogs.{cog}")

@bot.slash_command()
async def admin(ctx):
    pass
    
@admin.sub_command(description=f'Загрузить модуль бота', guild_ids=[1098232886802526262])
@commands.is_owner()
async def load(inter, module: str = commands.Param(description="Название модуля")):
    bot.load_extension(f"cogs.{module}")
    await inter.send(f"Загружен модуль `{module}`")
    
@admin.sub_command(description=f'Выгрузить модуль бота', guild_ids=[1098232886802526262])
@commands.is_owner()
async def unload(inter, module: str = commands.Param(description="Название модуля")):
    bot.unload_extension(f"cogs.{module}")
    await inter.send(f"Выгружен модуль `{module}`")

@admin.sub_command(description=f"Перезагрузить модуль бота", guild_ids=[1098232886802526262])
@commands.is_owner()
async def reload(inter, module: str = commands.Param(description="Название модуля", choices=list_cogs)):
    bot.reload_extension(f"cogs.{module}")
    await inter.send(f"Перезагружен модуль `{module}`")

bot.run(settings['token'])