from aiogram import Router, types, Bot

import utils as ut
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext

from utils.utils import BotStates
from connection.database_con import *
from Finder.keyboards import keyboards as kb
from aiogram import F

router = Router()

@router.message(F.text == 'Анкеты')
async def view_profile_reply(message : types.Message, state : FSMContext) :
    user = get_full_info(message.from_user.id)
    if not user or not user[0] or not ut.is_user_valid(user[0]) :
        await message.answer('У вас не настроен профиль')
        return
    user_profile = get_profile_of_selected_user(message.from_user.id)
    if user_profile and user_profile[0] and ut.is_user_valid(user_profile[0]):
        await message.answer_photo(photo=types.FSInputFile(user_profile[-1][7]), caption=ut.get_profile_str(user_profile), reply_markup=kb.viewing_profiles_keyboard)
    else :
        next_user = get_next_profile(message.from_user.id)
        if next_user and next_user[0]:
            await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=ut.get_profile_str(next_user),
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
        await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=ut.get_profile_str(next_user), reply_markup=kb.viewing_profiles_keyboard)
    await state.set_state(ut.BotStates.none)

@router.message(lambda msg: msg.text in ["❤️ Лайк", "❌ Пропустить"], ut.BotStates.reply_to_like)
async def handle_reply_to_like(message : types.Message, state : FSMContext, bot : Bot) :
    liked_users = get_reacted_users(message.from_user.id)
    if not liked_users :
        await state.set_state(BotStates.none)
        next_user = get_next_profile(message.from_user.id)
        if next_user and next_user[0]:
            await message.answer_photo(photo=types.FSInputFile(next_user[-1][7]), caption=ut.get_profile_str(next_user), reply_markup=kb.viewing_profiles_keyboard)
        return

    reacted_user = get_full_info(liked_users[-1][1])
    my_self_user = get_full_info(message.from_user.id)
    is_liked = True if message.text == '❤️ Лайк' else False
    react_to_like(my_self_user[-1][0], reacted_user[-1][0], is_liked)
    if is_liked:
        await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=f'У вас взаимная симпатия\n{ut.get_profile_str(reacted_user)}\n',
                                   reply_markup=kb.create_message_bot_link(reacted_user[-1][1]))
        await bot.send_photo(reacted_user[-1][1], photo=types.FSInputFile(my_self_user[-1][7]), caption=f'У вас взаимная симпатия\n{ut.get_profile_str(my_self_user)}',
                             reply_markup=kb.create_message_bot_link(my_self_user[-1][1]))
        return
    await message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=ut.get_profile_str(reacted_user),
                                   reply_markup=kb.viewing_profiles_keyboard)


@router.callback_query(F.data.startswith('liked_'))
async def handle_reply_to_like(call: types.CallbackQuery, state : FSMContext, bot : Bot) :
    sym = call.data.split('_')
    if sym[1] == 'show':
        await state.set_state(BotStates.reply_to_like)
        reacted_user = get_full_info(get_reacted_users(call.from_user.id)[-1][1])
        await call.message.answer_photo(photo=types.FSInputFile(reacted_user[-1][7]), caption=ut.get_profile_str(reacted_user), reply_markup=kb.viewing_profiles_keyboard)
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
    else :
        await stop_session(user)