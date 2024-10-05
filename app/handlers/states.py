from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.bot import bot, router
from app.database import *

from time import time

import logging

logger = logging.getLogger(__name__)


class Details(StatesGroup):
    amount = State()
    caption = State()
    category = State()
    
    validate_spent = State()
    validate_sent = State()
    
class CategoryForm(StatesGroup):
    caption = State()
    amount = State()
    update_amount = State()
    
class EditTransaction(StatesGroup):
    amount = State()
    caption = State()
    category = State()
    date = State()
    
    validate = State()
    
class Trip(StatesGroup):
    name = State()
    destination = State()
    date = State()
    validate = State()
    amount = State()
    
    

def checker_cancel(func):
    async def wrapper(message: types.Message, state: FSMContext, *args):
        if message.text == "/cancel":
            await state.clear()
            await message.answer("Canceled")
            return
        
        await func(message, state, *args)
        
    return wrapper

    

@router.message(Details.amount)
@checker_cancel
async def handle_amount(message: types.Message, state: FSMContext):
    logger.info("Amount received - %s€", message.from_user.id)
    
    cache_data = await state.get_data()
    msg_edit : types.Message = cache_data["msg"]
    
    await message.delete()
    
    from app.utils.utils import is_convertible_to_int
    
    if is_convertible_to_int(message.text):
        logger.debug("Amount is convertible to int")
    
        amount = int(message.text)
        await state.update_data(amount=amount)
        await state.set_state(Details.caption)
        
        from app.utils.messages import msg_transaction_1
        from aiogram.enums import ParseMode
        
        msg = msg_transaction_1.format(amount)
        await msg_edit.edit_text(msg, parse_mode=ParseMode.MARKDOWN)
        
    else:
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="Delete", callback_data="delete")
        await message.answer("Please enter a valid amount", reply_markup=mk_b.as_markup())
        
@router.message(Details.caption)
@checker_cancel
async def handle_caption(message: types.Message, state: FSMContext):
    
    logger.info("Caption received - %s", message.from_user.id)
    
    await message.delete()
    
    caption = message.text
    await state.update_data(caption=caption)
    
    cache_data = await state.get_data()
    
    await state.set_state(Details.category)
    await choose_category(message, state)
    
@router.message(Details.category)
@checker_cancel
async def choose_category(message: types.Message, state: FSMContext):
    logger.info("Choosing category - %s", message.from_user.id)
    
    
    from app.utils.messages import msg_transaction_2
    from aiogram.enums import ParseMode
    
    cache_data = await state.get_data()
    
    msg_to_edit : types.Message = cache_data["msg"]
    
    msg = msg_transaction_2.format(cache_data["amount"], cache_data["caption"])
    
    categories = Category.get_all()
    
    if not categories:
        
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="No Potatory Founded", callback_data="None")
        mk_b.button(text="Continue", callback_data="category:None")
        mk_b.adjust(1)
        
        await msg_to_edit.edit_text(msg, reply_markup=mk_b.as_markup(), parse_mode=ParseMode.MARKDOWN)

    else:
        
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="Choose a potatory", callback_data="None")
        for category in categories:
            mk_b.button(text=category.caption, callback_data=f"category:{category.id}")
        
        mk_b.button(text="None", callback_data="category:None")
        mk_b.adjust(1)
    
        await msg_to_edit.edit_text(msg, reply_markup=mk_b.as_markup(), parse_mode=ParseMode.MARKDOWN)
    

        
async def handle_category(message: types.Message, state: FSMContext):
    logger.info("Category received - %s", message.from_user.id)
    
    await message.delete()
    
    category = message.text
    await state.update_data(category=category)
    
    cache_data = await state.get_data()
    
    cache_data = await state.get_data()
    msg_edit : types.Message = cache_data["msg"]
        
    #index = (await state.get_data())["index_answer"]

        

@router.message(CategoryForm.caption)
@checker_cancel
async def handle_category_caption(message: types.Message, state: FSMContext):
    logger.info("Category caption received - %s", message.from_user.id)
    
    await message.delete()
    
    caption = message.text
    await state.update_data(caption=caption)
    
    msg = "Please enter the amount"
    await state.set_state(CategoryForm.amount)
    await message.answer(msg)
    
@router.message(CategoryForm.amount)
@checker_cancel
async def handle_category_amount(message: types.Message, state: FSMContext):
    logger.info("Category amount received - %s", message.from_user.id)
    
    await message.delete()
    
    amount = message.text
    await state.update_data(amount=amount)
    
    cache_data = await state.get_data()
    
    msg = f"Category details:\n\nCaption: {cache_data['caption']}\nAmount: {cache_data['amount']}"
    
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Yes", callback_data="validate_category")
    mk_b.button(text="No", callback_data="cancel")
    
    await message.answer(msg, reply_markup=mk_b.as_markup())

@router.message(CategoryForm.update_amount)
@checker_cancel
async def handle_category_update_amount(message: types.Message, state: FSMContext):
    
    logger.info("Category amount update received - %s", message.from_user.id)
    
    await message.delete()
    
    new_amount = message.text
    
    await state.update_data(new_amount=new_amount)
    
    from app.utils.utils import is_convertible_to_int
    
    if is_convertible_to_int(new_amount):
        
        cache_data = await state.get_data()
        
        ct_id = cache_data["ct_id_update"]
        msg_to_edit : types.Message = cache_data["msg_to_edit"]
        
        category = Category.get(ct_id)
        
        msg = f"*{category.caption}*\n\n`{category.mensual_amount}` -> `{new_amount}`\n\n*Validate ?*"
        
        mk_b = InlineKeyboardBuilder()
        
        mk_b.button(text="Yes", callback_data="validate_update_category")
        mk_b.button(text="No", callback_data="cancel")
        
        from aiogram.enums import ParseMode
        
        await msg_to_edit.edit_text(msg, reply_markup=mk_b.as_markup(), parse_mode=ParseMode.MARKDOWN)
        
    else:
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="Delete", callback_data="delete")
        
        await message.answer("Please enter a valid amount", reply_markup=mk_b.as_markup())


@router.message(EditTransaction.amount)
@checker_cancel
async def handle_edit_amount(message: types.Message, state: FSMContext):
    logger.info("Edit amount received - %s", message.from_user.id)
    
    await message.delete()
    
    from app.utils.utils import is_convertible_to_int
    
    if is_convertible_to_int(message.text):
        logger.debug("Amount is convertible to int")
    
        amount = int(message.text)
        
        await state.update_data(amount=amount)
        
        cache_data = await state.get_data()
        tx : transaction_t = cache_data["tx"]
        tx.amount = amount
        
        await state.update_data(tx=tx)

        await edit_transaction_validate(message, state)
        
    else:
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="Delete", callback_data="delete")
        await message.answer("Please enter a valid amount", reply_markup=mk_b.as_markup())
        
@router.message(EditTransaction.caption)
@checker_cancel
async def handle_edit_caption(message: types.Message, state: FSMContext):
    logger.info("Edit caption received - %s", message.from_user.id)
    
    await message.delete()
    
    caption = message.text
    await state.update_data(caption=caption)
    
    cache_data = await state.get_data()
    tx : transaction_t = cache_data["tx"]
    tx.caption = caption
        
    await state.update_data(tx=tx)
    
    await edit_transaction_validate(message, state)

@router.message(EditTransaction.date)
@checker_cancel
async def handle_edit_date(message: types.Message, state: FSMContext):
    logger.info("Edit date received - %s", message.from_user.id)
    
    def is_convertible_to_ts():
        
        format = "%d/%m/%y"
        
        from datetime import datetime
        date = message.text
        
        try:
            ts = datetime.strptime(date, format).timestamp()
            return ts
        except:
            return False
        
        
    ts = is_convertible_to_ts()  
    if not ts:
        
        mk_b = InlineKeyboardBuilder()
        mk_b.button(text="Delete", callback_data="delete")
        await message.answer("Please enter a valid date, format %d/%m/%y", reply_markup=mk_b.as_markup())
        return
        
    
    
    date = message.text
    await state.update_data(date=date)
    await state.update_data(ts=ts)
    
    cache_data = await state.get_data()
    tx : transaction_t = cache_data["tx"]
    tx.timestamp = ts
        
    await state.update_data(tx=tx)
    
    await edit_transaction_validate(message, state)



async def edit_transaction_validate(message: types.Message, state: FSMContext):
    logger.info("Edit transaction validation - %s", message.from_user.id)
    
    cache_data = await state.get_data()
    
    cache_data = await state.get_data()
    tx : transaction_t = cache_data["tx"]
    
    from datetime import datetime
    
    date = datetime.fromtimestamp(tx.timestamp).strftime("%d/%m/%y")
    
    category = cache_data["category"]
    
    from app.utils.messages import transaction_msg, transaction_msg_category
    
    if category:
            
        msg = transaction_msg_category.format(tx.id, date, tx.amount, tx.caption, category)
    
    else:
        msg = transaction_msg.format(tx.id, date, tx.amount, tx.caption)
    
    
    msg += "\n\n*Validate ?*"
    
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Yes", callback_data="validate_edit_transaction")
    mk_b.button(text="No", callback_data="cancel")
    
    await state.set_state(EditTransaction.validate)
    
    from aiogram.enums import ParseMode
    
    await message.answer(msg, reply_markup=mk_b.as_markup(), parse_mode=ParseMode.MARKDOWN)



@router.message(Trip.name)
@checker_cancel
async def handle_trip_name(message: types.Message, state: FSMContext):
    logger.info("Trip name received - %s", message.from_user.id)
    
    await message.delete()
    
    name = message.text
    await state.update_data(name=name)
    
    msg = "Please enter the destination"
    await state.set_state(Trip.destination)
    await message.answer(msg)
    
@router.message(Trip.destination)
@checker_cancel
async def handle_trip_destination(message: types.Message, state: FSMContext):
    logger.info("Trip destination received - %s", message.from_user.id)
    
    await message.delete()
    
    destination = message.text
    await state.update_data(destination=destination)
    
    msg = "Please enter the date"
    await state.set_state(Trip.date)
    await message.answer(msg)
    
@router.message(Trip.date)
@checker_cancel
async def handle_trip_date(message: types.Message, state: FSMContext):
    logger.info("Trip date received - %s", message.from_user.id)
    
    await message.delete()
    
    date = message.text
    await state.update_data(date=date)
    
    msg = "Please enter the amount per person"
    await state.set_state(Trip.amount)
    await message.answer(msg)
    
@router.message(Trip.amount)
@checker_cancel
async def handle_trip_amount(message: types.Message, state: FSMContext):
    logger.info("Trip amount received - %s", message.from_user.id)
    
    await message.delete()
    
    amount = message.text
    await state.update_data(amount=amount)
    
    cache_data = await state.get_data()
    
    msg = f"Trip details:\n\nName: {cache_data['name']}\nDestination: {cache_data['destination']}\nDate: {cache_data['date']}\nAmount per person: {cache_data['amount']}"
    
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Yes", callback_data="validate_trip")
    mk_b.button(text="No", callback_data="cancel")
    
    await state.set_state(Trip.validate)
    await message.answer(msg, reply_markup=mk_b.as_markup())