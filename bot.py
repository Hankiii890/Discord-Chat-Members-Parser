import discord
from database import connect_to_db
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


async def parse_participants(projects_name, discord_link):
    """Функция парсинга участников чата discord"""
    print(f"Начало парсинга!")
    invite = await client.fetch_invite(discord_link)
    guild_id = invite.guild.id
    guild = client.get_guild(guild_id)

    # Список членов чата
    members = []
    async for member in guild.fetch_members():
        members.append(member)

    # Очищаем таблицу result перед заполнением новыми данными
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("TRUNCATE TABLE result RESTART IDENTITY")
    connect.commit()

    # Добавляем данные
    for value in members:
        cur.execute("INSERT INTO result (projects_name, login, role) VALUES (%s, %s, %s)", (projects_name, value.name, value.top_role.name))
    connect.commit()
    cur.close()


async def parse_projects():
    """Функция парсера каждого проекта"""
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("SELECT projects_name, discord_link FROM projects")
    projects = cur.fetchall()
    for value in projects:
        await parse_participants(value[0], value[1])
    cur.close()


@client.event
async def on_ready():
    """Информируем об успешном подключение бота!"""
    print("Бот успешно запущен и подключён к серверу Discord!")


@client.event
async def on_message(message):
    """Запуск парсинга"""
    if message.content == '!start_parsing':
        await parse_projects()
    client.loop.create_task(parse_projects())


client.run(DISCORD_TOKEN)