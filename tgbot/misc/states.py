from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup


class exmple_state(StatesGroup):
    name = State()
    age = State()
    
class check_password(StatesGroup):
    password = State()

class overview(StatesGroup):
    password = State()
    theme = State()
    total_btc = State()
    total_usd = State()
    spot_usd = State()
    spot_btc = State()
    funding_btc = State()
    funding_usd = State()
    cross_matgin_btc = State()
    cross_matgin_usd = State()
    isolated_btc = State()
    isolated_usd = State()
    usdtm_btc = State()
    usdtm_usd = State()
    coin_btc = State()
    coin_usd = State()
    earn_btc = State()
    earn_usd = State()
    
class deposit(StatesGroup):
    password = State()
    theme = State()
    deposit = State()
    time_value = State()
class withdrawal(StatesGroup):
    password = State()
    theme = State()
    deposit = State()
    time_value = State()
class spot(StatesGroup):
    password = State()
    theme = State()
    total_btc = State()
    total_usd = State()
    pnl_usd = State()
    pnl_per = State()
    usdt = State()