import asyncio
import os
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from .handlers import router

# Appwrite Function entry point
def main(context):
    try:
        # Log request details for debugging
        context.log(f"Received request with method: {context.req.method}")
        context.log(f"Request path: {context.req.path}")
        # Appwrite passes request body as a string, parse it as JSON
        request_body = context.req.body
        context.log(f"Request body raw: {request_body}")

        # Parse the JSON body into an aiogram Update object
        update_data = json.loads(request_body)
        update = Update.model_validate(update_data)

        # Initialize Bot and Dispatcher for each execution (stateless)
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise ValueError("BOT_TOKEN environment variable not set")

        bot = Bot(token=bot_token)
        dp = Dispatcher()
        dp.include_router(router)

        # Process the update using aiogram's dispatcher
        # Необходимо обернуть асинхронный вызов в asyncio.run для синхронной функции Appwrite
        asyncio.run(dp.process_update(update))

        # Return a successful response to Telegram (Appwrite expects a response)
        return context.res.json({"status": "ok"})

    except Exception as e:
        # Log the error to Appwrite Console and return a 500 error
        context.error(f"Error during function execution: {e}")
        return context.res.json({"error": str(e)}, status=500)
