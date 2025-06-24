from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile

import Finder.handlers.handlers as handlers
import utils.utils as ut
import utils.logs as logs
import Finder.handlers.commands as commands
import Finder.handlers.weather_handlers as wh
from apscheduler.schedulers.asyncio import *
import Finder.handlers.logging as log

bot = Bot(token=ut.config['bot']['FINDER_BOT_TOKEN'])
dp = Dispatcher(storage=ut.storage)

async def send_daily_report(bot_, admins_id):
    report_file = logs.Log_Info.generate_report()
    [await bot_.send_document(
        chat_id = x,
        document=FSInputFile(path=report_file, filename="Отчет.pdf"),
        caption="Ежедневный отчет"
    ) for x in admins_id]

async def on_startup():
    scheduler_ = AsyncIOScheduler()
    scheduler_.start()
    scheduler_.add_job(send_daily_report, 'cron', hour=9, minute=0, args=[bot, ut.config['bot']['ADMINS'].split('|')])

async def start_bot():
    dp.startup.register(on_startup)

    dp.include_router(handlers.router)
    dp.include_router(commands.router)
    dp.include_router(wh.router)
    dp.include_router(log.router)

    await dp.start_polling(bot)