import os
import json
import logging
import time
from typing import Dict, Any
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from .handlers import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set or empty")

# Получение ID администратора из переменных окружения
ADMIN_ID = os.getenv("ADMIN_ID")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID environment variable not set or empty")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание и настройка роутера
router = Router()
register_handlers(router)
dp.include_router(router)

async def main(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Основная функция для обработки запросов от Telegram.
    
    Args:
        context: Контекст выполнения функции, содержащий request и response объекты.
        
    Returns:
        Dict[str, Any]: Ответ с результатом выполнения.
    """
    start_time = time.time()
    try:
        # Получение тела запроса
        request_body = context.get("request", {}).get("body", "")
        logger.info(f"Received request body: {request_body}")
        logger.info(f"Request processing started at: {start_time}")
        
        # Проверка на пустой запрос (для scheduled executions)
        if not request_body:
            logger.info("Empty request body received, likely a scheduled execution. Returning 200 OK.")
            return context["response"].json(
                {"status": "success", "message": "Scheduled execution completed"},
                status=200
            )
        
        # Парсинг JSON из тела запроса
        try:
            update_data = json.loads(request_body)
            logger.info(f"Parsed update data: {update_data}")
            logger.info(f"JSON parsing took: {time.time() - start_time:.2f} seconds")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return context["response"].json(
                {"status": "error", "message": f"Invalid JSON: {str(e)}"},
                status=400
            )
        
        # Создание объекта Update
        try:
            update = Update.model_validate(update_data)
            logger.info(f"Created Update object: {update}")
            logger.info(f"Update object creation took: {time.time() - start_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to create Update object: {e}")
            return context["response"].json(
                {"status": "error", "message": f"Invalid update data: {str(e)}"},
                status=400
            )
        
        # Обработка обновления
        try:
            logger.info("Starting update processing...")
            await dp.feed_update(bot, update)
            logger.info("Update processed successfully")
            logger.info(f"Total processing time: {time.time() - start_time:.2f} seconds")
            return context["response"].json(
                {"status": "success", "message": "Update processed successfully"},
                status=200
            )
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            logger.error(f"Error occurred after: {time.time() - start_time:.2f} seconds")
            return context["response"].json(
                {"status": "error", "message": f"Error processing update: {str(e)}"},
                status=500
            )
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(f"Unexpected error occurred after: {time.time() - start_time:.2f} seconds")
        return context["response"].json(
            {"status": "error", "message": f"Unexpected error: {str(e)}"},
            status=500
        )
