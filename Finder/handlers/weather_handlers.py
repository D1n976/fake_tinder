from aiogram import Router, types
from aiogram import F
import requests

import Finder.weather_api.weater as weather
import Finder.keyboards.keyboards as kb
from Finder.data_counter.DataCounter import DataCounter

def get_opt(call_data) :
    data = call_data.split('_')
    return { 'action' : data[2]}

router = Router()

county_counter = DataCounter(cur_counter=0, counter_step=5, collection=weather.get_countries())
city_counter = DataCounter(cur_counter=0, counter_step=5, collection=[])

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
    country = get_opt(call.data)['action']
    if country == 'back' or country == 'next' :
        if county_counter.change_counter(country) :
            await call.message.edit_text(text='Страны', reply_markup=kb.get_keyboard(counter=county_counter, key_board_opt="county_opt_"))
    else :
        city_counter.data = weather.get_city_by_country(country)
        await call.message.edit_text(text=f'Города {country}', reply_markup=kb.get_keyboard(counter=city_counter, key_board_opt='city_opt_'))

@router.callback_query(F.data.startswith('city_opt_'))
async def city_opt_proc(call: types.CallbackQuery) :
    city = get_opt(call.data)['action']
    if city == 'back' or city == 'next':
        if city_counter.change_counter(city):
            await call.message.edit_text(text='Страны', reply_markup=kb.get_keyboard(counter=city_counter,
                                                                                     key_board_opt="county_opt_"))
    else:
        await call.message.answer(text=f'{weather.get_weather_of_city(city=city)}')