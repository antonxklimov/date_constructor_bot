import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_webhook(
        webhook_path="/",
        on_startup=None,
        on_shutdown=None,
        skip_updates=True,
        host="0.0.0.0",
        port=8000,
    )

if __name__ == "__main__":
    asyncio.run(main())
