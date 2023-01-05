from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from PIL import Image, ImageDraw, ImageFont

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

import datetime
import asyncio

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
# bot2 = Bot(token=config.tg_bot.token2, parse_mode="HTML")

# base = psycopg2.connect(
#     dbname=config.db.database,
#     user=config.db.user,
#     password=config.db.password,
#     host=config.db.host,
# )
# cur = base.cursor()

async def generate_overview(data):
	try:
		im = Image.open('tgbot/misc/overview.png')
		ravno = Image.open('tgbot/misc/ravno.png')
		inf = Image.open('tgbot/misc/i.png')
		btc = Image.open('tgbot/misc/btc.png')

		
		data['total_usd'] += ' $'
		data['spot_usd'] += ' $'
		data['funding_usd'] += ' $'
		data['cross_matgin_usd'] += ' $'
		data['isolated_usd'] += ' $'
		data['usdtm_usd'] += ' $'
		data['coin_usd'] += ' $'
		data['earn_usd'] += ' $'	
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=29)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(20, 205),
			data['total_btc'].lower(),
			font=font,
			fill='#e1e4eb')	
		font = ImageFont.truetype(
				'tgbot/misc/binance2.ttf', size=15)
		im.paste(ravno, (21, 257))
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(35, 255),
			data['total_usd'].lower(),
			font=font,
			fill='#6f7680')
		im.paste(inf, (40 + int(font.getsize(data['total_usd'])[0]), 251))	
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['spot_btc'])[0]-68, 520),
			data['spot_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 516), mask=btc.convert('RGBA'))	
		if data['spot_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['spot_usd'])[0]-32, 550))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['spot_usd'])[0]-16, 550),
				data['spot_usd'].lower(),
				font=font,
				fill='#6f7680')	
		# 
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['funding_btc'])[0]-68, 614),
			data['funding_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 610), mask=btc.convert('RGBA'))	
		if data['funding_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['funding_usd'])[0]-32, 644))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['funding_usd'])[0]-16, 644),
				data['funding_usd'].lower(),
				font=font,
				fill='#6f7680')	
		# cross_matgin_usd
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['cross_matgin_btc'])[0]-68, 697),
			data['cross_matgin_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 693), mask=btc.convert('RGBA'))	
		if data['cross_matgin_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['cross_matgin_usd'])[0]-32, 727))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['cross_matgin_usd'])[0]-16, 727),
				data['cross_matgin_usd'].lower(),
				font=font,
				fill='#6f7680')	
		# isolated_usd
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['isolated_btc'])[0]-68, 780),
			data['isolated_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 776), mask=btc.convert('RGBA'))	
		if data['isolated_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['isolated_usd'])[0]-32, 810))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['isolated_usd'])[0]-16, 810),
				data['isolated_usd'].lower(),
				font=font,
				fill='#6f7680')	
		# usdtm-btc
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['usdtm_btc'])[0]-68, 863),
			data['usdtm_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 859), mask=btc.convert('RGBA'))	
		if data['usdtm_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['usdtm_usd'])[0]-32, 893))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['usdtm_usd'])[0]-16, 893),
				data['usdtm_usd'].lower(),
				font=font,
				fill='#6f7680')
		# coin-btc
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['coin_btc'])[0]-68, 946),
			data['coin_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 942), mask=btc.convert('RGBA'))	
		if data['coin_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['coin_usd'])[0]-32, 976))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['coin_usd'])[0]-16, 976),
				data['coin_usd'].lower(),
				font=font,
				fill='#6f7680')	
		# earn-btc
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(im)
		draw_lev.text(
			(591-font.getsize(data['earn_btc'])[0]-68, 1029),
			data['earn_btc'],
			font=font,
			fill='#e1e4eb')
		im.paste(btc, (530, 1025), mask=btc.convert('RGBA'))	
		if data['earn_usd'] != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			im.paste(ravno, (591-font.getsize(data['earn_usd'])[0]-32, 1059))
			draw_lev = ImageDraw.Draw(im)
			draw_lev.text(
				(591-font.getsize(data['earn_usd'])[0]-16, 1059),
				data['earn_usd'].lower(),
				font=font,
				fill='#6f7680')	
		im.save('tgbot/misc/output_overview.png')
	except:
		pass


async def generate_deposit(deposit_value,time_value):
	try:
		im = Image.open('tgbot/misc/overview.png')
		deposit = Image.open('tgbot/misc/deposit.png')
		ravno = Image.open('tgbot/misc/ravno.png')
		inf = Image.open('tgbot/misc/i.png')
		btc = Image.open('tgbot/misc/btc.png')
		usdt = Image.open('tgbot/misc/usdt.png')
		adres = Image.open('tgbot/misc/adres.png')
		txid = Image.open('tgbot/misc/txid.png')
		tr = Image.open('tgbot/misc/tr.png')
		colon = Image.open('tgbot/misc/colon.png')

		time_value2 = time_value.split(' ')
		tm_date = time_value2[0]
		tm_time = time_value2[1]
		tm_date = tm_date.split('-')
		tm_time = tm_time.split(':')


		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(394, 763),
			tm_date[0],
			font=font,
			fill='#e1e4eb')
		deposit.paste(tr, (394+int(font.getsize(tm_date[0])[0])+2, 768), mask=tr.convert('RGBA'))

		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(394+int(font.getsize(tm_date[0])[0])+10, 763),
			tm_date[1],
			font=font,
			fill='#e1e4eb')
		deposit.paste(tr, (394+int(font.getsize(tm_date[0])[0])+10+int(font.getsize(tm_date[1])[0])+2, 768), mask=tr.convert('RGBA'))

		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(394+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+20, 763),
			tm_date[2],
			font=font,
			fill='#e1e4eb')

		# new date
		width_for_time = 394+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+int(font.getsize(tm_date[2])[0])+27
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(width_for_time, 763),
			tm_time[0],
			font=font,
			fill='#e1e4eb')
		deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+3, 764), mask=colon.convert('RGBA'))

		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(width_for_time+int(font.getsize(tm_time[0])[0])+9, 763),
			tm_time[1],
			font=font,
			fill='#e1e4eb')
		deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+9+int(font.getsize(tm_time[1])[0])+3, 764), mask=colon.convert('RGBA'))

		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(width_for_time+int(font.getsize(tm_time[0])[0])+int(font.getsize(tm_time[1])[0])+18, 763),
			tm_time[2],
			font=font,
			fill='#e1e4eb')


		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=28)
		draw_lev = ImageDraw.Draw(deposit)
		draw_lev.text(
			(int(296-((int(font.getsize(deposit_value)[0]) + 8 + 54)/2)), 228),
			deposit_value,
			font=font,
			fill='#e1e4eb')
		deposit.paste(usdt, (int(296-((int(font.getsize(deposit_value)[0]) + 8 + 54)/2) + int(font.getsize(deposit_value)[0]) + 8), 231), mask=usdt.convert('RGBA'))
		# deposit.paste(usdt, (256+int(font.getsize(deposit_value)[0])+8, 231), mask=usdt.convert('RGBA'))
		deposit.paste(adres, (225, 591), mask=adres.convert('RGBA'))
		deposit.paste(txid, (225, 663), mask=txid.convert('RGBA'))


		deposit.save('tgbot/misc/output_deposit.png')
	except:
		pass
 
 
async def generate_withdrawal(deposit_value,time_value):
	try:
		im = Image.open('tgbot/misc/overview.png')
		deposit = Image.open('tgbot/misc/deposit.png')
		wt = Image.open('tgbot/misc/withdrawal.png')
		ravno = Image.open('tgbot/misc/ravno.png')
		inf = Image.open('tgbot/misc/i.png')
		btc = Image.open('tgbot/misc/btc.png')
		usdt = Image.open('tgbot/misc/usdt.png')
		adres = Image.open('tgbot/misc/adres.png')
		txid = Image.open('tgbot/misc/txid.png')
		tr = Image.open('tgbot/misc/tr.png')
		colon = Image.open('tgbot/misc/colon.png')

		time_value2 = time_value.split(' ')
		tm_date = time_value2[0]
		tm_time = time_value2[1]
		tm_date = tm_date.split('-')
		tm_time = tm_time.split(':')

		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(394, 838),
			tm_date[0],
			font=font,
			fill='#e1e4eb')
		wt.paste(tr, (394+int(font.getsize(tm_date[0])[0])+2, 843), mask=tr.convert('RGBA'))
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(394+int(font.getsize(tm_date[0])[0])+10, 838),
			tm_date[1],
			font=font,
			fill='#e1e4eb')
		wt.paste(tr, (394+int(font.getsize(tm_date[0])[0])+10+int(font.getsize(tm_date[1])[0])+2, 843), mask=tr.convert('RGBA'))
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(394+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+20, 838),
			tm_date[2],
			font=font,
			fill='#e1e4eb')
		# new date
		width_for_time = 394+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+int(font.getsize(tm_date[2])[0])+27
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(width_for_time, 838),
			tm_time[0],
			font=font,
			fill='#e1e4eb')
		wt.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+3, 839), mask=colon.convert('RGBA'))
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(width_for_time+int(font.getsize(tm_time[0])[0])+9, 838),
			tm_time[1],
			font=font,
			fill='#e1e4eb')
		wt.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+9+int(font.getsize(tm_time[1])[0])+3, 839), mask=colon.convert('RGBA'))
		font = ImageFont.truetype(
			'tgbot/misc/binance2.ttf', size=14)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(width_for_time+int(font.getsize(tm_time[0])[0])+int(font.getsize(tm_time[1])[0])+18, 838),
			tm_time[2],
			font=font,
			fill='#e1e4eb')


		font = ImageFont.truetype(
					'tgbot/misc/binance.ttf', size=28)
		draw_lev = ImageDraw.Draw(wt)
		draw_lev.text(
			(int(296-((int(font.getsize(deposit_value)[0]) + 8 + 54)/2)), 228),
			deposit_value,
			font=font,
			fill='#e1e4eb')
		wt.paste(usdt, (int(296-((int(font.getsize(deposit_value)[0]) + 8 + 54)/2) + int(font.getsize(deposit_value)[0]) + 8), 231), mask=usdt.convert('RGBA'))
		wt.paste(adres, (225, 617), mask=adres.convert('RGBA'))
		wt.paste(txid, (225, 691), mask=txid.convert('RGBA'))
		wt.save('tgbot/misc/output_withdrawal.png')

	except:
		pass

async def generate_spot(total_btc,total_usd,pnl_usd,pnl_per,usdt_spot):
	try:
		im = Image.open('tgbot/misc/overview.png')
		deposit = Image.open('tgbot/misc/deposit.png')
		wt = Image.open('tgbot/misc/withdrawal.png')
		spot = Image.open('tgbot/misc/spot.png')
		ravno = Image.open('tgbot/misc/ravno.png')
		inf = Image.open('tgbot/misc/i.png')
		btc = Image.open('tgbot/misc/btc.png')
		usdt = Image.open('tgbot/misc/usdt.png')
		adres = Image.open('tgbot/misc/adres.png')
		txid = Image.open('tgbot/misc/txid.png')
		tr = Image.open('tgbot/misc/tr.png')
		colon = Image.open('tgbot/misc/colon.png')
		per = Image.open('tgbot/misc/per.png')
		slash = Image.open('tgbot/misc/slash.png')
		plus = Image.open('tgbot/misc/plus.png')
		ar = Image.open('tgbot/misc/ar.png')
		dol = Image.open('tgbot/misc/dol.png')

		total_usd += ' $'

		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=29)
		draw_lev = ImageDraw.Draw(spot)
		draw_lev.text(
			(20, 205),
			total_btc.lower(),
			font=font,
			fill='#e1e4eb')	
		font = ImageFont.truetype(
				'tgbot/misc/binance2.ttf', size=15)
		spot.paste(ravno, (21, 257))
		draw_lev = ImageDraw.Draw(spot)
		draw_lev.text(
			(35, 255),
			total_usd.lower(),
			font=font,
			fill='#6f7680')

		spot.paste(plus, (21, 333), mask=plus.convert('RGBA'))
		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(spot)
		draw_lev.text(
			(32, 332),
			pnl_usd.lower(),
			font=font,
			fill='#e1e4eb')

		spot.paste(dol, (32 + font.getsize(pnl_usd)[0] + 8, 328), mask=dol.convert('RGBA'))
		spot.paste(slash, (32 + font.getsize(pnl_usd)[0] + 20, 330), mask=slash.convert('RGBA'))
		spot.paste(plus, (32 + font.getsize(pnl_usd)[0] + 30, 333), mask=plus.convert('RGBA'))

		font = ImageFont.truetype(
				'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(spot)
		draw_lev.text(
			(32 + font.getsize(pnl_usd)[0] + 41, 332),
			pnl_per.lower(),
			font=font,
			fill='#e1e4eb')

		spot.paste(per, (32 + font.getsize(pnl_usd)[0] + 41 + font.getsize(pnl_per)[0] + 7, 328), mask=per.convert('RGBA'))
		spot.paste(ar, (32 + font.getsize(pnl_usd)[0] + 41 + font.getsize(pnl_per)[0] + 47, 328), mask=ar.convert('RGBA'))


		font = ImageFont.truetype(
						'tgbot/misc/binance.ttf', size=17)
		draw_lev = ImageDraw.Draw(spot)
		draw_lev.text(
			(591-font.getsize(usdt_spot)[0]-22, 672),
			usdt_spot,
			font=font,
			fill='#e1e4eb')

		usdt_spot += ' $'
		if usdt_spot != '0,00 $':
			font = ImageFont.truetype(
					'tgbot/misc/binance2.ttf', size=13)
			draw_lev = ImageDraw.Draw(spot)
			draw_lev.text(
				(591-font.getsize(usdt_spot)[0]-18, 698),
				usdt_spot.lower(),
				font=font,
				fill='#6f7680')	


		spot.save('tgbot/misc/output_spot.png')

	except:
		pass