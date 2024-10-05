from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery


from aiogram import types
from aiogram.fsm.state import State, StatesGroup


import logging

from app.database import *
from app.core.config import admin_id
from app.core.bot import bot, router
from app.utils.utils import is_convertible_to_int, save_media

logger = logging.getLogger(__name__)

class AdminForm(StatesGroup):
    #state_name = State()


def admin_checker(func):
    async def wrapper(message: types.Message, state: FSMContext, *args):
        
        if int(message.chat.id) == int(admin_id):
            await func(message, state, *args)
        else:
            await message.answer("You are not allowed to use this command")
    return wrapper

def admin_checker_callback(func):
    async def wrapper(callback_query: CallbackQuery, state: FSMContext):
                    
        if int(callback_query.chat.id) == int(admin_id):
            await func(callback_query, state)
            
        else:
            await callback_query.message.answer("You are not allowed to use this command")
    return wrapper


# Add a lesson command
@router.message(Command("admin"))
@admin_checker
async def admin_command(message: types.Message, state: FSMContext):
    pass
      

# Callbacks for admin
@router.callback_query()
@admin_checker_callback
async def admin_callback(call: CallbackQuery, state: FSMContext):
    logger.info("Admin callback")
    
    await call.answer()
    message = call.message
    data = call.data 
    
    if data == "admin_command":
        pass
    
    else:
        from app.handlers.commands import handle_callback_query
        
        await handle_callback_query(call, state)