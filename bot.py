import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiohttp import web
from config import TELEGRAM_BOT_TOKEN
from handlers import start_handler, youtube_handler, instagram_handler, facebook_handler, error_handler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(youtube_router)
dp.include_router(instagram_router)
dp.include_router(facebook_router)
dp.include_router(error_router)

async def on_start(request):
    return web.Response(text="Bot is running")

# Main function for ASGI app
async def app(scope, receive, send):
    if scope['type'] == 'http':
        response = await on_start(request=None)
        await send({
            'type': 'http.response',
            'status': 200,
            'headers': [(b'content-type', b'text/plain')],
            'body': response.body
        })
    else:
        await send({
            'type': 'http.response',
            'status': 404,
            'body': b'Not Found'
        })

# Main bot entry point for polling
async def start_bot():
    await dp.start_polling(bot)

async def main():
    # Start the bot with polling
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    # ASGI app logic
    return web.Application(handler=app)

# For local testing
if __name__ == "__main__":
    from aiohttp import web
    web.run_app(main())
