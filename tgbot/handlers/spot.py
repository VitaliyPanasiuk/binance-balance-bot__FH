from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from tgbot.misc.states import check_password,overview,spot
from magic_filter import F
from tgbot.config import password

from tgbot.misc.functions import generate_overview,generate_spot

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

spot_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


@spot_router.message(commands=["spot"])
async def user_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Привет введи пароль")
    await state.set_state(spot.password)

@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.password)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text == password:
        await bot.send_message(user_id, "введите total value(BTC), без BTC и используя запятую")
        await state.set_state(spot.total_btc)
    else:
        await bot.send_message(user_id, "wrong,try more")
        await state.set_state(spot.password)
        
@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.total_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(total_btc=text)
    await bot.send_message(user_id, "введите total value(usd), без $ и ≈ и используя запятую")
    await state.set_state(spot.total_usd)
    
@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.total_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(total_usd=text)
    await bot.send_message(user_id, "введите pnl value(usd), без $ и ≈ и + и /, используя запятую")
    await state.set_state(spot.pnl_usd)
    
@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.pnl_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(pnl_usd=text)
    await bot.send_message(user_id, "введите pnl value(percent), без $ и ≈ и + и /, используя запятую")
    await state.set_state(spot.pnl_per)
    
@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.pnl_per)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(pnl_per=text)
    await bot.send_message(user_id, "введите usdt на балансе, без $ и ≈ и + и /, используя запятую")
    await state.set_state(spot.usdt)
    
@spot_router.message_handler(content_types=types.ContentType.TEXT, state=spot.usdt)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(usdt=text)
    data = await state.get_data()
    await generate_spot(str(data['total_btc']),str(data['total_usd']),str(data['pnl_usd']),str(data['pnl_per']),str(data['usdt']))
    photo = FSInputFile('tgbot/misc/output.png')
    await bot.send_photo(user_id, photo)