import pandas as pd
from pathlib import Path

class TarotCard:
    def __init__(self, id, name, arcanas, description, image_path=None):
        self.id = id
        self.name = name
        self.arcanas = arcanas
        self.description = description
        self.image_path = image_path

    def __repr__(self):
        return f"TarotCard(id={self.id}, name='{self.name}', arcanas='{self.arcanas}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'arcanas': self.arcanas,
            'description': self.description,
            'image_path': str(self.image_path) if self.image_path else None
        }

def load_tarot_cards(file_path="taro_tableCSV.csv", images_dir="Cards-png"):
    """
    Загружает данные из CSV и связывает с изображениями
    :param file_path: путь к CSV файлу
    :param images_dir: папка с изображениями
    :return: словарь {id: TarotCard}
    """
    try:
        # Чтение CSV
        df = pd.read_csv(file_path, sep=';')
        
        # Проверка существования папки с изображениями
        images_path = Path(images_dir)
        if not images_path.exists():
            print(f"Предупреждение: папка {images_dir} не найдена")
        
        tarot_cards = {}
        
        for index, row in df.iterrows():
            try:
                card_id = row["id"]
                
                # Формируем путь к изображению
                img_file = f"{card_id}.png"
                img_path = images_path / img_file
                
                # Проверяем существование файла изображения
                image_exists = img_path.is_file()
                
                card = TarotCard(
                    id=card_id,
                    name=row["Name"],
                    arcanas=row["Arcanas"],
                    description=row["description"],
                    image_path=img_path if image_exists else None
                )
                tarot_cards[card.id] = card
            except KeyError as e:
                print(f"Ошибка в строке {index+2}: отсутствует столбец {e}")
                continue
            except Exception as e:
                print(f"Ошибка обработки строки {index+2}: {e}")
                continue
                
        return tarot_cards
    
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        print("Убедитесь, что файл находится в той же папке, что и скрипт")
        return {}
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return {}

if __name__ == "__main__":
    # Загрузка данных
    cards = load_tarot_cards()
    
    if cards:
        print(f"\nУспешно загружено {len(cards)} карт:\n")
        
        # Вывод информации о первых 3 картах
        for card_id in sorted(cards.keys())[:3]:
            card = cards[card_id]
            print(f"ID: {card.id}")
            print(f"Название: {card.name}")
            print(f"Арканы: {card.arcanas}")
            print(f"Описание: {card.description[:70]}...")
            print(f"Путь к изображению: {card.image_path}")
            print(f"Изображение доступно: {'Да' if card.image_path else 'Нет'}\n")
        
        # Экспорт в JSON
        import json
        with open("tarot_cards.json", "w", encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in cards.items()}, f, ensure_ascii=False, indent=4)
        print("Данные сохранены в tarot_cards.json")
    else:
        print("Не удалось загрузить данные. Проверьте файл taro_tableCSV.csv")
