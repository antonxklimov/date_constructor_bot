from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

def get_atmosphere_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вейкборд с натуральным петнатом на причале", callback_data="atmo_1")],
        [InlineKeyboardButton(text="Водная прогулка на сапах или байдарках", callback_data="atmo_2")],
        [InlineKeyboardButton(text="Бассейн, солнце и новый московский загар", callback_data="atmo_3")],
        [InlineKeyboardButton(text="✨ Свой вариант", callback_data="custom_atmo")],
    ])

def get_activity_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поездка в Новый Иерусалим на выставку «Свет между мирами»", callback_data="act_1")],
        [InlineKeyboardButton(text="Прогулка имени трех выставок: Postrigay Gallery + AZ/ART + РосИЗО", callback_data="act_2")],
        [InlineKeyboardButton(text="Центр города. Новая Третьяковка. Борис Кустодиев", callback_data="act_3")],
        [InlineKeyboardButton(text="✨ Свой вариант", callback_data="custom_act")],
    ])

def get_final_touch_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="За Крышей", callback_data="final_1")],
        [InlineKeyboardButton(text="Bruno", callback_data="final_2")],
        [InlineKeyboardButton(text="Big Wine Freaks", callback_data="final_3")],
        [InlineKeyboardButton(text="Таби", callback_data="final_4")],
        [InlineKeyboardButton(text="✨ Свой вариант", callback_data="custom_final")],
    ])

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
        resize_keyboard=True,
        one_time_keyboard=True
    )
