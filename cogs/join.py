import disnake 
from disnake.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import aiohttp
import os

class JoinsLog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(member.guild.get_role(1099335173058854913))
        channel = self.bot.get_channel(1098290420250845254)  # ID канала, куда нужно отправлять приветствия
        humans = sum(not member.bot for member in member.guild.members)
        avatar_url = member.display_avatar.url
        image_url = "https://api.aggelos-007.xyz/welcomecard"

        params = {
            "text1": f"Hello, {member}",
            "text2": f"You are our #{humans} user",
            "text3": "Enjoy using Baget-inc.online hosting!",
            "blur": True,
            "avatar": avatar_url,
            "bgcolor": "373737",
            "fontcolor": "ffffff",
            "border": True,
            "bordercolor": "FF0000",
            "background": "https://w.forfun.com/fetch/d6/d6231aef1b85068f6442d0e75f6b0b0c.jpeg"
        }

        response = requests.get(image_url, params=params)

        if response.status_code == 200:
            with open('welcome_card.png', 'wb') as file:
                file.write(response.content)
            print("Изображение успешно скачано и сохранено как welcome_card.png")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")

        embed = disnake.Embed(
            title=f"Добро пожаловать, {member}", 
            description=f"Добро пожаловать на к нам, в **{member.guild.name}**, вы наш участник #{humans}", 
            color=0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        await channel.send(content=f"<@{member.id}>")
        await channel.send(embed=embed, file=disnake.File("welcome_card.png"))
        
        #<:boost_1:1095419759417364480> 
def setup(bot):
    bot.add_cog(JoinsLog(bot))
    print("[Join] готов")