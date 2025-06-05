from aiogram import Bot, Dispatcher
import Finder.handlers.handlers as handlers
import utils.utils as ut
import Finder.handlers.commands as commands
import Finder.handlers.weather_handlers as wh

async def start_bot():

    bot = Bot(token=ut.config['bot']['FINDER_BOT_TOKEN'])
    dp = Dispatcher(storage=ut.storage)
    dp.include_router(handlers.router)
    dp.include_router(commands.router)
    dp.include_router(wh.router)
    await dp.start_polling(bot)