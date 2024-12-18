import os
from dotenv import load_dotenv
import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.handlers import router


async def main():
    load_dotenv("env.env")
    bot = Bot(token=os.environ["TG_BOT_TOKEN"])
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
