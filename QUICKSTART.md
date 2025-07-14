# 🚀 Быстрый старт

## 1. Подготовка

```bash
# Клонирование проекта
git clone https://github.com/yourusername/tarot-telegram-bot.git
cd tarot-telegram-bot

# Установка зависимостей
pip install -r requirements.txt
```

## 2. Настройка бота

1. Идите к [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота: `/newbot`
3. Получите токен (например: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 3. Конфигурация

Создайте файл `.env`:
```bash
BOT_TOKEN=ваш_токен_здесь
OPENAI_API_KEY=ваш_ключ_openai_здесь  # опционально
```

## 4. Запуск

```bash
# Тестирование
python test_bot.py

# Запуск бота
python bot.py
```

## 5. Использование

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Выберите `/spreads` для создания расклада

## 🎯 Готово!

Ваш бот готов к работе! 🔮

---

📖 Подробная документация: [README.md](README.md)
🗺️ План развития: [ROADMAP.md](ROADMAP.md) 