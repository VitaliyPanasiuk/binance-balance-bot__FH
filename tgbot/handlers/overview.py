from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from tgbot.misc.states import check_password,overview
from magic_filter import F
from tgbot.config import password

from tgbot.misc.functions import generate_overview

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

overview_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

# base = psycopg2.connect(
#     dbname=config.db.database,
#     user=config.db.user,
#     password=config.db.password,
#     host=config.db.host,
# )
# cur = base.cursor()

    
@overview_router.message(commands=["overview"])
async def user_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Привет введи пароль")
    await state.set_state(overview.password)

@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.password)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text == password:
        # await bot.send_message(user_id, "введите total value(BTC), без BTC и используя запятую")
        # await state.set_state(overview.total_btc)
        await bot.send_message(user_id, "Введите нужную тему(w - светлая, b - темная)")
        await state.set_state(overview.theme)
    else:
        await bot.send_message(user_id, "wrong,try more")
        await state.set_state(overview.password)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.theme)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(theme=text.lower())
    await bot.send_message(user_id, "введите total value(BTC), без BTC и используя запятую")
    await state.set_state(overview.total_btc)
    
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.total_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(total_btc=text)
    await bot.send_message(user_id, "введите total value(usd), без $ и ≈ и используя запятую")
    await state.set_state(overview.total_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.total_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(total_usd=text)
    await bot.send_message(user_id, "введите spot value(BTC), без BTC и используя запятую")
    await state.set_state(overview.spot_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.spot_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(spot_btc=text)
    await bot.send_message(user_id, "введите spot value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.spot_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.spot_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(spot_usd=text)
    await bot.send_message(user_id, "введите funding value(BTC), без BTC и используя запятую")
    await state.set_state(overview.funding_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.funding_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(funding_btc=text)
    await bot.send_message(user_id, "введите funding value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.funding_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.funding_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(funding_usd=text)
    await bot.send_message(user_id, "введите cross margin value(BTC), без BTC и используя запятую")
    await state.set_state(overview.cross_matgin_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.cross_matgin_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(cross_matgin_btc=text)
    await bot.send_message(user_id, "введите cross margin value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.cross_matgin_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.cross_matgin_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(cross_matgin_usd=text)
    await bot.send_message(user_id, "введите isolated margin value(BTC), без BTC и используя запятую")
    await state.set_state(overview.isolated_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.isolated_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(isolated_btc=text)
    await bot.send_message(user_id, "введите isolated margin value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.isolated_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.isolated_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(isolated_usd=text)
    await bot.send_message(user_id, "введите usd-m futures value(BTC), без BTC и используя запятую")
    await state.set_state(overview.usdtm_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.usdtm_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(usdtm_btc=text)
    await bot.send_message(user_id, "введите usd-m futures value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.usdtm_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.usdtm_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(usdtm_usd=text)
    await bot.send_message(user_id, "введите coin-m futures value(BTC), без BTC и используя запятую")
    await state.set_state(overview.coin_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.coin_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(coin_btc=text)
    await bot.send_message(user_id, "введите coin-m futures value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.coin_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.coin_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(coin_usd=text)
    await bot.send_message(user_id, "введите earn value(BTC), без BTC и используя запятую")
    await state.set_state(overview.earn_btc)
        
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.earn_btc)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(earn_btc=text)
    await bot.send_message(user_id, "введите coin-m futures value(usd), без $ и ≈ и используя запятую, если должно быть пусто напишите 0,00. Используйте два знака после запятой")
    await state.set_state(overview.earn_usd)
    
@overview_router.message_handler(content_types=types.ContentType.TEXT, state=overview.earn_usd)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.update_data(earn_usd=text)
    data = await state.get_data()
    await generate_overview(data)
    photo = FSInputFile('tgbot/misc/output_overview.png')
    await bot.send_photo(user_id, photo)