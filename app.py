import asyncio

from config import ADMIN_ID
from loader import bot
from database import create_db


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await asyncio.sleep(5)
    await bot.send_message(ADMIN_ID, "Я запущен!")
    await create_db()

if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
