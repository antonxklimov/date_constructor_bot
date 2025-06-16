import asyncio
import os
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from .handlers import router
import logging
from aiogram.storage import MemoryStorage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create global dispatcher instance
bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)

# Appwrite Function entry point
async def main(context):
    try:
        # Log request details for debugging
        context.log(f"Received request with method: {context.req.method}")
        context.log(f"Request path: {context.req.path}")
        # Appwrite passes request body as a dictionary, not a string
        request_body = context.req.body
        context.log(f"Request body raw: {request_body}")

        # Parse the JSON body into an aiogram Update object
        update = Update.model_validate(request_body)

        # Process the update using aiogram's dispatcher
        await dp.feed_update(bot, update)

        # Return a successful response to Telegram (Appwrite expects a response)
        return context.res.json({"status": "ok"})

    except Exception as e:
        # Log the error to Appwrite Console and return a 500 error
        context.error(f"Error during function execution: {e}")
        return context.res.json({"error": str(e)})
