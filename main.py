import asyncio
import os
from aiogram import Bot, Dispatcher
# from config import BOT_TOKEN # Удаляем импорт config
from handlers import router

async def main():
    # Получаем BOT_TOKEN из переменных окружения
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN environment variable not set")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Получаем порт из переменной окружения Appwrite или используем 8000 по умолчанию
    webhook_port = int(os.getenv("PORT", 8000))

    await dp.start_webhook(
        webhook_path="/",
        on_startup=None,
        on_shutdown=None,
        skip_updates=True,
        host="0.0.0.0",
        port=webhook_port,
    )

if __name__ == "__main__":
    asyncio.run(main())
