import discord
from discord.ext import commands
from database import connect_to_db
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Информируем об успешном подключение бота!"""
    print("Бот успешно запущен и подключён к серверу Discord!")


async def parse_participants(projects_name, discord_link):
    """Функция парсинга участников чата discord"""
    print(f"Парсинг прошёл!")
    invite = await bot.fetch_invite(discord_link)
    guild_id = invite.guild.id
    guild = bot.get_guild(guild_id)

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
        cur.execute("INSERT INTO result (projects_name, login, role) VALUES (%s, %s, %s)",
                    (projects_name, value.name, value.top_role.name))
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


@bot.command()
async def start_parsing(ctx):
    await parse_projects()


@bot.command()
async def help_commands(ctx):
    help_message = """
    Список доступных команд:
    !start_parsing - запустить парсер
    """
    await ctx.send(help_message)


bot.run(DISCORD_TOKEN)
