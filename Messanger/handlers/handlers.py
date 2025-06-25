from aiogram import Router, types, Bot
from connection.database_con import *
from aiogram import F
import os

router = Router()

@router.message(F.content_type.in_(['text', 'photo', 'document', 'voice', 'video', 'audio', 'sticker']))
async def forward_message(message: types.Message, bot : Bot) :
    user = get_full_info(message.from_user.id)
    if not user or not user[0] :
        return

    session = get_session(user[-1][0])
    print(session)
    if not session or not session[0] :
        return

    to_user = get_full_info_with_user_id(session[-1][1])
    reversed_session = get_session(to_user[-1][0])
    if not reversed_session or not reversed_session[0] :
        return

    await bot.send_message(to_user[-1][1], text=f'{user[-1][3]}\n{message.text}')

    path = f'bot_logs/dialog_{message.from_user.id}_with_{to_user[-1][1]}_log'
    log_info = f'{message.date}\n{message.from_user.id}\n{message.text}\n'
    if not os.path.exists(path) :
        with open(path, 'x', encoding='UTF-8') as f :
            f.write(log_info)
    else :
        with open(path, 'a', encoding='UTF-8') as f:
            f.write(log_info)

