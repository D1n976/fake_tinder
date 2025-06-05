from aiogram import Router, types, Bot
from connection.database_con import *
from aiogram import F

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

    #Проверяем, общается ли с нами другой человек
    to_user = get_full_info_with_user_id(session[-1][1])
    reversed_session = get_session(to_user[-1][0])
    if not reversed_session or not reversed_session[0] :
        return

    #Если все нормально, пересылаем ему сообщения
    await bot.send_message(to_user[-1][1], text=f'{user[-1][3]}\n{message.text}')


