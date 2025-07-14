"""
Интеграция с OpenAI API для дополнительной интерпретации раскладов Таро
"""

import openai
from typing import Dict, Optional
from config import OPENAI_API_KEY


class TarotAIInterpreter:
    def __init__(self):
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
        else:
            print("Предупреждение: OPENAI_API_KEY не установлен")
    
    def create_prompt(self, spread: Dict, user_question: str = None) -> str:
        """Создает промпт для ChatGPT на основе расклада"""
        prompt = f"""Ты - опытный таролог. Проанализируй расклад Таро и дай глубокую, интуитивную интерпретацию.

Расклад: {spread['name']}
Описание: {spread['description']}

Карты в раскладе:
"""
        
        for i, card in enumerate(spread['cards'], 1):
            status = "перевернутая" if card['is_reversed'] else "прямая"
            prompt += f"{i}. {card['position']}: {card['card_name']} ({status})\n"
        
        if user_question:
            prompt += f"\nВопрос пользователя: {user_question}\n"
        
        prompt += """
Дай целостную интерпретацию расклада, учитывая:
1. Связь между картами
2. Общую энергетику расклада
3. Советы и рекомендации
4. Возможные варианты развития событий

Ответь на русском языке, используя мудрый и поддерживающий тон. Структурируй ответ с помощью эмодзи и разделов.
"""
        
        return prompt
    
    async def get_ai_interpretation(self, spread: Dict, user_question: str = None) -> str:
        """Получает AI-интерпретацию расклада"""
        if not OPENAI_API_KEY:
            return "❌ Для использования AI-интерпретации необходимо настроить OPENAI_API_KEY"
        
        try:
            prompt = self.create_prompt(spread, user_question)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # или "gpt-3.5-turbo" для более экономичного варианта
                messages=[
                    {"role": "system", "content": "Ты - мудрый таролог с многолетним опытом. Твоя задача - дать глубокую, интуитивную интерпретацию расклада Таро, помочь человеку понять свою ситуацию и найти правильный путь."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Добавляем заголовок
            formatted_response = f"🤖 **AI-интерпретация расклада**\n\n{ai_response}\n\n"
            formatted_response += "_Помните: AI-интерпретация дополняет, но не заменяет традиционные толкования карт._"
            
            return formatted_response
            
        except Exception as e:
            return f"❌ Ошибка при получении AI-интерпретации: {str(e)}"
    
    def is_available(self) -> bool:
        """Проверяет доступность OpenAI API"""
        return OPENAI_API_KEY is not None and OPENAI_API_KEY != ""


# Глобальный экземпляр для использования в боте
ai_interpreter = TarotAIInterpreter() 