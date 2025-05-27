from aiogram import Router, types, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.filters.command import Command, CommandObject
from datetime import datetime

from pyexpat.errors import messages

import Finder.utils.utils as ut
import os
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext
from io import BytesIO

from aiogram.types import InputFile, InlineKeyboardMarkup

from Finder.utils.utils import BotStates
from connection.database_con import *
from Finder.keyboards import keyboards as kb
from aiogram import F

router = Router()

def get_profile_str(profile_info) :
        return f'Я {profile_info[-1][3]}, {profile_info[-1][8]}\n'\
               f'Живу в {profile_info[-1][-1]}\n'f'{profile_info[-1][6]}'

@router.message(F.text.lower() == 'назад')
async def start(message: types.Message):
    await message.answer("Перемещаю в меню", reply_markup=kb.main_keyboard)

@router.message(Command('start'))
async def start(message: types.Message):
    add_user(telegram_name=message.from_user.username, telegram_id=message.from_user.id)
    await message.answer("Привет! Твоя анкета добавлена.", reply_markup=kb.main_keyboard)

@router.message(F.text.lower() == 'мой профиль')
async def fill_profile(message: types.Message) :
    await message.reply(text='Привет', reply_markup=kb.profile_keyboard)


####################### Смена псевдонима ##################################
@router.message(F.text.lower() == 'настроить анкету')
async def change_user_name_request(message: types.Message, state : FSMContext) :
    await state.set_state(ut.BotStates.change_nick_state)
    await message.answer('Введите новый псевдоним')

@router.message(ut.BotStates.change_nick_state, F.text)
async def process_nick(message : types.Message, state : FSMContext) :
    update_user_name(message.from_user.id, message.text)
    await message.answer('Сколько вам лет ?')
    await state.set_state(ut.BotStates.change_age)
####################### Смена псевдонима ##################################

####################### Возраст ##################################
@router.message(ut.BotStates.change_age, F.text)
async def process_age(message : types.Message, state : FSMContext) :
    update_age(message.from_user.id, message.text)
    await message.answer('Где вы живете : ')
    await state.set_state(ut.BotStates.change_country)
####################### Возраст ##################################


####################### Страна ##################################
@router.message(ut.BotStates.change_country, F.text)
async def process_age(message : types.Message, state : FSMContext) :
    update_country(message.from_user.id, message.text)
    await message.answer('Прикрепите фото : ')
    await state.set_state(ut.BotStates.change_photo)

####################### Страна ##################################

####################### Смена фото ##################################
@router.message(ut.BotStates.change_photo, F.photo)
async def process_photo(message : types.Message, state : FSMContext, bot : Bot) :
    # await state.set_state(BotStates.none)
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    local_filename = f"user_photos/{message.from_user.id}.jpg"
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    update_user_photo(message.from_user.id, str(local_filename))

    await bot.download_file(file_path, destination=local_filename)
    await message.answer("Фото сохранено!")
    await state.set_state(ut.BotStates.change_description)
    await message.answer('Введите описание : ')
####################### Смена фото ##################################


####################### Смена описания ##################################
@router.message(ut.BotStates.change_description, F.text)
async def process_description(message : types.Message, state : FSMContext) :
    # await state.set_state(BotStates.none)
    update_user_description(message.from_user.id, message.text)
    await message.answer('Описание успешно обновлено : ')
    await state.set_state(ut.BotStates.change_genre)
    await message.answer(f'Выберите cвой пол из списка : \n{''.join([str(f"{x[0]} - {x[1]}\n") for x in get_genres()])}')


####################### Смена описания ##################################


####################### Смена пола (На ленолиум меняем) ##################################
@router.message(ut.BotStates.change_genre, F.text)
async def process_genre(message: types.Message, state : FSMContext) :
    genre_map = {int(x[0]) : x[1] for x in get_genres()}
    gen_num = int(message.text.strip())
    if genre_map.get(gen_num) :
        # await state.set_state(BotStates.none)
        update_genre(message.from_user.id, gen_num)
        await state.set_state(ut.BotStates.change_genre_like)
        await message.answer(f'Кого будем искать?\n{''.join([str(f"{x[0]} - {x[1]}\n") for x in get_genres()])}')
    else:
        await message.answer('Такого пола нет в списке\nПопробуйте снова')
####################### Смена пола ##################################


####################### Выбираем какой ленолиум нравится ##################################
@router.message(ut.BotStates.change_genre_like, F.text)
async def process_genre_like(message: types.Message, state : FSMContext) :
    genre_map = {int(x[0]): x[1] for x in get_genres()}
    gen_num = int(message.text.strip())
    if genre_map.get(gen_num) :
        await  state.set_state(ut.BotStates.none)
        update_genre_like(telegram_id=message.from_user.id, genre_like_id=gen_num)
        await message.answer('Анкета успешно настроена!')
    else :
        await message.answer('Такого пола нет в списке\nПопробуйте снова')
####################### Выбираем какой ленолиум нравится ##################################

@router.message(F.text.lower() == 'о себе')
async def look_at_me(message : types.Message) :
    info = get_full_info(telegram_id=message.from_user.id)
    await message.answer_photo(photo=types.FSInputFile(info[-1][7]), caption=get_profile_str(info))

@router.message(F.text == 'Анкеты')
async def view_profile_reply(message : types.Message, state : FSMContext) :
    user_profile = get_profile_of_selected_user(message.from_user.id)
    if user_profile and user_profile[0] :
        await message.answer_photo(photo=types.FSInputFile(user_profile[-1][7]), caption=get_profile_str(user_profile), reply_markup=kb.viewing_profiles_keyboard)
    else :
        next_user = get_next_profile(message.from_user.id)
        if next_user and next_user[0]:
            await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=get_profile_str(next_user),
                                       reply_markup=kb.viewing_profiles_keyboard)
    await state.set_state(ut.BotStates.none)

@router.message(lambda msg: msg.text in ["❤️ Лайк", "❌ Пропустить"], ut.BotStates.none)
async def handle_vote_like(message: types.Message, bot : Bot, state : FSMContext) :
    is_like = True if message.text == '❤️ Лайк' else False
    info = request_user_like(message.from_user.id, is_like)
    if is_like :
        liked_user = info['liked_user'][0]
        await bot.send_message(liked_user[1], 'Кому-то понравилась ваша анкет\nПосмотреть', reply_markup=kb.get_choice_to_view_liked_users())
        await (FSMContext(storage=ut.storage, key=StorageKey(bot_id=bot.id, user_id=liked_user[1], chat_id=liked_user[1]))
                       .set_state(BotStates.show_liked_people))
    next_user = get_next_profile(message.from_user.id)
    if next_user and next_user[0]:
        await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=get_profile_str(next_user), reply_markup=kb.viewing_profiles_keyboard)
    await state.set_state(ut.BotStates.none)

@router.message(lambda msg: msg.text in ["❤️ Лайк", "❌ Пропустить"], ut.BotStates.reply_to_like)
async def handle_reply_to_like(message : types.Message, state : FSMContext, bot : Bot) :
    liked_users = get_reacted_users(message.from_user.id)
    if not liked_users :
        await state.set_state(BotStates.none)
        next_user = get_next_profile(message.from_user.id)
        if next_user and next_user[0]:
            await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=get_profile_str(next_user), reply_markup=kb.viewing_profiles_keyboard)
        return

    reacted_user = get_full_info(liked_users[-1][1])
    my_self_user = get_full_info(message.from_user.id)
    is_liked = True if message.text == '❤️ Лайк' else False
    react_to_like(my_self_user[-1][0], reacted_user[-1][0], is_liked)
    if is_liked:
        session_id = create_session(my_self_user[0][0], reacted_user[0][0])
        await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=f'У вас взаимная симпатия\n{get_profile_str(reacted_user)}\n',
                                   reply_markup=kb.create_message_bot_link(session_id))
        await bot.send_photo(reacted_user[-1][1], photo=types.FSInputFile(my_self_user[-1][7]), caption=f'У вас взаимная симпатия\n{get_profile_str(my_self_user)}',
                             reply_markup=kb.create_message_bot_link(session_id))
        return

    await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=get_profile_str(reacted_user),
                                   reply_markup=kb.viewing_profiles_keyboard)


@router.callback_query(F.data.startswith('liked_'))
async def handle_reply_to_like(call: types.CallbackQuery, state : FSMContext) :
    sym = call.data.split('_')
    if sym[1] == 'show':
        await state.set_state(BotStates.reply_to_like)
        reacted_user = get_full_info(get_reacted_users(call.from_user.id)[-1][1])
        await call.message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=get_profile_str(reacted_user), reply_markup=kb.viewing_profiles_keyboard)
    elif sym[1] == 'unshow' :
        await state.set_state(ut.BotStates.none)

@router.callback_query(F.data.startswith('session_'))
async def handle_start_messanger(call: types.CallbackQuery, bot: Bot) :
    parts = call.data.split("_")
    session_id, action = parts[1], parts[2]
    is_session_request_to_readiness = (action == 'start')

    session = get_session(session_id)
    first_user = get_full_info_with_user_id(session[1])
    second_user = get_full_info_with_user_id(session[2])

    if first_user[1] == call.message.from_user.id:
        confirm_user_readiness(session, first_user[0], is_session_request_to_readiness)
        user_to_request = second_user
        selected_user = first_user
    elif second_user[1] == call.message.from_user.id:
        confirm_user_readiness(session, first_user[1], is_session_request_to_readiness)
        user_to_request = first_user
        selected_user = second_user
    else:
        await call.message.answer("Вы не участвуете в этой сессии.")
        return

    if not user_to_request:
        await call.message.answer("Не удалось определить собеседника.")
        return

    if is_session_request_to_readiness:
        await bot.send_message(
            user_to_request[1],
            text=f"Пользователь {selected_user[3]} присоединился к чату",
            reply_markup=kb.create_message_bot_link(session_id)
        )
        await call.message.answer(
            text=f'Вы присоединились к чату c {user_to_request[3]}',
            reply_markup=kb.create_message_bot_link(session_id)
        )
    else:
        await bot.send_message(
            user_to_request[1],
            text=f"Пользователь {selected_user[3]} вышел из чата",
            reply_markup=kb.create_message_bot_link(session_id)
        )
        await call.message.answer(
            text=f'Вы вышли из чата c {user_to_request[3]}',
            reply_markup=kb.viewing_profiles_keyboard
        )