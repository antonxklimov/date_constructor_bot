from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

def get_atmosphere_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вейкборд на причале")],
            [KeyboardButton(text="Водная прогулка")],
            [KeyboardButton(text="Бассейн и загар")],
            [KeyboardButton(text="Свой вариант")],
        ],
        resize_keyboard=True
    )

def get_activity_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новый Иерусалим")],
            [KeyboardButton(text="Три выставки")],
            [KeyboardButton(text="Третьяковка")],
            [KeyboardButton(text="Свой вариант")],
        ],
        resize_keyboard=True
    )

def get_final_touch_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="За Крышей")],
            [KeyboardButton(text="Bruno")],
            [KeyboardButton(text="Big Wine Freaks")],
            [KeyboardButton(text="Таби")],
            [KeyboardButton(text="Свой вариант")],
        ],
        resize_keyboard=True
    )

def get_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ого! Давай попробуем! 👀")]],
        resize_keyboard=True
    )

def get_date_keyboard():
    today = datetime.now()
    keyboard = []
    
    # Создаем кнопки для следующих 14 дней
    for i in range(14):
        date = today + timedelta(days=i)
        date_str = date.strftime("%d.%m.%Y")
        keyboard.append([KeyboardButton(text=date_str)])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
