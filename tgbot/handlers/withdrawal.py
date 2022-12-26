from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from tgbot.misc.states import check_password,overview,deposit,withdrawal
from magic_filter import F
from tgbot.config import password

from tgbot.misc.functions import generate_overview,generate_deposit,generate_withdrawal

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

withdrawal_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

@withdrawal_router.message(commands=["withdrawal"])
async def user_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Привет введи пароль")
    await state.set_state(withdrawal.password)

@withdrawal_router.message_handler(content_types=types.ContentType.TEXT, state=withdrawal.password)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text == password:
        await bot.send_message(user_id, "введите суму депосита(без usdt, просто число)")
        await state.set_state(withdrawal.deposit)
    else:
        await bot.send_message(user_id, "wrong,try more")
        await state.set_state(withdrawal.password)
        
@withdrawal_router.message_handler(content_types=types.ContentType.TEXT, state=withdrawal.deposit)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(deposit=text)
    await bot.send_message(user_id, "введите дату в таком формате: 2022-10-14 18:51:00")
    await state.set_state(withdrawal.time_value)
    
@withdrawal_router.message_handler(content_types=types.ContentType.TEXT, state=withdrawal.time_value)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(time_value=text)
    data = await state.get_data()
    await generate_withdrawal(data['deposit'],data['time_value'])
    photo = FSInputFile('tgbot/misc/output.png')
    await bot.send_photo(user_id, photo)