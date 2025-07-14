"""
Простой тест для проверки работы основных функций бота
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tarot_logic import TarotReading
from tarot_cards import TAROT_CARDS, SPREAD_TYPES


def test_tarot_reading():
    """Тест основных функций TarotReading"""
    print("🧪 Тестирование TarotReading...")
    
    reader = TarotReading()
    
    # Тест 1: Проверка количества карт
    print(f"✅ Загружено {len(reader.cards)} карт")
    assert len(reader.cards) == 22, f"Ожидалось 22 карты, получено {len(reader.cards)}"
    
    # Тест 2: Выбор одной карты
    cards = reader.draw_cards(1)
    print(f"✅ Выбрана карта: {cards[0][0]} ({'перевернутая' if cards[0][1] else 'прямая'})")
    assert len(cards) == 1, "Должна быть выбрана одна карта"
    
    # Тест 3: Выбор трех карт без повторений
    cards = reader.draw_cards(3)
    card_names = [card[0] for card in cards]
    print(f"✅ Выбраны карты: {', '.join(card_names)}")
    assert len(set(card_names)) == 3, "Карты не должны повторяться"
    
    # Тест 4: Толкование карты
    interpretation = reader.get_card_interpretation("Шут", False)
    print(f"✅ Толкование получено: {interpretation[:50]}...")
    assert "Шут" in interpretation, "Толкование должно содержать название карты"
    
    print("✅ Все тесты TarotReading пройдены!")


def test_spreads():
    """Тест создания раскладов"""
    print("\n🧪 Тестирование раскладов...")
    
    reader = TarotReading()
    
    # Тест раскладов
    for spread_type in SPREAD_TYPES:
        spread = reader.create_spread(spread_type)
        expected_cards = len(SPREAD_TYPES[spread_type]["positions"])
        
        print(f"✅ {spread['name']}: {len(spread['cards'])} карт")
        assert len(spread['cards']) == expected_cards, f"Ожидалось {expected_cards} карт"
        
        # Проверка уникальности карт в раскладе
        card_names = [card['card_name'] for card in spread['cards']]
        assert len(set(card_names)) == len(card_names), "Карты в раскладе должны быть уникальными"
    
    print("✅ Все тесты раскладов пройдены!")


def test_message_formatting():
    """Тест форматирования сообщений"""
    print("\n🧪 Тестирование форматирования сообщений...")
    
    reader = TarotReading()
    
    # Тест форматирования расклада
    spread = reader.create_spread("one_card")
    message = reader.format_spread_message(spread)
    
    print(f"✅ Сообщение сформировано: {len(message)} символов")
    assert len(message) > 0, "Сообщение не должно быть пустым"
    assert spread['name'] in message, "Сообщение должно содержать название расклада"
    
    print("✅ Все тесты форматирования пройдены!")


def test_cards_database():
    """Тест базы данных карт"""
    print("\n🧪 Тестирование базы данных карт...")
    
    # Проверка структуры карт
    for card_name, card_data in TAROT_CARDS.items():
        assert "number" in card_data, f"Карта {card_name} должна иметь номер"
        assert "meaning" in card_data, f"Карта {card_name} должна иметь значение"
        assert "reversed" in card_data, f"Карта {card_name} должна иметь перевернутое значение"
    
    print(f"✅ Проверено {len(TAROT_CARDS)} карт")
    
    # Проверка раскладов
    for spread_type, spread_data in SPREAD_TYPES.items():
        assert "name" in spread_data, f"Расклад {spread_type} должен иметь название"
        assert "description" in spread_data, f"Расклад {spread_type} должен иметь описание"
        assert "positions" in spread_data, f"Расклад {spread_type} должен иметь позиции"
        assert len(spread_data["positions"]) > 0, f"Расклад {spread_type} должен иметь хотя бы одну позицию"
    
    print(f"✅ Проверено {len(SPREAD_TYPES)} раскладов")
    print("✅ Все тесты базы данных пройдены!")


def main():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов Таро-бота\n")
    
    try:
        test_cards_database()
        test_tarot_reading()
        test_spreads()
        test_message_formatting()
        
        print("\n🎉 Все тесты успешно пройдены! Бот готов к использованию.")
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 