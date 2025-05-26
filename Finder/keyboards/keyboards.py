from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=
                                    [
                                        [KeyboardButton(text='Анкеты')],
                                        [KeyboardButton(text='Мой профиль')]
                                    ],
    resize_keyboard=True)
profile_keyboard = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton(text='Настроить анкету')],
    [KeyboardButton(text='О себе')],
    [KeyboardButton(text='Назад')]
], resize_keyboard=True)

viewing_profiles_keyboard = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton(text="❤️ Лайк"), KeyboardButton(text='❌ Пропустить')],
    [KeyboardButton(text='Назад')]
],
    resize_keyboard=True)

def get_choice_to_view_liked_users() :
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Да", callback_data="liked_show"),
        InlineKeyboardButton(text="Нет", callback_data="liked_unshow")
    )
    return builder.as_markup()

def create_message_bot_link(message_id) : return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перейти в переписку", url="https://t.me/my_helper_bot", callback_data=f'session_{message_id}')]
])