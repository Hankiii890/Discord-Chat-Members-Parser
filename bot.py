# Импортируем необходимые библиотеки
import discord
from discord.ext import commands
from database import connect_to_db  # Подключаем файл для работы с базой данных
from dotenv import load_dotenv
import os
import csv

# Загружаем переменные окружения
load_dotenv()

# Получаем токен бота из переменных окружения
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Создаем объект интентов для определения поведения бота
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

# Создаем экземпляр бота с заданным префиксом команд и настройками интентов
bot = commands.Bot(command_prefix='!', intents=intents)

# Функция для парсинга и обновления данных участников проекта
async def parse_participants(projects_name, discord_link):
    """Функция парсинга участников проекта, обновления CSV и базы данных"""

    # Получаем приглашение и сервер Discord
    invite = await bot.fetch_invite(discord_link)
    guild_id = invite.guild.id
    guild = bot.get_guild(guild_id)

    # Получаем список участников проекта
    members = await guild.chunk()  # chunk используется для получения всех участников

    # Записываем информацию в базу данных
    connect = connect_to_db()
    cur = connect.cursor()
    for member in members:
        cur.execute("INSERT INTO result (projects_name, login, role) VALUES (%s, %s, %s)",
                    (projects_name, member.name, member.top_role.name))
    connect.commit()
    cur.close()

    # Обновляем CSV файл
    with open('results.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for member in members:
            writer.writerow([projects_name, member.name, member.top_role.name])

# Функция для парсинга данных каждого проекта
async def parse_projects():
    """Функция для парсинга данных каждого проекта и создания CSV файла"""

    # Получаем соединение с базой данных и выполняем запрос для получения проектов
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("TRUNCATE TABLE result RESTART IDENTITY")
    connect.commit()

    # Парсим участников для каждого проекта
    cur.execute("SELECT projects_name, discord_link FROM projects")
    projects = cur.fetchall()
    for value in projects:
        await parse_participants(value[0], value[1])
    cur.close()

# Обработчик события запуска бота
@bot.event
async def on_ready():
    print("Бот успешно запущен и подключен к серверу Discord!")

    # При запуске бота создаем пустой CSV файл, если он еще не существует
    with open('results.csv', 'a', newline='') as csvfile:
        pass

# Команда для запуска парсинга проектов
@bot.command()
async def start_parsing(ctx):
    """Команда для запуска парсинга проектов"""
    await parse_projects()
    await ctx.send("CSV файл с данными успешно сгенерирован и данные добавлены в базу данных!")

# Обработчик события нового сообщения
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Запускаем бота с помощью предоставленного токена
bot.run(DISCORD_TOKEN)