from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
from texts import BUTTONS

def get_atmosphere_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Вейкборд и петнат на причале"),
                KeyboardButton(text="Сапы или байдарки по реке")
            ],
            [
                KeyboardButton(text="Открытый бассейн и московский загар"),
                KeyboardButton(text="Свой вариант →")
            ],
        ],
        resize_keyboard=True
    )

def get_activity_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Новый Иерусалим. Свет между мирами"),
                KeyboardButton(text="Postrigay Gallery + AZ/ART + РосИЗО")
            ],
            [
                KeyboardButton(text="Новая Третьяковка. Борис Кустодиев."),
                KeyboardButton(text="Свой вариант →")
            ],
        ],
        resize_keyboard=True
    )

def get_final_touch_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="За Крышей"),
                KeyboardButton(text="Bruno")
            ],
            [
                KeyboardButton(text="Big Wine Freaks"),
                KeyboardButton(text="таби")
            ],
            [
                KeyboardButton(text="Свой вариант →")
            ],
        ],
        resize_keyboard=True
    )

def get_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ого! Давай попробуем! 👀")]],
        resize_keyboard=True
    )

def get_final_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Запланировать еще одно свидание?")]],
        resize_keyboard=True
    )

def get_date_keyboard():
    today = datetime.now()
    keyboard = []
    
    # Создаем кнопки для следующих 14 дней в формате 2x2
    row = []
    for i in range(14):
        date = today + timedelta(days=i)
        date_str = date.strftime("%d.%m.%Y")
        row.append(KeyboardButton(text=date_str))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:  # Добавляем оставшуюся кнопку, если она есть
        keyboard.append(row)
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
