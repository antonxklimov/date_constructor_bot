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

@router.callback_query(DateConstructorStates.atmosphere)
async def process_atmosphere(callback: CallbackQuery, state: FSMContext):
    await state.update_data(atmosphere=callback.data)
    await callback.message.edit_text(
        "<b>Шаг 2. День.</b>\n\n"
        "Нужно пропитаться искусством и периодически делать привалы на бокальчик:",
        reply_markup=get_activity_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.activity)
    await callback.answer()

@router.callback_query(DateConstructorStates.activity)
async def process_activity(callback: CallbackQuery, state: FSMContext):
    await state.update_data(activity=callback.data)
    await callback.message.edit_text(
        "<b>Шаг 3. Вечер.</b>\n\n"
        "Нагулялись, пора и серьезно поесть:",
        reply_markup=get_final_touch_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.final_touch)
    await callback.answer()

@router.callback_query(DateConstructorStates.final_touch)
async def process_final_touch(callback: CallbackQuery, state: FSMContext):
    await state.update_data(final_touch=callback.data)
    await callback.message.edit_text(
        "<b>Шаг 4. Выбор даты.</b>\n\n"
        "📅 Выбери удобную дату для свидания:",
        parse_mode="HTML"
    )
    await callback.message.answer(
        reply_markup=get_date_keyboard()
    )
    await state.set_state(DateConstructorStates.date)
    await callback.answer()

@router.message(DateConstructorStates.date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("🧘‍♀️ Есть ли что-то, что ты хочешь добавить или предложить?")
    await state.set_state(DateConstructorStates.comment)

@router.message(DateConstructorStates.comment)
async def process_comment(message: Message, state: FSMContext, bot):
    await state.update_data(comment=message.text)
    data = await state.get_data()

    # Преобразуем дату в формат '21 июня'
    date_str = data.get('date', '')
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        day = date_obj.day
        month = MONTHS[date_obj.strftime("%m")]
        date_text = f"{day} {month}"
    except Exception:
        date_text = date_str

    # Получаем тексты по callback_data
    atmo_text = ATMOSPHERE_TEXTS.get(data.get('atmosphere'), data.get('atmosphere'))
    act_text = ACTIVITY_TEXTS.get(data.get('activity'), data.get('activity'))
    final_touch = FINAL_TOUCH_TEXTS.get(data.get('final_touch'), data.get('final_touch'))

    # Добавляем дополнительные сообщения в зависимости от выбора
    additional_atmo_text = ""
    if data.get('atmosphere') == "atmo_1":
        additional_atmo_text = " Натуральное игристое открывается сразу после катера."
    elif data.get('atmosphere') == "atmo_2":
        additional_atmo_text = " Петнат будет и здесь, но из рюкзака и прямо на воде."
    elif data.get('atmosphere') == "atmo_3":
        additional_atmo_text = " Здесь игристое запрещено, поэтому оно нас ждет чуть позже."

    additional_final_text = ""
    if data.get('final_touch') == "final_1":
        additional_final_text = " Отличный выбор, современная классика и креветки с малиной."
    elif data.get('final_touch') == "final_2":
        additional_final_text = " Вижу, что хочется мяса."
    elif data.get('final_touch') == "final_3":
        additional_final_text = " Идем исследовать нэтти."
    elif data.get('final_touch') == "final_4":
        additional_final_text = " Давно не были, пора выпить саке!"

    text = (
        "Ура! ✨\n\n"
        f"Мы просыпаемся {date_text} и отправляемся <b>{atmo_text}</b>.{additional_atmo_text}\n"
        f"Немного устаем, но сможем вдохнуть в себя силы искусством — нас ждет <b>{act_text}</b>.\n"
        f"Финальной точкой дня становится <b>{final_touch}</b>.{additional_final_text} А дальше смотрим куда нас заведет этот вечер. До встречи!\n\n"
        "💕 👀\n\n"
        "<i>PS. На протяжении всего дня мы подпитываемся не только искусством, но и совершаем приятные привалы с пивом или вином. Без этого никак!</i>"
    )
    
    # Отправляем красивое сообщение пользователю
    await message.answer(text, parse_mode="HTML")

    # Отправляем результаты админу
    admin_text = (
        f"📅 Новое свидание!\n\n"
        f"От пользователя: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"<b>Дата:</b> {date_text}\n"
        f"<b>Утро:</b> {atmo_text}{additional_atmo_text}\n"
        f"<b>День:</b> {act_text}\n"
        f"<b>Вечер:</b> {final_touch}{additional_final_text}\n"
        f"<b>Комментарий:</b> {message.text}"
    )
    await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    
    await state.clear()

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

@router.callback_query(F.data == "custom_final")
async def process_custom_final_touch(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напиши, куда бы ты хотел(а) пойти вечером:"
    )
    await state.set_state(DateConstructorStates.custom_final_touch)
    await callback.answer()

@router.message(DateConstructorStates.custom_final_touch)
async def process_custom_final_touch_text(message: Message, state: FSMContext):
    await state.update_data(final_touch=message.text)
    await message.answer(
        "<b>Шаг 4. Выбор даты.</b>\n\n"
        "📅 Выбери удобную дату для свидания:",
        parse_mode="HTML"
    )
    await message.answer(
        reply_markup=get_date_keyboard()
    )
    await state.set_state(DateConstructorStates.date)
