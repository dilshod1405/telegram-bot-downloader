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

# Define the main function for the bot (without web)
async def start_bot():
    # Start polling (for handling Telegram updates)
    await dp.start_polling(bot)

async def set_webhook():
    webhook_url = "https://telegram-bot-downloader.vercel.app/webhook"
    await bot.set_webhook(webhook_url)

async def handle_request(request):
    # You can handle the HTTP requests here if necessary
    return web.Response(text="Bot is up and running")

# This function is required for serverless functions to work in Vercel
async def app(request):
    # For demonstration, simply handle the request and show a response
    return await handle_request(request)

async def main():
    # Register routers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)

    # Start the bot (you can also run it in a background task)
    app = web.Application()
    app.router.add_get("/", app)  # Optional: Root endpoint for testing
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    web.run_app(app, port=8000)

if __name__ == "__main__":
    asyncio.run(main())

# This is the handler function that Vercel expects
# It will ensure the function runs properly in the serverless environment
handler = app
