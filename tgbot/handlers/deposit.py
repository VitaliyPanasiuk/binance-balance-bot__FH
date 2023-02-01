from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from tgbot.misc.states import check_password,overview,deposit
from magic_filter import F
from tgbot.config import password

from tgbot.misc.functions import generate_overview,generate_deposit

import time
import datetime
import requests
import asyncio

from tgbot.services.del_message import delete_message

from tgbot.keyboards.inlineBtn import CastomCallback
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

deposit_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

@deposit_router.message(commands=["deposit"])
async def user_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    print('handlet deposit')
    await bot.send_message(user_id, "Привет введи пароль")
    await state.set_state(deposit.password)

# @deposit_router.message_handler(content_types=types.ContentType.TEXT, state=deposit.password)
# async def test_start(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     text = message.text
#     print('in deposit')
#     if text == password:
#         await bot.send_message(user_id, "введите суму депосита(без usdt, просто число)")
#         await state.set_state(deposit.deposit)
#     else:
#         await bot.send_message(user_id, "wrong,try more")
#         await state.set_state(deposit.password)

@deposit_router.message_handler(content_types=types.ContentType.TEXT, state=deposit.password)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text == password:
        # await bot.send_message(user_id, "введите total value(BTC), без BTC и используя запятую")
        # await state.set_state(overview.total_btc)
        await bot.send_message(user_id, "Введите нужную тему(w - светлая, b - темная)")
        await state.set_state(deposit.theme)
    else:
        await bot.send_message(user_id, "wrong,try more")
        await state.set_state(deposit.password)
        
@deposit_router.message_handler(content_types=types.ContentType.TEXT, state=deposit.theme)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(theme=text.lower())
    await bot.send_message(user_id, "введите суму депосита(без usdt, просто число)")
    await state.set_state(deposit.deposit)
        
@deposit_router.message_handler(content_types=types.ContentType.TEXT, state=deposit.deposit)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(deposit=text)
    await bot.send_message(user_id, "введите дату в таком формате: 2022-10-14 18:51:00")
    await state.set_state(deposit.time_value)
    
@deposit_router.message_handler(content_types=types.ContentType.TEXT, state=deposit.time_value)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(time_value=text)
    data = await state.get_data()
    await generate_deposit(data['deposit'], data['time_value'],data['theme'])
    photo = FSInputFile('tgbot/misc/output_deposit.png')
    await bot.send_photo(user_id, photo)
