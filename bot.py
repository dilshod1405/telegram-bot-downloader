import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers import start_handler, youtube_handler, instagram_handler, facebook_handler, error_handler
from aiohttp import web

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Set webhook for the bot
async def set_webhook():
    webhook_url = "https://telegram-bot-downloader.vercel.app/webhook"
    await bot.set_webhook(webhook_url)

# HTTP route to handle incoming webhook requests
async def handle(request):
    json_data = await request.json()  # Get the payload from Telegram
    update = types.Update(**json_data)
    await dp.process_update(update)  # Process the update with aiogram
    return web.Response(text="OK")

async def main():
    # Register routers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)
    
    # Set webhook
    await set_webhook()

    # Create an aiohttp web application
    app = web.Application()
    app.router.add_post("/webhook", handle)  # Handle webhook requests from Telegram
    
    # Run the app
    web.run_app(app, port=8000)

if __name__ == "__main__":
    asyncio.run(main())
