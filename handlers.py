from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from datetime import datetime
import os
import logging
import time

# from config import ADMIN_ID # Удаляем импорт config
from .states import DateConstructorStates # Изменено на относительный импорт
from .keyboards import ( # Изменено на относительный импорт
    get_atmosphere_keyboard,
    get_activity_keyboard,
    get_final_touch_keyboard,
    get_start_keyboard,
    get_date_keyboard,
)

router = Router()

# Получаем ADMIN_ID из переменных окружения
admin_id_str = os.getenv("ADMIN_ID")
if not admin_id_str:
    raise ValueError("ADMIN_ID environment variable not set or empty")
ADMIN_ID = int(admin_id_str) # Конвертируем в int, так как ID число

# Словари соответствий для текстов кнопок
ATMOSPHERE_TEXTS = {
    "atmo_1": "на вейкборд с натуральным петнатом на причале",
    "atmo_2": "на водную прогулку на сапах или байдарках",
    "atmo_3": "в бассейн, за солнцем и новым московским загаром",
}
ACTIVITY_TEXTS = {
    "act_1": "поездка в Новый Иерусалим на выставку «Свет между мирами»",
    "act_2": "прогулка имени трех выставок: Postrigay Gallery + AZ/ART + РосИЗО",
    "act_3": "центр города. Новая Третьяковка. Борис Кустодиев",
}
FINAL_TOUCH_TEXTS = {
    "final_1": "За Крышей",
    "final_2": "Bruno",
    "final_3": "Big Wine Freaks",
    "final_4": "Таби",
}
MONTHS = {
    "01": "января", "02": "февраля", "03": "марта", "04": "апреля", "05": "мая", "06": "июня",
    "07": "июля", "08": "августа", "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"
}

# Настройка логирования
logger = logging.getLogger(__name__)

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    start_time = time.time()
    logger.info(f"Processing /start command from user {message.from_user.id}")
    try:
        await message.answer(
            "Привет! Я — конструктор свиданий <b>Date Day 2025</b> 🚧\n\n"
            "Я помогу собрать идеальное свидание в несколько шагов. Просто выбирай, что тебе нравится, а я расскажу Антону.",
            reply_markup=get_start_keyboard(),
            parse_mode="HTML"
        )
        await state.clear()
        logger.info(f"/start command processed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        raise

@router.message(F.text == "Ого! Давай попробуем! 👀")
async def start_steps(message: Message, state: FSMContext):
    start_time = time.time()
    logger.info(f"Processing 'Ого! Давай попробуем! 👀' from user {message.from_user.id}")
    try:
        await message.answer("Отлично! Давай начнем.", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            "<b>Часть 1. Утро.</b>\n\n"
            "Можно проснуться либо рано, либо поздно, но хочется какой-то активности (завтрак в модном месте включен):",
            reply_markup=get_atmosphere_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(DateConstructorStates.atmosphere)
        logger.info(f"'Ого! Давай попробуем! 👀' processed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error in 'Ого! Давай попробуем! 👀': {e}")
        raise

@router.callback_query(F.data.startswith("atmo_"))
async def process_atmosphere_selection(callback: CallbackQuery, state: FSMContext):
    await state.update_data(atmosphere=callback.data)
    await callback.message.edit_text(
        "<b>Шаг 2. День.</b>\n\n"
        "Нужно пропитаться искусством и периодически делать привалы на бокальчик:",
        reply_markup=get_activity_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.activity)
    await callback.answer()

@router.callback_query(F.data.startswith("act_"))
async def process_activity_selection(callback: CallbackQuery, state: FSMContext):
    await state.update_data(activity=callback.data)
    await callback.message.edit_text(
        "<b>Шаг 3. Вечер.</b>\n\n"
        "Нагулялись, пора и серьезно поесть:",
        reply_markup=get_final_touch_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.final_touch)
    await callback.answer()

@router.callback_query()
async def process_final_touch(callback: CallbackQuery, state: FSMContext):
    logger.info(f"Received callback data: {callback.data}")
    if callback.data.startswith("final_"):
        await state.update_data(final_touch=callback.data)
        await callback.message.edit_text(
            "<b>Шаг 4. Выбор даты.</b>\n\n"
            "📅 Выбери дату:",
            reply_markup=get_date_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(DateConstructorStates.date)
    elif callback.data == "custom_final":
        await callback.message.edit_text(
            "Напиши, куда бы ты хотел(а) пойти вечером:"
        )
        await state.set_state(DateConstructorStates.custom_final_touch)
    await callback.answer()

@router.callback_query(DateConstructorStates.date)
async def process_date(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith("date_"):
        return
    
    date = callback.data[5:]  # Убираем префикс "date_"
    await state.update_data(date=date)
    data = await state.get_data()
    
    # Получаем текстовые значения для каждого выбора
    atmo_text = ATMOSPHERE_TEXTS.get(data.get("atmosphere", ""), data.get("atmosphere"))
    activity_text = ACTIVITY_TEXTS.get(data.get("activity", ""), data.get("activity"))
    final_touch_text = FINAL_TOUCH_TEXTS.get(data.get("final_touch", ""), data.get("final_touch"))
    
    # Формируем итоговый текст
    final_text = (
        f"Мы просыпаемся <b>{date}</b> и отправляемся <b>{atmo_text}</b>.\n"
        f"После этого идем <b>{activity_text}</b>.\n"
        f"А вечером нас ждет <b>{final_touch_text}</b>."
    )
    
    await callback.message.edit_text(
        final_text,
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "custom_atmo")
async def process_custom_atmosphere(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напиши, куда бы ты хотел(а) пойти утром:"
    )
    await state.set_state(DateConstructorStates.custom_atmosphere)
    await callback.answer()

@router.message(DateConstructorStates.custom_atmosphere)
async def process_custom_atmosphere_text(message: Message, state: FSMContext):
    await state.update_data(atmosphere=message.text)
    await message.answer(
        "<b>Шаг 2. День.</b>\n\n"
        "Нужно пропитаться искусством и периодически делать привалы на бокальчик:",
        reply_markup=get_activity_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.activity)

@router.callback_query(F.data == "custom_act")
async def process_custom_activity(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напиши, куда бы ты хотел(а) пойти днем:"
    )
    await state.set_state(DateConstructorStates.custom_activity)
    await callback.answer()

@router.message(DateConstructorStates.custom_activity)
async def process_custom_activity_text(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.answer(
        "<b>Шаг 3. Вечер.</b>\n\n"
        "Нагулялись, пора и серьезно поесть:",
        reply_markup=get_final_touch_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.final_touch)

@router.message(DateConstructorStates.custom_final_touch)
async def process_custom_final_touch_text(message: Message, state: FSMContext):
    await state.update_data(final_touch=message.text)
    await message.answer(
        "<b>Шаг 4. Выбор даты.</b>\n\n"
        "📅 Выбери дату:",
        reply_markup=get_date_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.date)
