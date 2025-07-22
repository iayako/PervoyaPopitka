/**
 * Telegram бот с AI и Таро функциональностью
 */

const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const OpenRouterClient = require('../lib/openrouter');
const { TarotSpreadSystem } = require('../lib/tarot/spreads');

class TelegramAIBot {
  constructor() {
    this.token = process.env.TELEGRAM_BOT_TOKEN;
    
    if (!this.token) {
      throw new Error('TELEGRAM_BOT_TOKEN не найден в переменных окружения');
    }

    this.bot = new TelegramBot(this.token, { polling: true });
    this.aiClient = new OpenRouterClient();
    this.tarotSystem = new TarotSpreadSystem();
    
    this.userSessions = new Map(); // Для хранения состояния пользователей
    
    this.setupHandlers();
    console.log('🤖 Telegram бот запущен!');
  }

  setupHandlers() {
    // Команды
    this.bot.onText(/\/start/, (msg) => this.handleStart(msg));
    this.bot.onText(/\/help/, (msg) => this.handleHelp(msg));
    this.bot.onText(/\/tarot/, (msg) => this.handleTarotMenu(msg));
    this.bot.onText(/\/ai/, (msg) => this.handleAIMenu(msg));
    this.bot.onText(/\/models/, (msg) => this.handleModels(msg));
    
    // Callback queries (кнопки)
    this.bot.on('callback_query', (query) => this.handleCallbackQuery(query));
    
    // Текстовые сообщения
    this.bot.on('message', (msg) => this.handleMessage(msg));
    
    // Обработка ошибок
    this.bot.on('error', (error) => {
      console.error('Ошибка бота:', error);
    });
  }

  async handleStart(msg) {
    const chatId = msg.chat.id;
    const username = msg.from.first_name || 'Пользователь';
    
    const welcomeMessage = `
🌟 **Добро пожаловать, ${username}!** 🌟

Я многофункциональный AI-бот с возможностями:

🤖 **AI Чат** - Общение с различными AI моделями
🔮 **Таро расклады** - Мистические предсказания и советы
✨ **Комбинированные функции** - AI интерпретация Таро раскладов

**Основные команды:**
/ai - Выбрать AI модель и задать вопрос
/tarot - Сделать расклад Таро
/models - Посмотреть доступные AI модели
/help - Подробная помощь

Просто напишите сообщение, и я отвечу как AI-ассистент, или используйте команды для специальных функций!
`;

    const keyboard = {
      inline_keyboard: [
        [
          { text: '🤖 AI Чат', callback_data: 'ai_chat' },
          { text: '🔮 Таро', callback_data: 'tarot_menu' }
        ],
        [
          { text: '🎯 Модели AI', callback_data: 'show_models' },
          { text: '❓ Помощь', callback_data: 'show_help' }
        ]
      ]
    };

    await this.bot.sendMessage(chatId, welcomeMessage, {
      parse_mode: 'Markdown',
      reply_markup: keyboard
    });
  }

  async handleHelp(msg) {
    const chatId = msg.chat.id;
    
    const helpMessage = `
📖 **Подробная помощь**

**🤖 AI Функции:**
• Выберите из ${this.aiClient.freeModels.length} бесплатных моделей
• Задавайте любые вопросы - программирование, творчество, советы
• Получайте AI интерпретацию Таро раскладов

**🔮 Таро Функции:**
• ${this.tarotSystem.getStatistics().spread_types} типов раскладов
• ${this.tarotSystem.getStatistics().total_cards} карт (${this.tarotSystem.getStatistics().major_arcana} Старших + ${this.tarotSystem.getStatistics().minor_arcana} Младших Арканов)
• Автоматические рекомендации раскладов по вашему вопросу

**🎭 Комбинированные функции:**
• AI анализ ваших Таро раскладов
• Персонализированные интерпретации
• Глубокие духовные советы

**💡 Советы по использованию:**
• Для обычного чата просто напишите сообщение
• Для Таро используйте /tarot
• Для смены AI модели используйте /ai
• Формулируйте вопросы четко для лучших результатов

_Пусть AI и древняя мудрость Таро помогут вам найти ответы!_ ✨
`;

    await this.bot.sendMessage(chatId, helpMessage, {
      parse_mode: 'Markdown'
    });
  }

  async handleTarotMenu(msg) {
    const chatId = msg.chat.id;
    const spreads = this.tarotSystem.getAvailableSpreads();
    
    const keyboard = {
      inline_keyboard: []
    };

    // Добавляем кнопки для каждого типа расклада
    spreads.forEach(spread => {
      keyboard.inline_keyboard.push([{
        text: `${spread.emoji} ${spread.name} (${spread.card_count} карт)`,
        callback_data: `tarot_${spread.id}`
      }]);
    });

    // Добавляем дополнительные опции
    keyboard.inline_keyboard.push([
      { text: '🎲 Случайный расклад', callback_data: 'tarot_random' },
      { text: '📊 Статистика карт', callback_data: 'tarot_stats' }
    ]);

    const message = `
🔮 **Выберите тип Таро расклада:**

Доступно ${spreads.length} типов раскладов для различных жизненных ситуаций.

_Совет: После расклада вы можете получить дополнительную AI интерпретацию!_
`;

    await this.bot.sendMessage(chatId, message, {
      parse_mode: 'Markdown',
      reply_markup: keyboard
    });
  }

  async handleAIMenu(msg) {
    const chatId = msg.chat.id;
    const models = await this.aiClient.getModels();
    
    const keyboard = {
      inline_keyboard: []
    };

    // Группируем модели по 2 в ряд для компактности
    for (let i = 0; i < models.length; i += 2) {
      const row = [];
      row.push({
        text: models[i].name,
        callback_data: `ai_model_${models[i].id}`
      });
      
      if (i + 1 < models.length) {
        row.push({
          text: models[i + 1].name,
          callback_data: `ai_model_${models[i + 1].id}`
        });
      }
      
      keyboard.inline_keyboard.push(row);
    }

    const message = `
🤖 **Выберите AI модель:**

Доступно ${models.length} бесплатных моделей с различными специализациями:

• **Универсальные** - для общих задач
• **Мощные** - для сложных вопросов  
• **Быстрые** - для простых запросов
• **Специализированные** - для конкретных областей

_После выбора модели просто напишите ваш вопрос!_
`;

    await this.bot.sendMessage(chatId, message, {
      parse_mode: 'Markdown',
      reply_markup: keyboard
    });
  }

  async handleModels(msg) {
    const chatId = msg.chat.id;
    const models = await this.aiClient.getModels();
    
    let message = '🎯 **Доступные AI модели:**\n\n';
    
    models.forEach((model, index) => {
      message += `**${index + 1}. ${model.name}**\n`;
      message += `_${model.description}_\n`;
      message += `ID: \`${model.id}\`\n\n`;
    });

    message += '_Все модели бесплатные! Выберите подходящую для ваших задач._';

    await this.bot.sendMessage(chatId, message, {
      parse_mode: 'Markdown'
    });
  }

  async handleCallbackQuery(query) {
    const chatId = query.message.chat.id;
    const data = query.data;
    const userId = query.from.id;

    try {
      await this.bot.answerCallbackQuery(query.id);

      if (data.startsWith('tarot_')) {
        await this.handleTarotCallback(chatId, userId, data, query);
      } else if (data.startsWith('ai_model_')) {
        await this.handleAIModelCallback(chatId, userId, data, query);
      } else if (data.startsWith('ai_interpret_')) {
        await this.handleAIInterpretation(chatId, userId, data.replace('ai_interpret_', ''));
      } else if (data === 'ai_chat') {
        await this.handleAIMenu({ chat: { id: chatId } });
      } else if (data === 'tarot_menu') {
        await this.handleTarotMenu({ chat: { id: chatId } });
      } else if (data === 'show_models') {
        await this.handleModels({ chat: { id: chatId } });
      } else if (data === 'show_help') {
        await this.handleHelp({ chat: { id: chatId } });
      }
    } catch (error) {
      console.error('Ошибка в handleCallbackQuery:', error);
      await this.bot.sendMessage(chatId, '❌ Произошла ошибка. Попробуйте снова.');
    }
  }

  async handleTarotCallback(chatId, userId, data, query) {
    const spreadType = data.replace('tarot_', '');
    
    if (spreadType === 'random') {
      // Случайный расклад
      const spread = this.tarotSystem.createRandomSpread();
      await this.sendTarotSpread(chatId, spread, true);
    } else if (spreadType === 'stats') {
      // Статистика
      const stats = this.tarotSystem.getStatistics();
      const message = `
📊 **Статистика Таро системы:**

🎴 **Всего карт:** ${stats.total_cards}
🔮 **Старшие Арканы:** ${stats.major_arcana}
🃏 **Младшие Арканы:** ${stats.minor_arcana}
✨ **Типы раскладов:** ${stats.spread_types}
🎭 **Мастей:** ${stats.suits}

_Система готова для любых магических консультаций!_
`;
      await this.bot.editMessageText(message, {
        chat_id: chatId,
        message_id: query.message.message_id,
        parse_mode: 'Markdown'
      });
    } else {
      // Конкретный тип расклада
      try {
        const spread = this.tarotSystem.createSpread(spreadType);
        await this.sendTarotSpread(chatId, spread, true);
      } catch (error) {
        await this.bot.sendMessage(chatId, `❌ Ошибка создания расклада: ${error.message}`);
      }
    }
  }

  async handleAIModelCallback(chatId, userId, data, query) {
    const modelId = data.replace('ai_model_', '');
    const modelInfo = this.aiClient.getModelInfo(modelId);
    
    if (!modelInfo) {
      await this.bot.sendMessage(chatId, '❌ Модель не найдена');
      return;
    }

    // Сохраняем выбранную модель в сессии пользователя
    this.userSessions.set(userId, {
      selectedModel: modelId,
      mode: 'ai_chat'
    });

    const message = `
✅ **Выбрана модель: ${modelInfo.name}**

_${modelInfo.description}_

Теперь просто напишите ваш вопрос, и я отвечу используя эту модель!

**Примеры вопросов:**
• Объясни квантовую физику простыми словами
• Помоги написать код на Python
• Дай совет по карьере
• Сочини короткий рассказ
`;

    await this.bot.editMessageText(message, {
      chat_id: chatId,
      message_id: query.message.message_id,
      parse_mode: 'Markdown'
    });
  }

  async sendTarotSpread(chatId, spread, withAIOption = false) {
    // Отправляем расклад
    const message = this.tarotSystem.formatSpreadMessage(spread);
    
    const keyboard = withAIOption ? {
      inline_keyboard: [
        [
          { text: '🤖 AI Интерпретация', callback_data: `ai_interpret_${spread.type}` },
          { text: '🔄 Новый расклад', callback_data: 'tarot_menu' }
        ]
      ]
    } : undefined;

    await this.bot.sendMessage(chatId, message, {
      parse_mode: 'Markdown',
      reply_markup: keyboard
    });

    // Сохраняем последний расклад для возможной AI интерпретации
    const userId = chatId; // В приватных чатах chatId = userId
    const session = this.userSessions.get(userId) || {};
    session.lastSpread = spread;
    this.userSessions.set(userId, session);
  }

  async handleMessage(msg) {
    if (msg.text && msg.text.startsWith('/')) {
      return; // Команды обрабатываются отдельно
    }

    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const text = msg.text;

    if (!text) return;

    try {
      const session = this.userSessions.get(userId) || {};
      const selectedModel = session.selectedModel || this.aiClient.defaultModel;

      // Показываем индикатор печати
      await this.bot.sendChatAction(chatId, 'typing');

      // Получаем ответ от AI
      const response = await this.aiClient.chat(text, { 
        model: selectedModel,
        max_tokens: 1500,
        temperature: 0.7
      });

      // Отправляем ответ
      await this.bot.sendMessage(chatId, response, {
        parse_mode: 'Markdown'
      });

    } catch (error) {
      console.error('Ошибка AI ответа:', error);
      await this.bot.sendMessage(chatId, `❌ Ошибка AI: ${error.message}`);
    }
  }

  async handleAIInterpretation(chatId, userId, spreadType) {
    const session = this.userSessions.get(userId);
    
    if (!session || !session.lastSpread) {
      await this.bot.sendMessage(chatId, '❌ Не найден расклад для интерпретации');
      return;
    }

    try {
      await this.bot.sendChatAction(chatId, 'typing');
      
      const interpretation = await this.aiClient.interpretTarotSpread(session.lastSpread);
      
      const message = `
🤖 **AI Интерпретация расклада "${session.lastSpread.name}":**

${interpretation}

_Эта интерпретация создана искусственным интеллектом на основе традиционных значений карт Таро._
`;

      await this.bot.sendMessage(chatId, message, {
        parse_mode: 'Markdown'
      });

    } catch (error) {
      console.error('Ошибка AI интерпретации:', error);
      await this.bot.sendMessage(chatId, `❌ Ошибка AI интерпретации: ${error.message}`);
    }
  }
}

// Запуск бота
if (require.main === module) {
  try {
    new TelegramAIBot();
  } catch (error) {
    console.error('Ошибка запуска бота:', error.message);
    process.exit(1);
  }
}

module.exports = TelegramAIBot;