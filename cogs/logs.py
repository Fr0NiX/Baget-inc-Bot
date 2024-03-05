import disnake
from disnake.ext import commands
from db import SQLITE
from datetime import datetime
import datetime

db = SQLITE("database.db")

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # [ ] Участник перешел в другой голосовой канал
    # [X] Участник покинул голосовой канал
    # [X] Участник зашел в голосовой канал
    # [X] Сообщение было отредактировано
    # [X] Сообщение было удалено
    # [ ] Сообщения были очищены
    # [ ] Участник был размьючен
    # [ ] Участник был замьючен
    # [ ] Участник был разбанен
    # [ ] Обновлены роли участника
    # [X] Никнейм участника был изменен
    # [X] Участник покинул сервер
    # [X] Присоединился новый участник
    # [X] Участник был забанен
    # [ ] Создана роль
    # [ ] Роль удалена
    # [ ] Канал создан
    # [ ] Канал удалён 


    @commands.Cog.listener()
    async def on_member_join(self, member):
        logchannel = db.get(f"logchannel_{member.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        embed = disnake.Embed(description=f"Участник {member.mention} (`{member.name}`) присоединился к серверу", timestamp=datetime.datetime.now(),  color=0x2b2d31)
        embed.add_field(name="Дата регистрации:", value=f'{disnake.utils.format_dt(member.created_at, "D")} ({disnake.utils.format_dt(member.created_at, "R")})')
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logchannel = db.get(f"logchannel_{member.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        roles = [role.mention for role in reversed(member.roles[1:])]
        if len(roles) > 15:
            roles = roles[:15] + ["\nи еще {} ролей...".format(len(roles) - 15)]
        embed = disnake.Embed(description=f"Участник {member.mention} (`{member.name}`) покинул(-а) сервер", timestamp=datetime.datetime.now(),  color=0x2b2d31)
        embed.add_field(name="Роли:", value=' '.join(roles))
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        logchannel = db.get(f"logchannel_{guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        embed = disnake.Embed(description=f"Участник {user.mention} (`{user.name}`) был забанен на сервере", timestamp=datetime.datetime.now(), color=0x2b2d31)
        roles = [role.mention for role in reversed(user.roles[1:])]
        if len(roles) > 15:
            roles = roles[:15] + ["\nи еще {} ролей...".format(len(roles) - 15)]
        embed.add_field(name="Роли:", value=' '.join(roles))
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        logchannel = db.get(f"logchannel_{guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        embed = disnake.Embed(description=f"Участник {user.mention} (`{user.name}`) был разбанен на сервере", timestamp=datetime.datetime.now(), color=0x2b2d31)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logchannel = db.get(f"logchannel_{before.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        if before.nick != after.nick:
            embed = disnake.Embed(description=f"Никнейм пользователя `{after.nick}` был обновлён", timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.add_field(name='До:',value=f'```\n{before.nick}\n```', inline=False)
            embed.add_field(name='После:',value=f'```\n{after.nick}\n```', inline=False)
            embed.set_footer(text=f"ID: {before.id}")
            embed.set_thumbnail(url=before.display_avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        logchannel = db.get(f"logchannel_{before.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        lang_server = db.get(f"lang_{before.guild.id}") or "ru"
        if before.content == after.content:
            return
        if lang_server == 'ru':
            embed = disnake.Embed(description=f"Сообщение было отредактировано", timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.add_field(name='До:',value=f'```\n{before.content}\n```', inline=False)
            embed.add_field(name='После:',value=f'```\n{after.content}\n```', inline=False)
            embed.add_field(name='Автор:',value=f'{before.author.mention} (`{before.author.name}`)', inline=True)
            embed.add_field(name='Канал:',value=f'{before.channel.mention} (`{before.channel.name}`)', inline=True)
            embed.set_footer(text=f"ID: {before.id}")
        if lang_server == 'en':
            embed = disnake.Embed(description=f"Post has been edited", timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.add_field(name='Before:',value=f'```\n{before.content}\n```', inline=False)
            embed.add_field(name='After:',value=f'```\n{after.content}\n```', inline=False)
            embed.add_field(name='Author:',value=f'{before.author.mention} (`{before.author.name}`)', inline=True)
            embed.add_field(name='Channel:',value=f'{before.channel.mention} (`{before.channel.name}`)', inline=True)
            embed.set_footer(text=f"ID: {before.id}")
        if lang_server == 'uk':
            embed = disnake.Embed(description=f"Повідомлення було відредаговано", timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.add_field(name='До:',value=f'```\n{before.content}\n```', inline=False)
            embed.add_field(name='Після:',value=f'```\n{after.content}\n```', inline=False)
            embed.add_field(name='Автор:',value=f'{before.author.mention} (`{before.author.name}`)', inline=True)
            embed.add_field(name='Канал:',value=f'{before.channel.mention} (`{before.channel.name}`)', inline=True)
            embed.set_footer(text=f"ID: {before.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logchannel = db.get(f"logchannel_{message.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        message_content = message.content
        if message_content == '':
            return
        if len(message_content) > 1024:
            with open('message.txt', 'w', encoding='utf-8') as file:
                file.write(message_content)
            file = disnake.File("message.txt")

            embed = disnake.Embed(description=f"Сообщение было удалено", color=0x2b2d31)
            embed.add_field(name='Автор:', value=f'{message.author.mention} (`{message.author.name}`)', inline=True)
            embed.add_field(name='Длина сообщения:', value=f'`{len(message.content)}` символов', inline=True)
            embed.add_field(name='Канал:', value=f'{message.channel.mention} (`{message.channel.name}`)', inline=True)
            await channel.send(embed=embed, file=file)
        if len(message_content) < 1024:
            text = message.content.replace("`", "")
            embed = disnake.Embed(description=f"Сообщение было удалено", color=0x2b2d31)
            embed.add_field(name='Удалённое сообщение:',value=f'```\n{text}\n```', inline=False)
            embed.add_field(name='Автор:',value=f'{message.author.mention} (`{message.author.name}`)', inline=True)
            embed.add_field(name='Канал:',value=f'{message.channel.mention} (`{message.channel.name}`)', inline=True)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logchannel = db.get(f"logchannel_{member.guild.id}")
        channel = self.bot.get_channel(int(logchannel))
        print(before.channel)
        print(after.channel)
        voice_stat = self.bot.get_channel(int(before.channel.id))
        if voice_stat and channel.type == disnake.ChannelType.stage_voice:
            join = "вошел на трибуну"
            leave = "покинул трибуну"
        if voice_stat and channel.type == disnake.ChannelType.voice:
            join = "присоединился к голосовому каналу"
            leave = "покинул головосой канал"
        if before.channel is None and after.channel is not None:
            embed = disnake.Embed(
                title="Участник присоединился к голосовому каналу",
                description=f"{member.mention} (`{member.name}`) {join} {after.channel.mention}",
                timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.set_footer(text=f"ID: {member.id}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)
        elif before.channel is not None and after.channel is None:
            embed = disnake.Embed(
                title="Участник вышел из голосового канала",
                description=f"{member.mention} (`{member.name}`) {leave} {before.channel.mention}",
                timestamp=datetime.datetime.now(), color=0x2b2d31)
            embed.set_footer(text=f"ID: {member.id}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def setlogchannel(self, inter, channel: disnake.TextChannel):
        logchannel = db.set(f"logchannel_{inter.guild.id}", f"{channel.id}")
        await inter.send(f"Теперь логи сервера будут приходить в установленный канал: {channel.mention}")

def setup(bot):
    bot.add_cog(Logs(bot))
    print("[Logs] готов")
