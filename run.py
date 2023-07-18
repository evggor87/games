import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers.user import router
from app.handlers.admin import admin
from app.database.models import create_base

async def main():

    logging.basicConfig(level=logging.INFO)
    await create_base()
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router, admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
