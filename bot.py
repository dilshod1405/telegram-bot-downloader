import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers import start_handler, youtube_handler, instagram_handler, facebook_handler, error_handler

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def main():
    # Register routers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)
    # dp.include_router(tiktok_handler.router)

    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
