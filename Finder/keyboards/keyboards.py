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

def create_message_bot_link(reacted_user_telegram_id) :
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать переписку", callback_data=f"session_start_{reacted_user_telegram_id}"),
        InlineKeyboardButton(text="Остановить переписку", callback_data=f"session_stop_{reacted_user_telegram_id}")],
        [InlineKeyboardButton(text='Перейти в бота', url='https://t.me/minimessenger_bot')]
    ])

more_options_keyboard = ReplyKeyboardMarkup(keyboard=
                                    [
                                        [KeyboardButton(text="Получить погоду по списку стран")],
                                        [KeyboardButton(text="Получить погоду по координатам", request_location=True)],
                                        [KeyboardButton(text="Получить кота")]
                                    ]
    , resize_keyboard=True)

def get_keyboard(counter, key_board_opt):
    inline_keyboard = [[InlineKeyboardButton(text=x, callback_data=f'{key_board_opt}{x}')]
                       for x in counter.get_data()]
    inline_keyboard.append([InlineKeyboardButton(text='Назад',callback_data=f'{key_board_opt}back'),
                            InlineKeyboardButton(text='Вперед', callback_data=f'{key_board_opt}next')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)