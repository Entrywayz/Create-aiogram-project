read -p "Введите путь к папке, где будет лежать проект (например, C:/Users/Desktop/): " path_to_project

cd "$path_to_project" || { echo "Не удалось перейти в указанную папку"; exit 1; }

read -p "Назовите свой проект: " project_name

if [ ! -d "$project_name" ]; then
    mkdir "$project_name"
else
    echo "Папка $project_name уже существует."
    exit 1
fi

cd "$project_name" || { echo "Не удалось перейти в папку проекта"; exit 1; }

python -m venv .venv || { echo "Ошибка при создании виртуального окружения"; exit 1; }

source .venv/bin/activate || { echo "Ошибка при активации виртуального окружения"; exit 1; }
pip install aiogram pydantic_settings pydantic || { echo "Ошибка при установке пакетов"; exit 1; }

mkdir -p handlers keyboards

cat > bot.py <<EOF
import asyncio
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
EOF

cat > config_reader.py <<EOF
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
EOF

cat > .env <<EOF
BOT_TOKEN=
EOF

cat > .gitignore <<EOF
.venv
.env
EOF

cd handlers

cat > bot_messages.py <<EOF
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message()
async def start(msg: Message):
    await msg.answer("Hello, this is your message: " + msg.text)
EOF

cat > user_commands.py <<EOF
from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def send_invoice_handler(msg: Message):
    await msg.answer("Hi!")
EOF

cat > __init__.py <<EOF
from .user_commands import router as user_commands_router
from .bot_messages import router as bot_messages_router

user_commands = user_commands_router
bot_messages = bot_messages_router
EOF

cd ..
cd keyboards

cat > __init__.py <<EOF
from .inline import *
from .reply import *

__all__ = ['*']
EOF

cat > inline.py <<EOF
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
EOF

cat > reply.py <<EOF
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
EOF

echo "Проект успешно создан!"
