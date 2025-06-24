from time import sleep
from aiogram import Router, types
from aiogram.filters.command import Command
from connection.database_con import *
from Finder.keyboards import keyboards as kb
from utils.logs import Log_Info

router = Router()

@router.message(Command('start'))
async def start(message: types.Message):
    add_user(telegram_name=message.from_user.username, telegram_id=message.from_user.id)
    await message.answer("Привет! Твоя анкета добавлена.", reply_markup=kb.main_keyboard)

    Log_Info.add_to_report(message.date, message.from_user.id, 'start')

@router.message(Command('help'))
async def help(message: types.Message) :
    await message.answer('Вот список команд в нашем боте\n'
                         '/start - добавляет вашу анкету в базу\n'
                         '/help - получить справку по камандам\n'
                         '/about - информация о боте и авторах\n'
                         '/more - получить список опцианальных программ\n'
                         '/roll - выпадает случайное число')

    Log_Info.add_to_report(message.date, message.from_user.id, 'help')

@router.message(Command('about'))
async def about(message: types.Message) :
    await message.answer('Бот делали - Kenny, Kiry\nИмитация бота для знакомств (Tinder-like)')

    Log_Info.add_to_report(message.date, message.from_user.id, 'about')

@router.message(Command('more'))
async def more(message : types.Message) :
    await message.answer('Вот список опциональных действий, которые может делать бот', reply_markup=kb.more_options_keyboard)

    Log_Info.add_to_report(message.date, message.from_user.id, 'more')

@router.message(Command('roll'))
async def roll(message : types.Message) :
    msg = await message.answer_dice()
    sleep(5)
    await message.answer(text=f'Выпавшее число {msg.dice.value}')

    Log_Info.add_to_report(message.date, message.from_user.id, 'roll')