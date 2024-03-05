import disnake
from disnake.ext import commands
import sqlite3

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('points.db')
        self.c = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS points (
                    user_id integer PRIMARY KEY,
                    points integer NOT NULL DEFAULT 0
                    )""")
        self.conn.commit()

    def _modify_points(self, user_id, points):
        self.c.execute("INSERT OR IGNORE INTO points (user_id, points) VALUES (?, ?)", (user_id, points))
        self.c.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (points, user_id))
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Point готовы")
        
    @commands.slash_command()
    async def balls(self, ctx):
        print("Дарова, это чел заюзал сую команду")

    @balls.sub_command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member: disnake.Member, points: int):
        self._modify_points(member.id, points)
        embed = disnake.Embed(title="Добавлено баллов", description=f"Пользователь: {member.mention}\nБаллов: {points}", color=0x00ff00)
        await ctx.send(embed=embed)

    @balls.sub_command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, member: disnake.Member, points: int):
        self._modify_points(member.id, -points)
        embed = disnake.Embed(title="Убрано баллов", description=f"Пользователь: {member.mention}\nБаллов: {points}", color=0x00ff00)
        await ctx.send(embed=embed)
 
    @balls.sub_command()
    @commands.has_permissions(administrator=True)
    async def adduser(self, ctx, member: disnake.Member=None):
        self.c.execute("INSERT INTO points (user_id, points) VALUES (?, 0)", (member.id,))
        self.conn.commit()
        embed = disnake.Embed(title="Добавлен в бд", description=f"Пользователь {member.mention} добавлен в базу данных", color=0x00ff)
        await ctx.send(embed=embed)
        
    @balls.sub_command()
    async def balance(self, ctx, member: disnake.Member):
        member = member or ctx.author
        self.c.execute("SELECT points FROM points WHERE user_id = ?", (member.id,))
        result = self.c.fetchone()
        if result is not None:
            embed = disnake.Embed(title="Баллы", description=f"Пользователь: {member.mention}\nБаллов: {result[0]}", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(title="У пользователя ноль баллов", description=f"Пользователь: {member.mention}", color=0x00ff00)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Points(bot))
    print("[Points] готов")