from aiogram import Router, types, Bot
from aiogram.filters.command import Command

import utils as ut
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext

from utils.utils import BotStates
from connection.database_con import *
from Finder.keyboards import keyboards as kb
from aiogram import F

router = Router()

def get_profile_str(profile_info) :
        return f'Я {profile_info[-1][3]}, {profile_info[-1][8]}\n'\
               f'Живу в {profile_info[-1][-1]}\n'f'{profile_info[-1][6]}'
def is_user_valid(user) :
    return user[2] and user[3] and user[4] and user[5] and user[6] and user[7] and user[8]

@router.message(F.text.lower() == 'назад')
async def start(message: types.Message):
    await message.answer("Перемещаю в меню", reply_markup=kb.main_keyboard)


@router.message(F.text.lower() == 'мой профиль')
async def fill_profile(message: types.Message) :
    await message.reply(text='Настроить профиль', reply_markup=kb.profile_keyboard)


####################### Смена псевдонима ##################################
@router.message(F.text.lower() == 'настроить анкету')
async def change_user_name_request(message: types.Message, state : FSMContext) :
    await state.set_state(ut.BotStates.change_nick_state)
    await message.answer('Введите новый псевдоним')

@router.message(ut.BotStates.change_nick_state, F.text)
async def process_nick(message : types.Message, state : FSMContext) :
    nick = message.text
    if nick and nick != '' :
        update_user_name(message.from_user.id, nick)
        await message.answer('Сколько вам лет ?')
        await state.set_state(ut.BotStates.change_age)
    else :
        await message.answer('Ник пустой или введенные данные некоректные')
####################### Смена псевдонима ##################################

####################### Возраст ##################################
@router.message(ut.BotStates.change_age, F.text)
async def process_age(message : types.Message, state : FSMContext) :
    age = message.text
    if ut.is_number(age) :
        update_age(message.from_user.id, message.text)
        await message.answer('Где вы живете : ')
        await state.set_state(ut.BotStates.change_country)
####################### Возраст ##################################


####################### Страна ##################################
@router.message(ut.BotStates.change_country, F.text)
async def process_country(message : types.Message, state : FSMContext) :
    update_country(message.from_user.id, message.text)
    await message.answer('Прикрепите фото : ')
    await state.set_state(ut.BotStates.change_photo)

####################### Страна ##################################

####################### Смена фото ##################################
@router.message(ut.BotStates.change_photo)
async def process_photo(message : types.Message, state : FSMContext, bot : Bot) :
    if message.photo is None :
        await message.answer('Фото задано неправильно, попробуйте снова!')
        return
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
        update_genre(message.from_user.id, gen_num)
        await state.set_state(ut.BotStates.change_genre_like)
        await message.answer(f'Кого будем искать?\n{''.join([str(f"{x[0]} - {x[1]}\n") for x in get_genres()])}')
    else:
        await message.answer('Такого пола нет в списке\nПопробуйте снова')
####################### Смена пола ##################################


####################### Выбираем какой ленолиум нравится ##################################
@router.message(ut.BotStates.change_genre_like, F.text)
async def process_genre_like(message: types.Message, state : FSMContext) :
    # if not ut.is_number(message.text) :
    #     await message.answer('Такого пола нет в списке\nПопробуйте снова')
    #     return

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
async def look_at_me(message : types.Message, state : FSMContext) :
    info = get_full_info(telegram_id=message.from_user.id)
    await message.answer_photo(photo=types.FSInputFile(info[-1][7]), caption=get_profile_str(info))
    await state.set_state(ut.BotStates.none)

@router.message(F.text == 'Анкеты')
async def view_profile_reply(message : types.Message, state : FSMContext) :
    user = get_full_info(message.from_user.id)
    if not user or not user[0] or not is_user_valid(user[0]) :
        await message.answer('У вас не настроен профиль')
        return
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
        await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=f'У вас взаимная симпатия\n{get_profile_str(reacted_user)}\n',
                                   reply_markup=kb.create_message_bot_link(reacted_user[-1][1]))
        await bot.send_photo(reacted_user[-1][1], photo=types.FSInputFile(my_self_user[-1][7]), caption=f'У вас взаимная симпатия\n{get_profile_str(my_self_user)}',
                             reply_markup=kb.create_message_bot_link(my_self_user[-1][1]))
        return
    await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=get_profile_str(reacted_user),
                                   reply_markup=kb.viewing_profiles_keyboard)


@router.callback_query(F.data.startswith('liked_'))
async def handle_reply_to_like(call: types.CallbackQuery, state : FSMContext, bot : Bot) :
    sym = call.data.split('_')
    if sym[1] == 'show':
        await state.set_state(BotStates.reply_to_like)
        reacted_user = get_full_info(get_reacted_users(call.from_user.id)[-1][1])
        await call.message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=get_profile_str(reacted_user), reply_markup=kb.viewing_profiles_keyboard)
    elif sym[1] == 'unshow' :
        delete_request_likes(telegram_id=call.from_user.id)
        await state.set_state(ut.BotStates.none)

@router.callback_query(F.data.startswith('session_'))
async def handle_start_messanger(call: types.CallbackQuery) :
    parts = call.data.split("_")
    user = get_full_info(telegram_id=call.from_user.id)
    reacted_user = get_full_info(telegram_id=parts[2])
    if not user or not user[0] :
        return
    if not reacted_user or not reacted_user[0] :
        return
    remove_all_session_with(user[-1][0])
    if parts[1] == 'start':
        create_session(user[-1][0], reacted_user[-1][0])