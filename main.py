import asyncio
import logging
import time
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
        try:
            now = int(time.time())
            updated_lines = []
            with open("users.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        user_id, last_ts = parts[0], int(parts[1])
                    else:
                        user_id, last_ts = parts[0], 0
                    if now - last_ts >= 28 * 24 * 60 * 60:
                        try:
                            await bot.send_message(user_id, TEXTS["reminder"])
                            logger.info(f"Sent reminder to user {user_id}")
                            updated_lines.append(f"{user_id}:{now}\n")
                        except Exception as e:
                            logger.error(f"Failed to send reminder to {user_id}: {e}")
                            updated_lines.append(line)
                    else:
                        updated_lines.append(line)
            with open("users.txt", "w") as f:
                f.writelines(updated_lines)
        except Exception as e:
            logger.error(f"Failed to process reminders: {e}")
        await asyncio.sleep(24 * 60 * 60)  # Проверять раз в сутки

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