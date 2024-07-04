import discord
from discord.ext import tasks
from database import connect_to_db
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


# Функция парсинга участников чата discord
async def parse_participants(projects_name, discord_link):
    print(f'Пошёл парсинг!')
    # Покдлючаемся к серверу
    # guild_id = int(discord_link.split('/')[-1])
    # guild = client.get_guild(guild_id)
    invite = await client.fetch_invite(discord_link)
    guild_id = invite.guild.id
    guild = client.get_guild(guild_id)

    # Список членов чата
    members = []
    async for member in guild.fetch_members():
        members.append(member)

    # Вставляем данные в БД
    connect = connect_to_db()
    cur = connect.cursor()
    for value in members:
        cur.execute("INSERT INTO result (projects_name, login, role) VALUES (%s, %s, %s)", (projects_name, value.name, value.top_role.name))
    connect.commit()
    cur.close()


# Функция парсера каждого проекта
async def parse_projects():
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("SELECT projects_name, discord_link FROM projects")
    projects = cur.fetchall()
    for value in projects:
        await parse_participants(value[0], value[1])
    cur.close()


@tasks.loop(seconds=300)  # Run every 5 minutes
async def parse_projects_loop():
    await parse_projects()


@client.event
async def on_ready():
    print("Бот успешно запущен и подключён к серверу Discord!")
    parse_projects_loop.start()


# Запуск парсинга
@client.event
async def on_message(message):
    print(f"(Канал: {message.channel.name}, Автор: {message.author.name})")
    if message.content == '!start_parsing':
        await parse_projects()

client.run(DISCORD_TOKEN)



