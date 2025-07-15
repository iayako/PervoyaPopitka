import pandas as pd

class TarotCard:
    def __init__(self, id, name, image, arcanas, description):
        self.id = id
        self.name = name
        self.image = image
        self.arcanas = arcanas
        self.description = description

    def __repr__(self):
        return f"TarotCard(id={self.id}, name='{self.name}', arcanas='{self.arcanas}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'arcanas': self.arcanas,
            'description': self.description
        }

def load_tarot_cards(file_path="taro_tableCSV.csv", file_type='csv'):
    """
    Загружает данные из CSV-файла с разделителем ;
    :param file_path: путь к файлу (по умолчанию taro_tableCSV.csv)
    :param file_type: тип файла (только csv)
    :return: словарь {id: TarotCard}
    """
    try:
        df = pd.read_csv(file_path, sep=';')
        
        tarot_cards = {}
        
        for _, row in df.iterrows():
            try:
                card = TarotCard(
                    id=row["id"],
                    name=row["Name"],
                    image=row["Image"],
                    arcanas=row["Arcanas"],
                    description=row["description"]
                )
                tarot_cards[card.id] = card
            except KeyError as e:
                print(f"Ошибка в строке {_+2}: отсутствует столбец {e}")
                continue
                
        return tarot_cards
    
    except FileNotFoundError:
        print(f"Файл {file_path} не найден в текущей директории")
        print("Поместите файл taro_tableCSV.csv в ту же папку, где находится скрипт")
        return {}
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return {}

if __name__ == "__main__":
    # Автоматическая загрузка taro_tableCSV.csv
    cards = load_tarot_cards()
    
    if cards:
        print(f"\nУспешно загружено {len(cards)} карт:\n")
        
        # Вывод первых 3 карт для проверки
        for card_id in sorted(cards.keys())[:3]:
            card = cards[card_id]
            print(f"{card.id}. {card.name} ({card.arcanas})")
            print(f"Описание: {card.description[:60]}...\n")
        
        # Экспорт в JSON
        import json
        with open("tarot_cards.json", "w", encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in cards.items()}, f, ensure_ascii=False, indent=4)
        print("Данные сохранены в tarot_cards.json")

    else:
        print("Не удалось загрузить данные. Проверьте файл taro_tableCSV.csv")
