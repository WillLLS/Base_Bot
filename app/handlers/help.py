from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery


from aiogram import types
from aiogram.fsm.state import State, StatesGroup


import logging

from app.database import *
from app.core.config import admin_usernames
from app.core.bot import bot, router
from app.handlers.states import Form
from app.utils.utils import is_convertible_to_int, save_media

from app.handlers.admin import admin_checker
from app.handlers.teachers import check_teacher


logger = logging.getLogger(__name__)

async def init(message: types.Message):
    from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
    
    await message.react([ReactionTypeEmoji(emoji="🥰")], is_big=True)

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Compris  🫡", callback_data="delete")
    
    return mk_b


@router.message(Command("help"))
@admin_checker
async def help_admin(message: types.Message, state: FSMContext):
    
    mk_b = await init(message)
    
    if message.chat.id == int(TEACHER_GROUP_ID):
        from app.utils.messages import teacher_help_message
        
        await message.answer(teacher_help_message, reply_markup=mk_b.as_markup())
        return
    
    from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
    
    await message.react([ReactionTypeEmoji(emoji="🥰")], is_big=True)
    
    
    from app.utils.messages import admin_help_message
    
    await message.answer(admin_help_message, reply_markup=mk_b.as_markup())
    
    message.chat.id == int(TEACHER_GROUP_ID)
    
    await message.answer("Message /help (Teacher):", reply_markup=mk_b.as_markup())
    await help_teacher(message, state)
    
    await message.answer("Message /help (Student):", reply_markup=mk_b.as_markup())
    await help_student(message, state)
    
    
@router.message(Command("help"))
@check_teacher
async def help_teacher(message: types.Message, state: FSMContext, flag_admin=False):
    print("help_teacher")
    mk_b = await init(message)
    
    from app.utils.messages import teacher_help_message
        
    await message.answer(teacher_help_message, reply_markup=mk_b.as_markup())


@router.message(Command("help"))
async def help_student(message: types.Message, state: FSMContext):
    mk_b = await init(message)
    
    from app.utils.messages import student_help_message
    
    await message.answer(student_help_message, reply_markup=mk_b.as_markup())