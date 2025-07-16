"""
Обновленная база данных карт Таро с загрузкой из JSON файла
"""

import json
from typing import Dict, List, Any


class TarotCardsLoader:
    """Класс для загрузки и работы с картами Таро из JSON файла"""
    
    def __init__(self, json_file: str = "taro_cards.json"):
        self.json_file = json_file
        self.cards_data = self._load_cards()
    
    def _load_cards(self) -> List[Dict[str, Any]]:
        """Загружает карты из JSON файла"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.json_file} не найден!")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {self.json_file}")
            return []
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Возвращает все карты"""
        return self.cards_data
    
    def get_card_by_index(self, index: int) -> Dict[str, Any]:
        """Возвращает карту по индексу"""
        if 0 <= index < len(self.cards_data):
            return self.cards_data[index]
        return None
    
    def get_card_by_name(self, name: str) -> Dict[str, Any]:
        """Возвращает карту по имени (английскому названию)"""
        for card in self.cards_data:
            if card.get('name') == name:
                return card
        return None
    
    def get_card_by_arcana_name(self, arcana_name: str) -> Dict[str, Any]:
        """Возвращает карту по названию аркана"""
        for card in self.cards_data:
            if arcana_name in card.get('arcana_name', ''):
                return card
        return None
    
    def get_card_image_path(self, card_index: int) -> str:
        """Возвращает путь к изображению карты"""
        if 0 <= card_index < len(self.cards_data):
            card = self.cards_data[card_index]
            name = card.get('name', '')
            if name:
                return f"Cards-png/{card_index}.{name}.png"
        return None
    
    def get_card_meaning(self, card_index: int, 
                        is_reversed: bool = False) -> str:
        """Возвращает значение карты (прямое или перевернутое)"""
        card = self.get_card_by_index(card_index)
        if not card:
            return "Карта не найдена"
        
        # Формируем заголовок
        arcana_name = card.get('arcana_name', 'Неизвестная карта')
        name = card.get('name', '').replace('_', ' ')
        
        if is_reversed:
            title = f"🔄 **{arcana_name}** ({name} - перевернутая)\n\n"
        else:
            title = f"🔮 **{arcana_name}** ({name})\n\n"
        
        # Получаем значение из general_meaning
        general_meaning = card.get('general_meaning', {})
        
        if is_reversed:
            meaning = general_meaning.get('reversed', 
                                        'Толкование перевернутой карты недоступно')
        else:
            meaning = general_meaning.get('upright', 
                                        'Толкование прямой карты недоступно')
        
        return title + meaning
    
    def format_card_description(self, card: Dict, is_reversed: bool = False) -> str:
        """Форматирует описание карты для отправки в боте"""
        if not card:
            return "Карта не найдена"
        
        # Формируем заголовок
        arcana_name = card.get('arcana_name', 'Неизвестная карта')
        name = card.get('name', '').replace('_', ' ')
        
        if is_reversed:
            title = f"🔄 **{arcana_name}** ({name} - перевернутая)\n\n"
        else:
            title = f"🔮 **{arcana_name}** ({name})\n\n"
        
        # Получаем значение из general_meaning
        general_meaning = card.get('general_meaning', {})
        
        if is_reversed:
            meaning = general_meaning.get('reversed', 
                                        'Толкование перевернутой карты недоступно')
        else:
            meaning = general_meaning.get('upright', 
                                        'Толкование прямой карты недоступно')
        
        # Обрезаем описание если оно слишком длинное
        if len(meaning) > 500:
            meaning = meaning[:500] + "..."
        
        return title + meaning
    
    def get_card_love_meaning(self, card_index: int, 
                             is_reversed: bool = False) -> str:
        """Возвращает значение карты в любви"""
        card = self.get_card_by_index(card_index)
        if not card:
            return "Карта не найдена"
        
        love_meaning = card.get('love_meaning', {})
        
        if is_reversed:
            meaning = love_meaning.get('reversed', 
                                     'Толкование в любви недоступно')
        else:
            meaning = love_meaning.get('upright', 
                                     'Толкование в любви недоступно')
        
        return meaning
    
    def get_card_situation_meaning(self, card_index: int, 
                                  is_reversed: bool = False) -> str:
        """Возвращает значение карты в ситуации"""
        card = self.get_card_by_index(card_index)
        if not card:
            return "Карта не найдена"
        
        situation_meaning = card.get('situation_meaning', {})
        
        if is_reversed:
            meaning = situation_meaning.get('reversed', 
                                          'Толкование в ситуации недоступно')
        else:
            meaning = situation_meaning.get('upright', 
                                          'Толкование в ситуации недоступно')
        
        return meaning
    
    def get_card_day_meaning(self, card_index: int) -> str:
        """Возвращает значение карты дня"""
        card = self.get_card_by_index(card_index)
        if not card:
            return "Карта не найдена"
        
        return card.get('day_meaning', 'Значение карты дня недоступно')
    
    def get_card_advice(self, card_index: int) -> str:
        """Возвращает совет карты"""
        card = self.get_card_by_index(card_index)
        if not card:
            return "Карта не найдена"
        
        return card.get('advice', 'Совет карты недоступен')
    
    def get_card_positions(self, card_index: int) -> Dict[str, str]:
        """Возвращает краткие описания прямого и перевернутого положения"""
        card = self.get_card_by_index(card_index)
        if not card:
            return {"upright": "Не найдено", "reversed": "Не найдено"}
        
        return {
            "upright": card.get('upright_position', 'Описание недоступно'),
            "reversed": card.get('reversed_position', 'Описание недоступно')
        }
    
    def get_statistics(self) -> Dict[str, int]:
        """Возвращает статистику по картам"""
        major_arcana = 0
        minor_arcana = 0
        
        for card in self.cards_data:
            category = card.get('category', '')
            if 'Старшие арканы' in category:
                major_arcana += 1
            else:
                minor_arcana += 1
        
        return {
            "total_cards": len(self.cards_data),
            "major_arcana": major_arcana,
            "minor_arcana": minor_arcana
        }


# Глобальный экземпляр для использования в других модулях
tarot_loader = TarotCardsLoader()


# Типы раскладов остаются прежними
SPREAD_TYPES = {
    "daily": {
        "name": "Карта дня",
        "description": "Одна карта для общего совета на день",
        "positions": ["Совет на день"]
    },
    "three_cards": {
        "name": "Прошлое-Настоящее-Будущее",
        "description": "Три карты для анализа временных аспектов ситуации",
        "positions": ["Прошлое", "Настоящее", "Будущее"]
    },
    "celtic_cross": {
        "name": "Кельтский крест",
        "description": "Полный расклад из 10 карт для глубокого анализа",
        "positions": [
            "Текущая ситуация",
            "Препятствие или вызов",
            "Отдаленное прошлое",
            "Недавнее прошлое",
            "Возможный исход",
            "Ближайшее будущее",
            "Ваш подход",
            "Внешние влияния",
            "Надежды и страхи",
            "Окончательный результат"
        ]
    },
    "love": {
        "name": "Расклад на любовь",
        "description": "Пять карт для анализа отношений",
        "positions": [
            "Ваши чувства",
            "Чувства партнера",
            "Что вас связывает",
            "Препятствия",
            "Перспективы отношений"
        ]
    }
}


def get_all_tarot_cards() -> List[Dict[str, Any]]:
    """Возвращает все карты Таро"""
    return tarot_loader.get_all_cards()


def get_tarot_card_by_index(index: int) -> Dict[str, Any]:
    """Возвращает карту по индексу"""
    return tarot_loader.get_card_by_index(index)


def get_tarot_statistics() -> Dict[str, int]:
    """Возвращает статистику по картам"""
    return tarot_loader.get_statistics() 