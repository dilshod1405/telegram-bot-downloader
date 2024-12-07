import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from config import TELEGRAM_BOT_TOKEN
from handlers import start_handler, youtube_handler, instagram_handler, facebook_handler, error_handler

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Define the main function for the bot
async def start_bot():
    # Start polling (to handle Telegram updates)
    await dp.start_polling(bot)

async def set_webhook():
    webhook_url = "https://telegram-bot-downloader.vercel.app/webhook"
    await bot.set_webhook(webhook_url)

# Vercel requires an 'app' or 'handler' function. Let's define 'app'.
async def handle_request(request):
    return web.Response(text="Bot is up and running")

# This function will handle the HTTP request. It's required for Vercel.
async def app(request):
    # Simple HTTP response when a request hits the serverless function
    return web.Response(text="Bot is up and running!")

# Vercel uses 'handler' or 'app' to manage serverless function behavior.
# We need to make sure Vercel can find 'handler' or 'app'
handler = app

async def main():
    # Register handlers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)

    # Start the bot in the background
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    # Set up the web app to listen for incoming HTTP requests
    app = web.Application()
    app.router.add_get("/", app)  # Optional: root endpoint to check bot status
    web.run_app(app, port=8000)

# This block is needed for running the bot locally or as a background task.
if __name__ == "__main__":
    asyncio.run(main())

