import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers import start_handler, youtube_handler, instagram_handler, facebook_handler, error_handler
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import os
import dotenv

dotenv.load_dotenv()


# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 3000


async def on_startup(app: web.Application):
    # Set webhook on bot startup
    await bot.set_webhook(WEBHOOK_URL)
    
    
def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
    app.on_startup.append(on_startup)
    
    # Register routers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)
    # dp.include_router(tiktok_handler.router)

    # Run the web app
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)

if __name__ == "__main__":
    asyncio.run(main())
