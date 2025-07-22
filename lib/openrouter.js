const axios = require('axios');
require('dotenv').config();

class OpenRouterClient {
  constructor() {
    this.apiKey = process.env.OPENROUTER_API_KEY;
    this.baseURL = process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';
    this.defaultModel = process.env.DEFAULT_MODEL || 'qwen/qwen3-14b:free';
    
    if (!this.apiKey) {
      throw new Error('OPENROUTER_API_KEY не найден в переменных окружения');
    }

    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:3000',
        'X-Title': 'PervoyaPopitka AI'
      }
    });

    // Список бесплатных моделей
    this.freeModels = [
      {
        id: 'qwen/qwen3-14b:free',
        name: 'Qwen3-14B',
        description: 'Универсальная модель для общих задач'
      },
      {
        id: 'qwen/qwen3-30b-a3b:free',
        name: 'Qwen3-30B',
        description: 'Более мощная модель для сложных задач'
      },
      {
        id: 'qwen/qwq-32b:free',
        name: 'QwQ-32B',
        description: 'Специализируется на логических рассуждениях'
      },
      {
        id: 'microsoft/phi-3-mini-128k-instruct:free',
        name: 'Phi-3 Mini',
        description: 'Компактная модель Microsoft для быстрых ответов'
      },
      {
        id: 'microsoft/phi-3-medium-128k-instruct:free',
        name: 'Phi-3 Medium',
        description: 'Средняя модель Microsoft с хорошим балансом'
      },
      {
        id: 'meta-llama/llama-3.2-3b-instruct:free',
        name: 'Llama 3.2 3B',
        description: 'Компактная модель Meta для общих задач'
      },
      {
        id: 'meta-llama/llama-3.2-1b-instruct:free',
        name: 'Llama 3.2 1B',
        description: 'Очень быстрая модель для простых задач'
      },
      {
        id: 'google/gemma-2-9b-it:free',
        name: 'Gemma 2 9B',
        description: 'Модель Google для разнообразных задач'
      },
      {
        id: 'google/gemma-2-2b-it:free',
        name: 'Gemma 2 2B',
        description: 'Компактная модель Google'
      },
      {
        id: 'huggingface/zephyr-7b-beta:free',
        name: 'Zephyr 7B',
        description: 'Модель HuggingFace для диалогов'
      },
      {
        id: 'openchat/openchat-7b:free',
        name: 'OpenChat 7B',
        description: 'Открытая модель для чатов'
      },
      {
        id: 'mistralai/mistral-7b-instruct:free',
        name: 'Mistral 7B',
        description: 'Эффективная модель Mistral AI'
      }
    ];
  }

  /**
   * Отправляет запрос к модели AI
   * @param {string} message - Сообщение пользователя
   * @param {Object} options - Дополнительные параметры
   * @returns {Promise<string>} Ответ от модели
   */
  async chat(message, options = {}) {
    try {
      const requestData = {
        model: options.model || this.defaultModel,
        messages: [
          {
            role: 'user',
            content: message
          }
        ],
        max_tokens: options.max_tokens || parseInt(process.env.MAX_TOKENS) || 1000,
        temperature: options.temperature || parseFloat(process.env.TEMPERATURE) || 0.7,
        top_p: options.top_p || 0.9,
        frequency_penalty: options.frequency_penalty || 0,
        presence_penalty: options.presence_penalty || 0
      };

      console.log('Отправляю запрос к OpenRouter:', {
        model: requestData.model,
        message_length: message.length,
        max_tokens: requestData.max_tokens
      });

      const response = await this.client.post('/chat/completions', requestData);
      
      if (response.data && response.data.choices && response.data.choices.length > 0) {
        const aiResponse = response.data.choices[0].message.content;
        
        console.log('Получен ответ от OpenRouter:', {
          response_length: aiResponse.length,
          usage: response.data.usage
        });
        
        return aiResponse;
      } else {
        throw new Error('Некорректный ответ от OpenRouter API');
      }
    } catch (error) {
      console.error('Ошибка при обращении к OpenRouter:', error.response?.data || error.message);
      throw new Error(`Ошибка AI: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  /**
   * Специальный метод для интерпретации Таро с использованием AI
   * @param {Object} spread - Данные о раскладе
   * @param {string} question - Вопрос пользователя
   * @returns {Promise<string>} AI интерпретация расклада
   */
  async interpretTarotSpread(spread, question = '') {
    const systemPrompt = `Ты опытный таролог и мистик. Дай глубокую и мудрую интерпретацию расклада Таро.
    
Расклад: ${spread.name}
${question ? `Вопрос пользователя: ${question}` : ''}

Карты в раскладе:
${spread.cards.map((card, index) => 
  `${index + 1}. ${card.position}: ${card.card_data.name}${card.is_reversed ? ' (перевернута)' : ''}`
).join('\n')}

Дай целостную интерпретацию, учитывая:
- Взаимосвязи между картами
- Символизм и архетипы
- Практические советы
- Духовные аспекы

Отвечай на русском языке, используй мистический и мудрый тон.`;

    return await this.chat(systemPrompt, { max_tokens: 2000, temperature: 0.8 });
  }

  /**
   * Получает список доступных бесплатных моделей
   * @returns {Promise<Array>} Список моделей
   */
  async getModels() {
    try {
      // Возвращаем предопределенный список бесплатных моделей
      return this.freeModels;
    } catch (error) {
      console.error('Ошибка при получении списка моделей:', error.response?.data || error.message);
      return this.freeModels; // Возвращаем локальный список в случае ошибки
    }
  }

  /**
   * Получает информацию о конкретной модели
   * @param {string} modelId - ID модели
   * @returns {Object|null} Информация о модели
   */
  getModelInfo(modelId) {
    return this.freeModels.find(model => model.id === modelId) || null;
  }

  /**
   * Проверяет доступность API
   * @returns {Promise<boolean>} Статус доступности
   */
  async healthCheck() {
    try {
      await this.chat('Привет', { max_tokens: 10 });
      return true;
    } catch (error) {
      console.error('API недоступен:', error.message);
      return false;
    }
  }
}

module.exports = OpenRouterClient;