import os
from aiogram import Bot, Dispatcher
from Messanger.handlers.handlers import router
import utils.utils as ut
async def run_bot():

    bot = Bot(token=ut.config['bot']['MESSANGER_BOT_TOKEN'])
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)
