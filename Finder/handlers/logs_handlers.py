from aiogram import F
import os.path
from aiogram import Router, types

router = Router()

@router.message(F.text, flags={"unhandled": True})
async def save_to_logs(message : types.Message) :
    log_info = f'{message.date}\n{message.from_user.id}\n{message.text}\n'
    if not os.path.exists(f'bot_logs/{message.from_user.id}_log') :
        with open(f'bot_logs/{message.from_user.id}_log', 'x', encoding='UTF-8') as f :
            f.write(log_info)
    else :
        with open(f'bot_logs/{message.from_user.id}_log', 'a', encoding='UTF-8') as f:
            f.write(log_info)
