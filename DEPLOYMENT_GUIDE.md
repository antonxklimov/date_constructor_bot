# Гайд по деплою бота в AppWrite

## 1. Подготовка кода
- Убедитесь, что все зависимости указаны в `requirements.txt`
- Проверьте версии библиотек, особенно `aiogram` (3.x)
- Убедитесь, что все импорты соответствуют актуальным версиям библиотек
- Проверьте наличие всех необходимых файлов в репозитории

## 2. Настройка AppWrite
### Функция
- Создайте новую функцию в AppWrite
- Установите Python 3.9 или выше
- Добавьте все необходимые переменные окружения:
  - `BOT_TOKEN` - токен вашего бота
  - `ADMIN_ID` - ID администратора
  - `OPENAI_API_KEY` - ключ API OpenAI (если используется)

### Зависимости
- Убедитесь, что все зависимости установлены в правильном порядке
- Проверьте совместимость версий библиотек
- Особое внимание уделите:
  - `aiogram` - используйте актуальные импорты для версии 3.x
  - `python-dotenv` - для работы с переменными окружения
  - `openai` - если используется

## 3. Частые проблемы и их решения
### Импорты
- `aiogram.storage` → `aiogram.fsm.storage.memory`
- `aiogram.filters.state` → `aiogram.filters`
- `aiogram.utils.logging` → используйте стандартный `logging`

### Состояния
- Убедитесь, что все состояния определены в `states.py`
- Проверьте правильность переходов между состояниями
- Используйте `StateFilter` для фильтрации состояний

### Обработка ошибок
- Добавьте обработку исключений во все асинхронные функции
- Логируйте ошибки для отладки
- Используйте try-except блоки для критических операций

## 4. Проверка после деплоя
1. Проверьте работу команды `/start`
2. Протестируйте все этапы создания свидания:
   - Выбор атмосферы
   - Выбор активности
   - Выбор финального штриха
   - Выбор даты
   - Комментарий пользователя
3. Проверьте форматирование сообщений
4. Убедитесь, что уведомления приходят администратору

## 5. Отладка
- Используйте логирование для отслеживания проблем
- Проверяйте логи в AppWrite
- Тестируйте каждое изменение перед деплоем
- Сохраняйте рабочие версии с помощью тегов Git

## 6. Рекомендации
- Создавайте теги для рабочих версий: `git tag v1.0.0`
- Документируйте все изменения
- Регулярно обновляйте зависимости
- Следите за обновлениями библиотек
- Используйте систему контроля версий для отслеживания изменений

## 7. Полезные команды
```bash
# Создание тега для рабочей версии
git tag v1.0.0
git push origin v1.0.0

# Откат к предыдущей версии
git reset --hard <commit-hash>
git push -f origin main

# Проверка статуса
git status
git log --oneline

# Получить свежие изменения с сервера
git pull
```

# Гайд по деплою бота на сервер (polling + systemd)

## 1. Клонирование репозитория

```bash
cd ~/bots/dateday
git clone https://github.com/antonxklimov/date_constructor_bot.git
cd date_constructor_bot
```

## 2. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 4. Настройка конфига

В файле `config.py` должны быть:
```python
BOT_TOKEN = "<токен_бота>"
ADMIN_ID = <ваш_telegram_id>
```

## 5. Проверка локального запуска

```bash
python3 main.py
```
Бот должен отвечать на /start в Telegram.

## 6. Удаление webhook (если ранее был установлен)

```bash
curl "https://api.telegram.org/bot<токен_бота>/deleteWebhook"
```

## 7. Создание systemd unit-файла

```bash
sudo nano /etc/systemd/system/date_constructor_bot.service
```

Вставить:
```ini
[Unit]
Description=Date Constructor Bot
After=network.target

[Service]
User=anton
WorkingDirectory=/home/anton/bots/dateday/date_constructor_bot
ExecStart=/home/anton/bots/dateday/date_constructor_bot/venv/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

- Проверь пути и имя пользователя!

## 8. Активация и запуск сервиса

```bash
sudo systemctl daemon-reload
sudo systemctl start date_constructor_bot
sudo systemctl enable date_constructor_bot
```

## 9. Проверка статуса и логов

```bash
sudo systemctl status date_constructor_bot
journalctl -u date_constructor_bot -f
```

## 10. Обновление кода

```bash
cd ~/bots/dateday/date_constructor_bot
git pull
sudo systemctl restart date_constructor_bot
```

---

**Если возникнут ошибки — смотри логи через journalctl и проверяй config.py.** 