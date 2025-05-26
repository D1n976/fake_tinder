import os
from aiogram import Bot, Dispatcher
import asyncpg
import asyncio
from dotenv import *
import logging

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

# API_TOKEN = 'BOT2_TOKEN'
# DATABASE_URL = 'postgresql://user:password@localhost/dbname'
#
bot = Bot(token=os.getenv('MESSANGER_BOT_TOKEN'))
dp = Dispatcher()

# conn: asyncpg.Connection = None
#
# @dp.message(commands=['start_session'])
# async def start_session(message: types.Message):
#     parts = message.text.split()
#     if len(parts) == 3:
#         user1, user2 = int(parts[1]), int(parts[2])
#         await conn.execute(
#             "INSERT INTO sessions (user1_id, user2_id) VALUES ($1, $2)", user1, user2
#         )
#         await bot.send_message(user1, "Чат создан! Напишите что-нибудь.")
#         await bot.send_message(user2, "Чат создан! Напишите что-нибудь.")
#
# @dp.message_handler()
# async def relay_message(message: types.Message):
#     user_id = message.from_user.id
#     session = await conn.fetchrow(
#         "SELECT * FROM sessions WHERE user1_id = $1 OR user2_id = $1",
#         user_id
#     )
#     if session:
#         recipient = session['user2_id'] if session['user1_id'] == user_id else session['user1_id']
#         await bot.send_message(recipient, f"Сообщение от собеседника:\n{message.text}")
#
# @dp.message_handler(commands=['end'])
# async def end_chat(message: types.Message):
#     user_id = message.from_user.id
#     await conn.execute(
#         "DELETE FROM sessions WHERE user1_id = $1 OR user2_id = $1",
#         user_id
#     )
#     await message.answer("Чат завершён.")
#
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
