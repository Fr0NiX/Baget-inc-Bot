import disnake
from disnake.ext import commands
import platform
import psutil
import pytz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import io
import numpy as np
import matplotlib.patches as mpatches
import requests
from disnake import Embed
import asyncio
from disnake.ext import commands, tasks


moscow_tz = pytz.timezone('Europe/Moscow')

def get_moscow_time():
    # Добавляем к текущему времени 3 часа
    return datetime.now(moscow_tz) + timedelta(hours=3)

def system_info():
    uname = platform.uname()
    sys_info = f"Система: {uname.system}\nИмя узла: {uname.node}\nВерсия: {uname.version}\nМашина: {uname.machine}\nПроцессор: {uname.processor}"
    return sys_info, psutil.cpu_count(logical=True)

def round_to_thousands_gb(value):
    return round(value / 1024)

class Stats2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_stats.start()

    @tasks.loop(seconds=10)
    async def send_stats(self): # Не забудь про async
        messagebox = self.bot.get_channel(1193307736788709386)  # Замени на актуальный ID канала

        cpu_patch = mpatches.Patch(color='orange', label='CPU')
        memory_patch = mpatches.Patch(color='skyblue', label='Memory')

        # IP-адрес Flask сервера и порт, на котором он запущен
        flask_server_ip = 'http://141.147.61.232:25567'  # Пример адреса, замени на актуальный

        response = requests.get(f"{flask_server_ip}/stats")

        if response.status_code == 200:
            data = response.json()
            cpu_usage = np.array(data['cpu_usage_history'])
            mem_usage = np.array(data['memory_usage_history'])
            mem_usage = mem_usage / 1024  # Предполагается, что данные приходят в МБ
        else:
            print("Ошибка при получении данных с сервера")

        # Находим максимальное значение потребления ОЗУ и устанавливаем шкалу с некоторым запасом
        min_mem_usage = np.min(mem_usage)
        max_mem_usage = np.max(mem_usage)
        # Например, можем сделать так, чтобы максимум на шкале всегда был на 10% больше
        mem_scale_min = np.floor(min_mem_usage)
        mem_scale_max = np.ceil(max_mem_usage * 1.1)  # Нижняя граница + 10%

        fig, (ax_cpu, ax_mem) = plt.subplots(2, 1, figsize=(10, 8))

        ax_cpu.plot(cpu_usage, label='CPU Usage', color='orange', linewidth=2)
        ax_cpu.fill_between(range(len(cpu_usage)), cpu_usage, color='orange', alpha=0.1)
        ax_cpu.set_ylim(0, 100)
        ax_cpu.set_ylabel('Процент(%)', color='orange', fontsize=14)
        ax_cpu.tick_params(axis='y', colors='orange', which='both', length=0)
        ax_cpu.legend(handles=[cpu_patch])
        ax_cpu.grid(False)

# Настраиваем график Memory
        ax_mem.plot(mem_usage, label='Memory Usage', color='skyblue', linewidth=2)
        ax_mem.fill_between(range(len(mem_usage)), mem_usage, color='skyblue', alpha=0.1)
        ax_mem.set_ylim(mem_scale_min, mem_scale_max)  # Динамическая верхняя и нижняя границы оси Y
        ax_mem.set_yticks(np.arange(mem_scale_min, mem_scale_max + 0.5, 0.5))  # Шаг сетки 500 МБ
        ax_mem.set_ylabel('Гигабайт(GB)', color='orange', fontsize=14)
        ax_mem.tick_params(axis='y', colors='orange', which='both', length=0)
        ax_mem.legend(handles=[memory_patch])
        ax_mem.grid(False)


# Устанавливаем размер шрифта для подписей делений
        plt.rc('ytick', labelsize=14)

# Настраиваем общие параметры графиков
        ax_cpu.set_facecolor('#353535')
        ax_mem.set_facecolor('#353535')
        fig.patch.set_facecolor('#353535')

        plt.tight_layout(pad=3.0)
        plt.savefig('d2_usage.png', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        
        title = "D2"
        embed = Embed(title=title)
        response = requests.get('http://141.147.61.232:25567/stats')
        node_stats = response.json()
    
        if not node_stats.get('system_hard_data'):
            embed.description = "Offline 📴"
            embed.colour = disnake.Colour.red()
            return embed

        is_online = node_stats.get('is_online', True)
        if is_online:
            system_hard_data = node_stats['system_hard_data']
            system_data = node_stats['system_data']
        
            cpu_name = system_hard_data['cpuName']
            os_name = system_hard_data['os']

            embed.description = f"{os_name}\n\n{cpu_name}"
            embed.colour = disnake.Colour.green()
        
            memory_usage_latest = system_data.get('memory', 0) / 1024
            disk_usage_latest = system_data.get('disk', 0) / 1024
            cpu_usage_latest = system_data.get('cpu', 0)

            embed.add_field(name="CPU Cores", value=str(system_hard_data['cpu']), inline=True)
            embed.add_field(name="CPU Usage", value=f"{round(cpu_usage_latest)}%", inline=True)
            embed.add_field(name="Memory", value=f"{memory_usage_latest:.2f}/{round_to_thousands_gb(system_hard_data['memory'])} GB", inline=True)
            embed.add_field(name="Disk", value=f"{disk_usage_latest:.2f}/{round_to_thousands_gb(system_hard_data['disk'])} GB", inline=True)
        
            embed.set_thumbnail(url="https://static.linux123123.com/online.png")
            embed.set_image(file=disnake.File("/home/container/d2_usage.png"))
        else:
            embed.description = "Node is offline 😴"
            embed.colour = disnake.Colour.greyple()

        try:
            if self.last_message is not None:
                await self.last_message.edit(embed=embed)
            else:
                self.last_message = await messagebox.send(embed=embed)
        except Exception as e:
            print(f"Ошибка при изменении сообщения: {e}")
  
    @send_stats.before_loop
    async def before_send_stats(self):
        await self.bot.wait_until_ready()
        self.last_message = None
            
            

def setup(bot):
    bot.add_cog(Stats2(bot))
    print("[D2] готов")