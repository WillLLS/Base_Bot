"""
    @Author: HunTon
    @contact: https://x.com/huntoncrypto 🤝
    @info: V1.0 - 08.09.2024
"""

import logging
import asyncio


import app.core 
from app.core.bot import bot, dp
from app.core.menu import set_menu

import app.core.config
import app.handlers

# Configuration de base des logs
logging.basicConfig(
    level=logging.INFO,  # Niveau de log
    format="%(asctime)s [%(levelname)s] %(message)s",  # Format du message
    handlers=[
        logging.FileHandler("bot.log"),  # Enregistrement dans un fichier
        logging.StreamHandler()  # Affichage dans la console
    ]
)

logger = logging.getLogger(__name__)


if not app.core.config.DEBUG:
    logging.getLogger('aiogram').setLevel(logging.WARNING)  # Ne montre que les WARNING et plus graves

    # Optionnel : désactiver d'autres bibliothèques tierces
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.ERROR)


async def main():
    logger.info("Bot starting")
    #await bot.send_message(app.core.config.TEACHER_GROUP_ID, "Bot Online: 🟢")
    await set_menu(bot)
    await asyncio.gather(dp.start_polling(bot))


if __name__ == '__main__':
    asyncio.run(main())
    