import json

from aiogram import Router, types
from aiogram import F
from aiogram.filters.command import Command
import csv
import requests as r
import os
import requests

import Finder.weather_api.weater as weather
import Finder.keyboards.keyboards as kb
from Finder.data_counter.DataCounter import DataCounter

def get_opt(call_data) :
    data = call_data.split('_')
    return { 'action' : data[2]}

router = Router()

county_counter = DataCounter(cur_counter=0, counter_step=5, collection=weather.countries)
city_counter = DataCounter(cur_counter=0, counter_step=5, collection=[])

@router.message(Command("start"))
async def get_start(message: types.Message) :
    field_names = ['id', 'first-name', 'user_name']
    try :
        with open('usernames.csv', 'x', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
    except Exception:
        print('File exist')

    #save client info
    with open('usernames.csv', 'r+', encoding='utf-8') as csvfile:
        response = r.get(url=f'https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/getUpdates')
        user_data = response.json()['result'][-1]['message']['from']
        users = csv.DictReader(csvfile)
        if user_data['id'] not in [int(user['id']) for user in users] :
            info = dict({
                field_names[0]: user_data['id'],
                field_names[1]: f'{user_data['first_name']}',
                field_names[2]: f'{user_data['username']}'
            })
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writerow(info)

    await message.answer(text='Страны', reply_markup=kb.main_keyboard)

@router.message(F.text.lower() == 'получить погоду по списку стран')
async def get_weather_menu(message : types.Message) :
    await message.answer(text='Страны', reply_markup=kb.get_keyboard(counter=county_counter, key_board_opt="county_opt_"))

@router.message(F.text.lower() == 'получить кота')
async def get_cat(message : types.Message) :
    res = requests.get(url='https://cataas.com/cat')
    await message.answer_photo(photo=res.content)

@router.message(F.location)
async def get_weather_from_location(message : types.Message) :
    if message.location is not None :
        await message.answer(text=weather.get_weather_of_location(message.location.latitude, message.location.longitude))

@router.callback_query(F.data.startswith('county_opt_'))
async def county_opt_proc(call: types.CallbackQuery) :
    action = get_opt(call.data)['action']
    if action == 'back' or action == 'next' :
        if county_counter.change_counter(action) :
            await call.message.edit_text(text='Страны', reply_markup=kb.get_keyboard(counter=county_counter, key_board_opt="county_opt_"))
    else :
        city_counter.data = weather.city_by_country[action]
        await call.message.edit_text(text=f'Города {action}', reply_markup=kb.get_keyboard(counter=city_counter, key_board_opt='city_opt_'))

@router.callback_query(F.data.startswith('city_opt_'))
async def city_opt_proc(call: types.CallbackQuery) :
    action = get_opt(call.data)['action']
    if action == 'back' or action == 'next':
        if city_counter.change_counter(action):
            await call.message.edit_text(text='Страны', reply_markup=kb.get_keyboard(counter=city_counter,
                                                                                     key_board_opt="county_opt_"))
    else:
        await call.message.answer(text=f'{weather.get_weather_of_city(city=action)}')