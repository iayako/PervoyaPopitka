"""
Логика работы с картами Таро и раскладами
"""

import random
from typing import List, Dict, Tuple
from tarot_cards import TAROT_CARDS, SPREAD_TYPES


class TarotReading:
    def __init__(self):
        self.cards = list(TAROT_CARDS.keys())
        
    def draw_cards(self, count: int) -> List[Tuple[str, bool]]:
        """
        Случайно выбирает заданное количество карт без повторений
        Возвращает список кортежей (название_карты, перевернута_ли)
        """
        if count > len(self.cards):
            raise ValueError(f"Невозможно выбрать {count} карт из {len(self.cards)} доступных")
        
        selected_cards = random.sample(self.cards, count)
        
        # Случайно определяем, перевернута ли карта (30% вероятность)
        cards_with_orientation = []
        for card in selected_cards:
            is_reversed = random.random() < 0.3
            cards_with_orientation.append((card, is_reversed))
        
        return cards_with_orientation
    
    def get_card_interpretation(self, card_name: str, is_reversed: bool) -> str:
        """
        Возвращает толкование карты
        """
        if card_name not in TAROT_CARDS:
            return "Карта не найдена"
        
        card_data = TAROT_CARDS[card_name]
        
        if is_reversed:
            interpretation = f"🔄 *{card_name}* (перевернутая)\n\n"
            interpretation += card_data.get("reversed", "Толкование перевернутой карты недоступно")
        else:
            interpretation = f"🔮 *{card_name}*\n\n"
            interpretation += card_data["meaning"]
        
        return interpretation
    
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
            "cards": []
        }
        
        for i, (card_name, is_reversed) in enumerate(cards):
            card_info = {
                "position": positions[i],
                "card_name": card_name,
                "is_reversed": is_reversed,
                "interpretation": self.get_card_interpretation(card_name, is_reversed)
            }
            spread_result["cards"].append(card_info)
        
        return spread_result
    
    def format_spread_message(self, spread: Dict) -> str:
        """
        Форматирует результат расклада в красивое сообщение
        """
        message = f"✨ *{spread['name']}*\n\n"
        message += f"_{spread['description']}_\n\n"
        
        for i, card in enumerate(spread['cards'], 1):
            message += f"**{i}. {card['position']}**\n"
            message += f"{card['interpretation']}\n\n"
        
        return message


def get_chatgpt_interpretation(spread: Dict, user_question: str = None) -> str:
    """
    Генерирует дополнительную интерпретацию с помощью ChatGPT
    (функция для будущего использования)
    """
    # Этот код будет реализован позже при подключении OpenAI API
    prompt = f"Проанализируй расклад Таро и дай развернутую интерпретацию:\n\n"
    prompt += f"Расклад: {spread['name']}\n"
    
    for card in spread['cards']:
        status = "перевернутая" if card['is_reversed'] else "прямая"
        prompt += f"- {card['position']}: {card['card_name']} ({status})\n"
    
    if user_question:
        prompt += f"\nВопрос пользователя: {user_question}\n"
    
    prompt += "\nДай целостную интерпретацию всего расклада, связав карты между собой."
    
    return prompt  # Пока возвращаем сам промпт 