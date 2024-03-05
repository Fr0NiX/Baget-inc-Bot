import disnake
from disnake.ext import commands
import sqlite3
import requests
import re
import aiosqlite

image_url = "https://api.aggelos-007.xyz/rankcard"
guild_id = 1098232886802526262

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('level.db')
        self.c = self.conn.cursor()
        self._create_table()
        self.db_name = 'background_url'
        self.db_path = f"{self.db_name}.sqlite3"
        self.default_bg = "https://avatars.mds.yandex.net/i?id=532ab0450dc0e882a5d32c23e335bc4d1fc690ca-5344236-images-thumbs&n=13"
        self.bot.loop.run_until_complete(self.create_db())

    def _create_table(self):
        def _create_table(self):
            self.c.execute("""
                CREATE TABLE IF NOT EXISTS user_levels (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    level INTEGER
                )
            """)
            self.conn.commit()

    async def create_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_backgrounds (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    url TEXT
                )
            """)

    def is_member_in_database(self, member_id):
        query = "SELECT user_id FROM exp WHERE user_id =?"
        result = self.c.execute(query, (member_id,)).fetchone()
        return result is not None

    def add_member_to_database(self, member_id):
        query = "INSERT INTO exp (user_id, exp) VALUES (?, 0)"
        self.c.execute(query, (member_id,))
        self.conn.commit()
    
    def _modify_points(self, user_id, exp):
        self.c.execute("INSERT OR IGNORE INTO exp (user_id, exp) VALUES (?, ?)", (user_id, exp))
        self.c.execute("UPDATE exp SET exp = exp + ? WHERE user_id = ?", (exp, user_id))
        self.conn.commit()
    
    def _create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS exp (
                    user_id integer PRIMARY KEY,
                    exp integer NOT NULL DEFAULT 0
                    )""")
        self.conn.commit()

    def new_exp(self, user_id, exp=5):
        self.c.execute("INSERT OR IGNORE INTO exp (user_id, exp) VALUES (?,?)", (user_id, exp))
        self.c.execute("UPDATE exp SET exp = exp +? WHERE user_id =?", (exp, user_id))
        self.conn.commit()
        
    def url_is_valid(self, url: str):
        regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?'
            r'|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            r')'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE
        )

        return re.match(regex, url) is not None

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(guild_id)

        members = guild.members

        for member in members:
            if not self.is_member_in_database(member.id):
                self.add_member_to_database(member.id)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.c.execute("INSERT INTO exp (user_id, exp) VALUES (?, 0)", (member.id,))
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        user = message.author
        user_id = user.id 
        self.new_exp(user_id) 
        
    @commands.slash_command(name="level")
    async def _level(self, interaction):
        print("Суб команда")
        
    @_level.sub_command()
    async def level(self, interaction, member: disnake.Member = None):
        await interaction.response.defer()
        if member is None:
            member = interaction.author
        avatar_url = member.display_avatar.url
        name = member.display_name
        self.c.execute("SELECT exp FROM exp WHERE user_id =?", (member.id,))
        result = self.c.fetchone()
        exp = result[0] if result else 0  # Проверка на None и извлечение значения опыта
    
        async with aiosqlite.connect(self.db_path) as db:
            r = await db.execute("SELECT url FROM user_backgrounds WHERE user_id = ?", (member.id,))
            bg_url = await r.fetchone()
            bg_url = bg_url[0] if bg_url else self.default_bg
        
        params = {
            "avatar": avatar_url,
            "username": name,
            "xp": exp,
            "maxxp": 10000000,
            "level": exp / 200,
            "background": bg_url,
            "blur": True,
            "xpcolor": "FFA500",
            "fontcolor": "FFFFFF",
            "bgcolor": "000000",
            "border": True,
            "bordercolor": "808080"
        }

        response = requests.get(image_url, params=params)
        
        if response.status_code == 200:
            with open('welcome_card.png', 'wb') as file:
                file.write(response.content)
            print("Изображение успешно скачано и сохранено как welcome_card.png")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")
        await interaction.edit_original_message(file=disnake.File("welcome_card.png"))
    
    @_level.sub_command()
    @commands.has_permissions(administrator=True)
    async def addexp(self, inter, member: disnake.Member, exp: int):
        self._modify_points(member.id, exp)
        embed = disnake.Embed(title="Добавлено опыта", description=f"Пользователь: {member.mention}\nОпыта: {exp}", color=0x00ff00)
        await inter.response.send_message(embed=embed)
        

    @_level.sub_command()
    @commands.has_permissions(administrator=True)
    async def removeexp(self, inter, member: disnake.Member, exp: int):
        await interaction.response.defer()
        self._modify_points(member.id, -exp)
        embed = disnake.Embed(title="Убрано опыта", description=f"Пользователь: {member.mention}\nОпыта: {exp}", color=0x00ff00)
        await inter.response.send_message.send(embed=embed)
         
    @_level.sub_command(name="setbackground", description="Поставить свой задний фон")
    async def setbackground(self, inter, *, url: str = ""):
        if url == "" or not self.url_is_valid(url):
            url = self.default_bg
            
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO user_backgrounds(user_id, url)
                VALUES(?, ?)
            """, (inter.author.id, url))
            await db.commit()

        await inter.response.send_message(f"Фоновая картинка заменена.") 
        


def setup(bot):
    bot.add_cog(Level(bot))
    print("[Level] готов")