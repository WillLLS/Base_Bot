from aiogram import Bot
from aiogram.types import BotCommand

async def set_menu(bot: Bot):
    commands = [
        BotCommand(command="start", description="It’s good to start somewhere 🥳"),
    ]
    await bot.set_my_commands(commands)
