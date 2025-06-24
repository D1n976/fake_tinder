from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext

from connection.database_con import *
from Finder.keyboards import keyboards as kb
from aiogram import F

router = Router()

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
    await message.answer_photo(photo=types.FSInputFile(info[-1][7]), caption=ut.get_profile_str(info))
    await state.set_state(ut.BotStates.none)