from aiogram import Bot, Dispatcher, Router
from app.core.config import API_TOKEN

import logging

logger = logging.getLogger(__name__)
logger.info("Bot initialisation...")

# Initialisation du bot
bot = Bot(token=API_TOKEN)

dp = Dispatcher()
router = Router()
dp.include_router(router)

