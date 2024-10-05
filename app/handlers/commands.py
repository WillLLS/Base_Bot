from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery

from aiogram.enums import ParseMode

from aiogram import types

import logging

from app.database import *
from app.core.bot import bot, router
from app.handlers.states import Details, Trip, CategoryForm, EditTransaction
from app.utils.messages import *

from time import time

logger = logging.getLogger(__name__)


def user_checker(func):
    async def wrapper(message: types.Message, state: FSMContext, *args):
        
        if "user" in list((await state.get_data()).keys()):
            user : user_t =(await state.get_data())["user"]
        else:
            user = User.get(message.from_user.id)
        
        if user:
            await func(message, state, *args)
        else:
            await message.answer("You are not registered. Please use /register")
            
    return wrapper

# Gérer la commande /start
@router.message(CommandStart())
@user_checker
async def start_command(message: types.Message, state: FSMContext):    
    await message.delete()
    
    msg = "Welcome to Potabalance"
    
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Quit", callback_data="quit")  
    
    await message.answer(msg, reply_markup=mk_b.as_markup())
    

# Gérer les réponses
@router.callback_query()
async def handle_callback_query(call: CallbackQuery, state: FSMContext):
    
    logger.info("Main Callback")
    
    await call.answer()
    message = call.message
    data = call.data 
    
    
    if data == "quit":
        await message.delete()
        await state.clear()