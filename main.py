import discord
import config
import requests
from datetime import datetime
import asyncio

# URL API для получения времени
url = "https://worldtimeapi.org/api/timezone/Europe/Moscow"

# Токен вашего бота
TOKEN = config.TOKEN

# Создаем клиент Discord с указанием интентов
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Переменная для хранения последнего сообщения бота
last_bot_message = None

async def fetch_time():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        datetime_str = data['datetime']
        datetime_obj = datetime.fromisoformat(datetime_str)
        # Добавляем указание временной зоны
        moscow_time = datetime_obj.strftime("%H:%M") + " по МСК"
        return moscow_time
    else:
        return "Не удалось получить время"

# Обработчик события "бот готов к использованию"
@client.event
async def on_ready():
    print('Бот готов')
    # Устанавливаем статус бота
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="кошариков"))

# Обработчик события "сообщение от пользователя"
@client.event
async def on_message(message):
    global last_bot_message

    if message.author == client.user:
        return  # Игнорируем сообщения, отправленные самим ботом

    print(message.author)
    print('Получено сообщение:', message.content)
    
    # Получаем текущее время
    current_time = await fetch_time()
    
    # Удаляем предыдущее сообщение бота, если оно существует
    if last_bot_message is not None:
        try:
            await last_bot_message.delete()
        except discord.NotFound:
            # Сообщение уже удалено
            pass
    
    # Формируем сообщение с временем и картинкой
    message_content = f"# {current_time}"
    embed = discord.Embed(description=message_content)
    embed.set_image(url="https://cdn.discordapp.com/avatars/1212443449039786035/e9cb4b960517ae17448111bffbe0dbc7.webp?size=1024&format=webp&width=0&height=256")
    
    # Отправляем новое сообщение и сохраняем его ссылку
    last_bot_message = await message.channel.send(embed=embed)

# Запускаем бота
client.run(TOKEN)
