import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from config import TELEGRAM_BOT_TOKEN
from aiohttp import web

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Webhook handling
async def handle(request):
    json_data = await request.json()
    try:
        update = types.Update(**json_data)
        await dp.process_update(update)
    except Exception as e:
        logging.error(f"Error processing update: {e}")
    return web.Response(text="OK")

# Example of a loop with try/except block
async def start_bot():
    while True:
        try:
            logging.info("Starting bot polling...")
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Error occurred while polling: {e}")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

async def main():
    # Register routers with the dispatcher
    dp.include_router(start_handler.router)
    dp.include_router(youtube_handler.router)
    dp.include_router(instagram_handler.router)
    dp.include_router(facebook_handler.router)
    dp.include_router(error_handler.router)

    # Start the bot
    try:
        await bot.set_webhook("https://telegram-bot-downloader.vercel.app/webhook")
    except Exception as e:
        logging.error(f"Error setting webhook: {e}")

    # Set up aiohttp web application
    app = web.Application()
    app.router.add_post("/webhook", handle)

    # Run app
    try:
        logging.info("Starting the web app...")
        web.run_app(app, port=8000)
    except Exception as e:
        logging.error(f"Error running the web app: {e}")

if __name__ == "__main__":
    asyncio.run(main())
