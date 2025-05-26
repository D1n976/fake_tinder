from aiogram import Bot, Dispatcher
import os
from dotenv import *
import logging
import asyncio
from handlers.handlers import router
import utils.utils as ut

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('FINDER_BOT_TOKEN'))
dp = Dispatcher(storage=ut.storage)
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())