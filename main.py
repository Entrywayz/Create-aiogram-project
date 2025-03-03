import os
import subprocess

path_to_project = input("Введите путь к папке где будет лежать проект (C:/Users/Desktop/): ")

os.chdir(path_to_project)

project_name = input("Назовите свой проект: ")

path_project = os.path.join(path_to_project, project_name)

if not os.path.exists(project_name):
    os.mkdir(project_name)
else:
    print(f"Папка {project_name} уже существует.")

os.chdir(project_name)

# Создание виртуального окружения
result = subprocess.run(['python', '-m', 'venv', '.venv'], shell=True)
if result.returncode != 0:
    print("Ошибка при создании виртуального окружения")
    exit(1)

# Установка пакетов
result = subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', 'aiogram', 'pydantic_settings', 'pydantic'], shell=True)
if result.returncode != 0:
    print("Ошибка при установке пакетов")
    exit(1)

# Создание папок и файлов
os.makedirs('handlers', exist_ok=True)
os.makedirs('keyboards', exist_ok=True)

with open('bot.py', 'w') as f:
    f.write("""import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
import logging
import handlers
from handlers import user_commands, bot_messages
bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.info('Starting bot...')

async def main():
    dp.include_routers(
        user_commands,
        bot_messages,
    )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
        """)

with open('config_reader.py', 'w') as f:
    f.write("""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8"
    )
    
config = Settings()

""")

with open('.env', 'w') as f:
    f.write('BOT_TOKEN=')

with open('.gitignore', 'w') as f:
    f.write('.venv\n.env')

os.chdir('handlers')

with open('bot_messages.py', 'w') as f:
    f.write("""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message()
async def start(msg: Message):
    await msg.answer("Hello, this is your message: " + msg.text)
        """)

with open('user_commands.py', 'w') as f:
    f.write("""
from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def send_invoice_handler(msg: Message):
    await msg.answer("Hi!")
        """)

with open('__init__.py', 'w') as f:
    f.write("""
from .user_commands import router as user_commands_router
from .bot_messages import router as bot_messages_router

user_commands = user_commands_router
bot_messages = bot_messages_router
""")

os.chdir("..")
os.chdir('keyboards')

with open('__init__.py', 'w') as f:
    f.write("""
from .inline import *
from .reply import *

__all__ = ['*']
""")

with open('inline.py', 'w') as f:
    f.write("""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
""")

with open('reply.py', 'w') as f:
    f.write("""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
""")

print("Success")