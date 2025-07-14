"""
Телеграм бот для расклада Таро
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import BOT_TOKEN
from tarot_logic import TarotReading
from tarot_cards import SPREAD_TYPES

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальный экземпляр для работы с картами
tarot_reader = TarotReading()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    welcome_message = """
🔮 *Добро пожаловать в Таро-бот!* 🔮

Я помогу вам сделать расклад карт Таро и получить мудрые советы.

*Доступные команды:*
/start - Показать это сообщение
/spreads - Выбрать тип расклада
/help - Помощь

Нажмите /spreads чтобы начать!
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /help"""
    help_message = """
🔮 *Помощь по использованию Таро-бота*

*Доступные типы раскладов:*
• **Карта дня** - Одна карта для общего совета
• **Прошлое-Настоящее-Будущее** - Три карты для анализа временных аспектов
• **Кельтский крест** - Полный расклад из 10 карт для глубокого анализа

*Как использовать:*
1. Нажмите /spreads
2. Выберите тип расклада
3. Получите толкование карт

*Примечания:*
• Карты могут выпадать в перевернутом виде
• Каждый расклад уникален и не повторяется
• Используйте Таро как инструмент для размышлений, а не как предсказание будущего

_Пусть карты укажут вам верный путь!_ ✨
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def spreads_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать меню выбора типа расклада"""
    keyboard = [
        [InlineKeyboardButton("🃏 Карта дня (1 карта)", callback_data="spread_one_card")],
        [InlineKeyboardButton("🔮 Прошлое-Настоящее-Будущее (3 карты)", callback_data="spread_three_cards")],
        [InlineKeyboardButton("✨ Кельтский крест (10 карт)", callback_data="spread_celtic_cross")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🔮 *Выберите тип расклада:*

🃏 **Карта дня** - Быстрый совет или энергия дня
🔮 **Прошлое-Настоящее-Будущее** - Анализ временных аспектов ситуации  
✨ **Кельтский крест** - Глубокий анализ сложной ситуации

_Выберите один из вариантов ниже:_
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
    
    # Показываем сообщение о создании расклада
    await query.edit_message_text("🔮 Создаю расклад... Перемешиваю карты...")
    
    try:
        # Создаем расклад
        spread = tarot_reader.create_spread(spread_type)
        
        # Форматируем сообщение
        message = tarot_reader.format_spread_message(spread)
        
        # Добавляем кнопки для дополнительных действий
        keyboard = [
            [InlineKeyboardButton("🔄 Новый расклад", callback_data="new_spread")],
            [InlineKeyboardButton("🤖 Получить AI-интерпретацию", callback_data=f"ai_interpret_{spread_type}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем результат (может быть длинным, поэтому разбиваем если нужно)
        if len(message) > 4096:
            # Разбиваем длинное сообщение на части
            parts = []
            current_part = ""
            
            for card in spread['cards']:
                card_text = f"**{card['position']}**\n{card['interpretation']}\n\n"
                if len(current_part + card_text) > 4000:
                    parts.append(current_part)
                    current_part = card_text
                else:
                    current_part += card_text
            
            if current_part:
                parts.append(current_part)
            
            # Отправляем заголовок
            header = f"✨ *{spread['name']}*\n\n_{spread['description']}_\n\n"
            await query.edit_message_text(header, parse_mode=ParseMode.MARKDOWN)
            
            # Отправляем части расклада
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Последняя часть с кнопками
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=part,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=part,
                        parse_mode=ParseMode.MARKDOWN
                    )
        else:
            await query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logger.error(f"Ошибка при создании расклада: {e}")
        await query.edit_message_text(
            "❌ Произошла ошибка при создании расклада. Попробуйте снова.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Попробовать снова", callback_data="new_spread")]])
        )


async def handle_new_spread(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка запроса на новый расклад"""
    query = update.callback_query
    await query.answer()
    
    # Возвращаем в меню выбора расклада
    keyboard = [
        [InlineKeyboardButton("🃏 Карта дня (1 карта)", callback_data="spread_one_card")],
        [InlineKeyboardButton("🔮 Прошлое-Настоящее-Будущее (3 карты)", callback_data="spread_three_cards")],
        [InlineKeyboardButton("✨ Кельтский крест (10 карт)", callback_data="spread_celtic_cross")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🔮 *Выберите тип расклада:*

🃏 **Карта дня** - Быстрый совет или энергия дня
🔮 **Прошлое-Настоящее-Будущее** - Анализ временных аспектов ситуации  
✨ **Кельтский крест** - Глубокий анализ сложной ситуации

_Выберите один из вариантов ниже:_
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_ai_interpretation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка запроса на AI-интерпретацию (заглушка)"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🤖 AI-интерпретация будет доступна в следующих версиях!\n\n" +
        "Сейчас эта функция находится в разработке. " +
        "Пока что используйте стандартные толкования карт.\n\n" +
        "Хотите сделать новый расклад?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Новый расклад", callback_data="new_spread")]])
    )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['таро', 'карт', 'расклад', 'гадание']):
        await update.message.reply_text(
            "🔮 Для создания расклада используйте команду /spreads",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔮 Сделать расклад", callback_data="new_spread")]])
        )
    else:
        await update.message.reply_text(
            "Я специализируюсь на раскладах Таро! 🔮\n\n" +
            "Используйте /spreads для выбора типа расклада или /help для получения помощи."
        )


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
    application.add_handler(CallbackQueryHandler(handle_new_spread, pattern="^new_spread$"))
    application.add_handler(CallbackQueryHandler(handle_ai_interpretation, pattern="^ai_interpret_"))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Запускаем бота
    logger.info("Бот запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main() 