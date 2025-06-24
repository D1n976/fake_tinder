import os
from aiogram import Bot, Dispatcher
from Messanger.handlers.handlers import router
import utils.utils as ut

async def run_bot():
    bot = Bot(token=ut.config['bot']['MESSANGER_BOT_TOKEN'])
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

async def remove_all_messages(bot, telegram_id) :
    if bot is None :
        return
    try:
        async for message in bot.iter_messages(telegram_id):
            await bot.delete_message(telegram_id, message.message_id)
        return True
    except Exception as e:
        print(f"Ошибка при удалении сообщений: {e}")
        return False
