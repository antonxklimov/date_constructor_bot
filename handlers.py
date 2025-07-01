from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import os
import logging
import time

from config import ADMIN_ID
from states import DateConstructorStates
from keyboards import (
    get_atmosphere_keyboard,
    get_activity_keyboard,
    get_final_touch_keyboard,
    get_start_keyboard,
    get_date_keyboard,
    get_final_keyboard,
    get_date_offer_keyboard,
)
from texts import ATMOSPHERE_TEXTS, ACTIVITY_TEXTS, FINAL_TOUCH_TEXTS, MONTHS, TEXTS, DATE_OFFER_TEXT, DATE_OFFER_BUTTONS, DATE_OFFER_REPLY

router = Router()

# Настройка логирования
logger = logging.getLogger(__name__)

def save_user_id(user_id):
    try:
        user_id = str(user_id)
        updated = False
        lines = []
        try:
            with open("users.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if parts[0] == user_id:
                        lines.append(f"{user_id}:{parts[1] if len(parts)>1 else '0'}\n")
                        updated = True
                    else:
                        lines.append(line)
        except FileNotFoundError:
            pass
        if not updated:
            lines.append(f"{user_id}:0\n")
        with open("users.txt", "w") as f:
            f.writelines(lines)
    except Exception as e:
        logger.error(f"Failed to save user_id: {e}")

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    save_user_id(message.from_user.id)
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

@router.message(StateFilter(DateConstructorStates.atmosphere))
async def process_atmosphere_selection(message: Message, state: FSMContext):
    if message.text == "Свой вариант →":
        await message.answer(
            "Напиши, куда бы ты хотел(а) пойти утром:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(DateConstructorStates.custom_atmosphere)
        return

    await state.update_data(atmosphere=message.text)
    await message.answer(
        "<b>Шаг 2. День.</b>\n\n"
        "Нужно пропитаться искусством и периодически делать привалы на бокальчик:",
        reply_markup=get_activity_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.activity)

@router.message(StateFilter(DateConstructorStates.activity))
async def process_activity_selection(message: Message, state: FSMContext):
    if message.text == "Свой вариант →":
        await message.answer(
            "Напиши, куда бы ты хотел(а) пойти днем:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(DateConstructorStates.custom_activity)
        return

    await state.update_data(activity=message.text)
    await message.answer(
        "<b>Шаг 3. Вечер.</b>\n\n"
        "Нагулялись, пора и серьезно поесть:",
        reply_markup=get_final_touch_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.final_touch)

@router.message(StateFilter(DateConstructorStates.final_touch))
async def process_final_touch(message: Message, state: FSMContext):
    if message.text == "Свой вариант →":
        await message.answer(
            "Напиши, куда бы ты хотел(а) пойти вечером:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(DateConstructorStates.custom_final_touch)
        return

    await state.update_data(final_touch=message.text)
    await message.answer(
        "<b>Шаг 4. Выбор даты.</b>\n\n"
        "📅 Выбери дату:",
        reply_markup=get_date_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.date)

@router.message(StateFilter(DateConstructorStates.date))
async def process_date(message: Message, state: FSMContext):
    try:
        # Проверяем формат даты
        datetime.strptime(message.text, "%d.%m.%Y")
        
        # Сохраняем дату
        await state.update_data(date=message.text)
        
        # Переходим к этапу комментария
        await message.answer(
            "💭 Хочешь добавить что-то от себя? Напиши комментарий или предложение:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(DateConstructorStates.comment)
        
    except ValueError:
        await message.answer("Пожалуйста, выбери дату из предложенных вариантов.")
    except Exception as e:
        logger.error(f"Error in process_date: {e}")
        await message.answer("Произошла ошибка при обработке даты. Пожалуйста, попробуйте еще раз.")
        await state.clear()

@router.message(StateFilter(DateConstructorStates.comment))
async def process_comment(message: Message, state: FSMContext, bot):
    try:
        # Получаем все данные
        data = await state.get_data()
        comment = message.text.strip()
        if not comment or len(comment) < 2:
            await message.answer("Комментарий слишком короткий. Пожалуйста, напиши что-то подробнее.")
            return
        date = data.get('date', '')
        atmo_text = ATMOSPHERE_TEXTS.get(data.get('atmosphere'), data.get('atmosphere'))
        act_text = ACTIVITY_TEXTS.get(data.get('activity'), data.get('activity'))
        final_touch = FINAL_TOUCH_TEXTS.get(data.get('final_touch'), data.get('final_touch'))
        
        # Преобразуем дату в формат '21 июня'
        try:
            date_obj = datetime.strptime(date, "%d.%m.%Y")
            day = date_obj.day
            month = MONTHS[date_obj.strftime("%m")]
            date_text = f"{day} {month}"
        except Exception:
            date_text = date

        # Добавляем дополнительные сообщения в зависимости от выбора
        additional_atmo_text = ""
        if data.get('atmosphere') == "Вейкборд и петнат на причале":
            additional_atmo_text = " Натуральное игристое открывается сразу после катера."
        elif data.get('atmosphere') == "Сапы или байдарки по реке":
            additional_atmo_text = " Петнат будет и здесь, но из рюкзака и прямо на воде."
        elif data.get('atmosphere') == "Открытый бассейн и московский загар":
            additional_atmo_text = " Здесь игристое запрещено, поэтому оно нас ждет чуть позже."

        additional_final_text = ""
        if data.get('final_touch') == "За Крышей":
            additional_final_text = " Отличный выбор, современная классика и креветки с малиной."
        elif data.get('final_touch') == "Bruno":
            additional_final_text = " Вижу, что хочется мяса."
        elif data.get('final_touch') == "Big Wine Freaks":
            additional_final_text = " Идем исследовать нэтти."
        elif data.get('final_touch') == "таби":
            additional_final_text = " Давно не были, пора выпить саке!"

        # Формируем финальный текст
        final_message = (
            "Ура! ✨\n\n"
            f"Мы просыпаемся <b>{date_text}</b> и отправляемся <b>{atmo_text}</b>.{additional_atmo_text}\n"
            f"Немного устаем, но сможем вдохнуть в себя силы искусством — нас ждет <b>{act_text}</b>.\n"
            f"Финальной точкой дня становится <b>{final_touch}</b>.{additional_final_text} А дальше смотрим куда нас заведет этот вечер. До встречи!\n\n"
            "💕 👀\n\n"
            "<i>PS. На протяжении всего дня мы подпитываемся не только искусством, но и совершаем приятные привалы с пивом или вином. Без этого никак!</i>"
        )
        
        # Отправляем финальный текст пользователю
        await message.answer(final_message, parse_mode="HTML")
        
        # Отправляем все данные админу
        admin_text = (
            f"📅 Новое свидание!\n"
            f"От пользователя: {message.from_user.full_name} (@{message.from_user.username})\n\n"
            f"<b>Дата:</b> {date_text}\n"
            f"<b>Утро:</b> {atmo_text}\n"
            f"<b>День:</b> {act_text}\n"
            f"<b>Вечер:</b> {final_touch}\n"
            f"<b>Комментарий пользователя:</b> {comment}"
        )
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
        
        # Отправляем финальное сообщение с новой кнопкой
        await message.answer(
            "💫 Отличный выбор! Будет классно!",
            reply_markup=get_final_keyboard()
        )
        
        # Сбрасываем состояние
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in process_comment: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        await state.clear()

@router.message(StateFilter(DateConstructorStates.custom_atmosphere))
async def process_custom_atmosphere_text(message: Message, state: FSMContext):
    await state.update_data(atmosphere=message.text)
    await message.answer(
        "<b>Шаг 2. День.</b>\n\n"
        "Нужно пропитаться искусством и периодически делать привалы на бокальчик:",
        reply_markup=get_activity_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.activity)

@router.message(StateFilter(DateConstructorStates.custom_activity))
async def process_custom_activity_text(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.answer(
        "<b>Шаг 3. Вечер.</b>\n\n"
        "Нагулялись, пора и серьезно поесть:",
        reply_markup=get_final_touch_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.final_touch)

@router.message(StateFilter(DateConstructorStates.custom_final_touch))
async def process_custom_final_touch_text(message: Message, state: FSMContext):
    await state.update_data(final_touch=message.text)
    await message.answer(
        "<b>Шаг 4. Выбор даты.</b>\n\n"
        "📅 Выбери дату:",
        reply_markup=get_date_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.date)

@router.message(F.text == "Запланировать еще одно свидание?")
async def start_new_planning(message: Message, state: FSMContext):
    await message.answer(
        "<b>Часть 1. Утро.</b>\n\n"
        "Можно проснуться либо рано, либо поздно, но хочется какой-то активности (завтрак в модном месте включен):",
        reply_markup=get_atmosphere_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(DateConstructorStates.atmosphere)

@router.message(Command("date"))
async def cmd_date_offer(message: Message, bot):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Нет доступа.")
        return
    try:
        now = int(time.time())
        # Читаем всех пользователей
        users = {}
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    users[parts[0]] = int(parts[1])
                elif parts[0]:
                    users[parts[0]] = 0
        # Рассылаем и обновляем timestamp
        for user_id in users:
            try:
                await bot.send_message(user_id, DATE_OFFER_TEXT, reply_markup=get_date_offer_keyboard())
                users[user_id] = now
                logger.info(f"Manual /date: sent to {user_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить предложение {user_id}: {e}")
        # Сохраняем обновлённые timestamps
        with open("users.txt", "w") as f:
            for user_id, ts in users.items():
                f.write(f"{user_id}:{ts}\n")
        await message.answer("Рассылка завершена.")
    except Exception as e:
        await message.answer(f"Ошибка рассылки: {e}")

@router.message(lambda m: m.text in DATE_OFFER_BUTTONS)
async def process_date_offer_reply(message: Message, state: FSMContext):
    reply = DATE_OFFER_REPLY.get(message.text)
    if reply:
        await message.answer(reply, reply_markup=ReplyKeyboardRemove())
