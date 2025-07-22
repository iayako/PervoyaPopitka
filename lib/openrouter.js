const axios = require('axios');
require('dotenv').config();

class OpenRouterClient {
  constructor() {
    this.apiKey = process.env.OPENROUTER_API_KEY;
    this.baseURL = process.env.OPENROUTER_BASE_URL;
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
   * Получает список доступных моделей
   * @returns {Promise<Array>} Список моделей
   */
  async getModels() {
    try {
      const response = await this.client.get('/models');
      return response.data.data.filter(model => model.pricing.prompt === 0); // Только бесплатные модели
    } catch (error) {
      console.error('Ошибка при получении списка моделей:', error.response?.data || error.message);
      throw new Error(`Ошибка получения моделей: ${error.message}`);
    }
  }

  /**
   * Проверяет доступность API
   * @returns {Promise<boolean>} Статус доступности
   */
  async healthCheck() {
    try {
      await this.client.get('/models');
      return true;
    } catch (error) {
      console.error('API недоступен:', error.message);
      return false;
    }
  }
}

module.exports = OpenRouterClient;