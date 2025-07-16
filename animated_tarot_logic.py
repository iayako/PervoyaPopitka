"""
Анимированная логика работы с картами Таро и раскладами
"""

import random
import asyncio
from typing import Dict, List, Tuple, Optional
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from tarot_cards_updated import tarot_loader


class AnimatedTarotReading:
    def __init__(self):
        self.card_loader = tarot_loader
        self.all_cards = self.card_loader.get_all_cards()
        
    def draw_cards(self, count: int) -> List[Tuple[Dict, bool]]:
        """
        Случайно выбирает заданное количество карт без повторений
        Возвращает список кортежей (карта_данные, перевернута_ли)
        """
        if count > len(self.all_cards):
            msg = f"Невозможно выбрать {count} карт из "
            msg += f"{len(self.all_cards)} доступных"
            raise ValueError(msg)
        
        selected_cards = random.sample(self.all_cards, count)
        
        # Случайно определяем, перевернута ли карта (30% вероятность)
        cards_with_orientation = []
        for card in selected_cards:
            is_reversed = random.random() < 0.3
            cards_with_orientation.append((card, is_reversed))
        
        return cards_with_orientation
    
    def create_spread(self, spread_type: str) -> Dict:
        """
        Создает расклад выбранного типа
        """
        if spread_type not in SPREAD_TYPES:
            raise ValueError(f"Неизвестный тип расклада: {spread_type}")
        
        spread_info = SPREAD_TYPES[spread_type]
        positions = spread_info["positions"]
        cards = self.draw_cards(len(positions))
        
        spread_result = {
            "name": spread_info["name"],
            "description": spread_info["description"],
            "emoji": spread_info["emoji"],
            "cards": []
        }
        
        for i, (card, is_reversed) in enumerate(cards):
            # Находим реальный индекс карты в основном массиве
            card_index = self.all_cards.index(card)
            
            card_info = {
                "position": positions[i],
                "card_data": card,
                "is_reversed": is_reversed,
                "interpretation": self.card_loader.format_card_description(
                    card, is_reversed),
                "image_path": self.card_loader.get_card_image_path(card_index)
            }
            spread_result["cards"].append(card_info)
        
        return spread_result
    
    async def send_animated_spread(self, update: Update,
                                   context: ContextTypes.DEFAULT_TYPE,
                                   spread: Dict) -> None:
        """
        Отправляет анимированный расклад с красивыми эффектами
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        
        # Этап 1: Показываем анимацию "тасования"
        await self._show_shuffling_animation(query, spread)
        
        # Этап 2: Показываем каждую карту с анимацией
        for i, card_info in enumerate(spread["cards"]):
            await self._reveal_card_with_animation(
                context, chat_id, card_info, i + 1)
            await asyncio.sleep(2)  # Пауза между картами
        
        # Этап 3: Показываем итоговое сообщение
        await self._send_final_summary(context, chat_id, spread)
    
    async def _show_shuffling_animation(self, query, spread: Dict) -> None:
        """
        Показывает анимацию тасования карт
        """
        messages = [
            f"🔮 {spread['emoji']} Начинаю расклад *{spread['name']}*...",
            "🃏 Тасую карты...",
            "✨ Карты готовы раскрыть свои секреты...",
            f"🎯 Делаю расклад из {len(spread['cards'])} карт(ы)..."
        ]
        
        for i, message in enumerate(messages):
            await query.edit_message_text(
                message, parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(1.5)
    
    async def _reveal_card_with_animation(self,
                                          context: ContextTypes.DEFAULT_TYPE,
                                          chat_id: int, card_info: Dict,
                                          card_number: int) -> None:
        """
        Показывает карту с анимацией раскрытия
        """
        # Сначала показываем позицию
        position_message = (f"🎴 **{card_number}. "
                            f"{card_info['position']}**")
        await context.bot.send_message(
            chat_id, position_message, parse_mode=ParseMode.MARKDOWN)
        
        # Затем показываем изображение карты
        image_path = card_info.get('image_path')
        if image_path:
            try:
                with open(image_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=card_info['interpretation'],
                        parse_mode=ParseMode.MARKDOWN
                    )
            except Exception as e:
                print(f"Ошибка при отправке изображения "
                      f"{image_path}: {e}")
                # Если не удалось отправить изображение, отправляем только текст
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=card_info['interpretation'],
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            # Если изображения нет, отправляем только текст
            await context.bot.send_message(
                chat_id=chat_id,
                text=card_info['interpretation'],
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def _send_final_summary(self, context: ContextTypes.DEFAULT_TYPE,
                                  chat_id: int, spread: Dict) -> None:
        """
        Отправляет итоговое сообщение с кнопками для дальнейших действий
        """
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        summary_message = f"""
✨ **Расклад "{spread['name']}" завершен!**

_{spread['description']}_

🔮 Все карты раскрыты и готовы дать вам мудрые советы.

_Помните: карты Таро - это инструмент для размышлений и самопознания. Используйте их мудро!_
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Новый расклад",
                                  callback_data="new_spread")],
            [InlineKeyboardButton("🤖 AI-интерпретация",
                                  callback_data="ai_interpret")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=summary_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def get_card_by_name(self, name: str) -> Optional[Dict]:
        """
        Получает карту по имени для совместимости со старым кодом
        """
        return self.card_loader.get_card_by_name(name)
    
    def format_simple_spread_message(self, spread: Dict) -> str:
        """
        Форматирует расклад в простое сообщение (для совместимости)
        """
        message = f"✨ *{spread['name']}*\n\n"
        message += f"_{spread['description']}_\n\n"
        
        for i, card in enumerate(spread['cards'], 1):
            message += f"**{i}. {card['position']}**\n"
            message += f"{card['interpretation']}\n\n"
        
        return message
    
    def get_spread_statistics(self) -> Dict:
        """
        Возвращает статистику доступных карт
        """
        stats = self.card_loader.get_statistics()
        
        return {
            "total_cards": stats["total_cards"],
            "major_arcana": stats["major_arcana"],
            "minor_arcana": stats["minor_arcana"],
            "spread_types": len(SPREAD_TYPES)
        }


# Типы раскладов с позициями
SPREAD_TYPES = {
    "one_card": {
        "name": "Карта дня",
        "description": ("Одна карта, которая даст общий совет или "
                        "покажет энергию дня"),
        "positions": ["Общий совет"],
        "emoji": "🃏"
    },
    "three_cards": {
        "name": "Прошлое-Настоящее-Будущее",
        "description": ("Три карты, показывающие влияние прошлого, "
                        "настоящую ситуацию и возможное будущее"),
        "positions": ["Прошлое", "Настоящее", "Будущее"],
        "emoji": "🔮"
    },
    "celtic_cross": {
        "name": "Кельтский крест",
        "description": ("Полный расклад из 10 карт для глубокого "
                        "анализа ситуации"),
        "positions": [
            "Текущая ситуация",
            "Препятствие/вызов",
            "Далекое прошлое",
            "Недавнее прошлое",
            "Возможное будущее",
            "Ближайшее будущее",
            "Ваш подход",
            "Внешние влияния",
            "Надежды и страхи",
            "Итоговый результат"
        ],
        "emoji": "✨"
    }
} 