import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import router
from texts import TEXTS

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_reminders(bot):
    while True:
        await asyncio.sleep(28 * 24 * 60 * 60)  # 4 недели
        try:
            with open("users.txt", "r") as f:
                user_ids = set(line.strip() for line in f if line.strip())
            for user_id in user_ids:
                try:
                    await bot.send_message(user_id, TEXTS["reminder"])
                    logger.info(f"Sent reminder to user {user_id}")
                except Exception as e:
                    logger.error(f"Failed to send reminder to {user_id}: {e}")
        except Exception as e:
            logger.error(f"Failed to read users.txt: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    asyncio.create_task(send_reminders(bot))
    logger.info("Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
