"""
Телеграм бот для расклада Таро с анимациями и изображениями
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler, 
                          ContextTypes, MessageHandler, filters)
from telegram.constants import ParseMode

from config import BOT_TOKEN
from animated_tarot_logic import AnimatedTarotReading, SPREAD_TYPES

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальный экземпляр для работы с картами
tarot_reader = AnimatedTarotReading()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    stats = tarot_reader.get_spread_statistics()
    
    major_count = stats['major_arcana']
    minor_count = stats['minor_arcana']
    total_count = stats['total_cards']
    
    welcome_message = f"""
🔮 *Добро пожаловать в обновленный Таро-бот!* 🔮

Я помогу вам сделать красивый анимированный расклад карт Таро с 
изображениями и получить мудрые советы.

📊 *Доступно:*
• {total_count} карт Таро ({major_count} Старших + {minor_count} Младших Арканов)
• {stats['spread_types']} типа раскладов
• Анимированные эффекты
• Изображения карт

*Доступные команды:*
/start - Показать это сообщение
/spreads - Выбрать тип расклада
/help - Помощь

Нажмите /spreads чтобы начать магическое путешествие! ✨
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /help"""
    help_message = """
🔮 *Помощь по использованию Таро-бота*

*Новые возможности:*
• 🎬 **Анимированные расклады** - каждая карта открывается с эффектом
• 🖼️ **Изображения карт** - вы увидите настоящие карты Таро
• 📚 **Полная колода** - все 78 карт (22 Старших + 56 Младших Арканов)
• 🎭 **Улучшенные описания** - детальные толкования из базы данных

*Доступные типы раскладов:*
• **🃏 Карта дня** - Одна карта для общего совета
• **🔮 Прошлое-Настоящее-Будущее** - Три карты для анализа временных аспектов
• **✨ Кельтский крест** - Полный расклад из 10 карт для глубокого анализа

*Как использовать:*
1. Нажмите /spreads
2. Выберите тип расклада
3. Наблюдайте за анимацией тасования карт
4. Получите красивое раскрытие каждой карты с изображением
5. Изучите толкования и советы

*Особенности:*
• Карты могут выпадать в перевернутом виде (30% вероятность)
• Каждый расклад уникален и не повторяется
• Пауза между картами для лучшего восприятия
• Используйте Таро как инструмент для размышлений

_Пусть анимированные карты укажут вам верный путь!_ 🌟
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def spreads_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать меню выбора типа расклада"""
    keyboard = [
        [InlineKeyboardButton("🃏 Карта дня (1 карта)", 
                              callback_data="spread_one_card")],
        [InlineKeyboardButton("🔮 Прошлое-Настоящее-Будущее (3 карты)", 
                              callback_data="spread_three_cards")],
        [InlineKeyboardButton("✨ Кельтский крест (10 карт)", 
                              callback_data="spread_celtic_cross")],
        [InlineKeyboardButton("📊 Статистика карт", 
                              callback_data="show_stats")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🔮 *Выберите тип анимированного расклада:*

🃏 **Карта дня** - Быстрый совет с одной картой
🔮 **Прошлое-Настоящее-Будущее** - Анализ временных аспектов ситуации  
✨ **Кельтский крест** - Глубокий анализ сложной ситуации
📊 **Статистика карт** - Информация о доступных картах

_Каждый расклад будет показан с красивыми анимациями и изображениями карт!_
"""
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_spread_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка выбора типа расклада"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем тип расклада из callback_data
    spread_type = query.data.replace("spread_", "")
    
    if spread_type not in SPREAD_TYPES:
        await query.edit_message_text("❌ Неизвестный тип расклада")
        return
    
    try:
        # Создаем расклад
        spread = tarot_reader.create_spread(spread_type)
        
        # Отправляем анимированный расклад
        await tarot_reader.send_animated_spread(update, context, spread)
            
    except Exception as e:
        logger.error(f"Ошибка при создании расклада: {e}")
        await query.edit_message_text(
            "❌ Произошла ошибка при создании расклада. Попробуйте снова.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                "🔄 Попробовать снова", callback_data="new_spread")]])
        )


async def handle_show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать статистику доступных карт"""
    query = update.callback_query
    await query.answer()
    
    stats = tarot_reader.get_spread_statistics()
    
    stats_message = f"""
📊 *Статистика карт Таро*

🎴 **Всего карт:** {stats['total_cards']}
🔮 **Старшие Арканы:** {stats['major_arcana']} карт
🃏 **Младшие Арканы:** {stats['minor_arcana']} карт
✨ **Типы раскладов:** {stats['spread_types']}

💫 **Особенности:**
• Все карты имеют изображения
• Поддержка перевернутых карт
• Анимированные эффекты раскрытия
• Детальные описания из базы данных

_Готовы к магическому путешествию?_
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Вернуться к раскладам", 
                              callback_data="back_to_spreads")],
        [InlineKeyboardButton("🎯 Случайный расклад", 
                              callback_data="random_spread")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        stats_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_random_spread(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Создать случайный расклад"""
    query = update.callback_query
    await query.answer()
    
    import random
    spread_types = list(SPREAD_TYPES.keys())
    random_spread_type = random.choice(spread_types)
    
    try:
        spread = tarot_reader.create_spread(random_spread_type)
        await tarot_reader.send_animated_spread(update, context, spread)
    except Exception as e:
        logger.error(f"Ошибка при создании случайного расклада: {e}")
        await query.edit_message_text(
            "❌ Произошла ошибка при создании расклада. Попробуйте снова.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                "🔄 Попробовать снова", callback_data="random_spread")]])
        )


async def handle_back_to_spreads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Вернуться к выбору раскладов"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🃏 Карта дня (1 карта)", 
                              callback_data="spread_one_card")],
        [InlineKeyboardButton("🔮 Прошлое-Настоящее-Будущее (3 карты)", 
                              callback_data="spread_three_cards")],
        [InlineKeyboardButton("✨ Кельтский крест (10 карт)", 
                              callback_data="spread_celtic_cross")],
        [InlineKeyboardButton("📊 Статистика карт", 
                              callback_data="show_stats")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🔮 *Выберите тип анимированного расклада:*

🃏 **Карта дня** - Быстрый совет с одной картой
🔮 **Прошлое-Настоящее-Будущее** - Анализ временных аспектов ситуации  
✨ **Кельтский крест** - Глубокий анализ сложной ситуации
📊 **Статистика карт** - Информация о доступных картах

_Каждый расклад будет показан с красивыми анимациями и изображениями карт!_
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_new_spread(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка запроса на новый расклад"""
    await handle_back_to_spreads(update, context)


async def handle_ai_interpretation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка запроса на AI-интерпретацию (заглушка)"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🤖 AI-интерпретация будет доступна в следующих версиях!\n\n" +
        "Сейчас эта функция находится в разработке. " +
        "Пока что используйте расширенные толкования карт из базы данных.\n\n" +
        "Хотите сделать новый расклад?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            "🔄 Новый расклад", callback_data="new_spread")]])
    )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений"""
    text = update.message.text.lower()
    
    keywords = ['таро', 'карт', 'расклад', 'гадание', 'анимация']
    if any(word in text for word in keywords):
        await update.message.reply_text(
            "🔮 Для создания анимированного расклада используйте команду /spreads",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                "🔮 Сделать расклад", callback_data="back_to_spreads")]])
        )
    else:
        msg = "Я специализируюсь на анимированных раскладах Таро с изображениями карт! 🔮✨\n\n"
        msg += "Используйте /spreads для выбора типа расклада или /help для получения помощи."
        await update.message.reply_text(msg)


def main() -> None:
    """Основная функция для запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("spreads", spreads_menu))
    
    # Добавляем обработчики callback-запросов
    application.add_handler(CallbackQueryHandler(handle_spread_selection, pattern="^spread_"))
    application.add_handler(CallbackQueryHandler(handle_show_stats, pattern="^show_stats$"))
    application.add_handler(CallbackQueryHandler(handle_random_spread, pattern="^random_spread$"))
    application.add_handler(CallbackQueryHandler(handle_back_to_spreads, pattern="^back_to_spreads$"))
    application.add_handler(CallbackQueryHandler(handle_new_spread, pattern="^new_spread$"))
    application.add_handler(CallbackQueryHandler(handle_ai_interpretation, pattern="^ai_interpret"))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Запускаем бота
    logger.info("🔮 Анимированный Таро-бот запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main() 