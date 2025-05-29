import os
from aiogram import Bot, Dispatcher
from dotenv import *
import logging
from Messanger.handlers.handlers import router

async def run_bot():

    load_dotenv(find_dotenv())
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('MESSANGER_BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)
