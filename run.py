import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers.user import router
from app.handlers.admin import admin
from app.database.models import create_base


async def main():

    await create_base()
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router, admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
