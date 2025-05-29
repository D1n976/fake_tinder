from aiogram import Bot, Dispatcher
import os
from dotenv import *
import logging
from Finder.handlers.handlers import router
import Finder.utils.utils as ut


async def start_bot():

    load_dotenv(find_dotenv())
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('FINDER_BOT_TOKEN'))
    dp = Dispatcher(storage=ut.storage)
    dp.include_router(router)

    await dp.start_polling(bot)
