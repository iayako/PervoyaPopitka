const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const OpenRouterClient = require('./lib/openrouter');
const { TarotSpreadSystem } = require('./lib/tarot/spreads');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Инициализация AI клиента и Таро системы
const aiClient = new OpenRouterClient();
const tarotSystem = new TarotSpreadSystem();

// Маршруты
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API для общения с AI
app.post('/api/chat', async (req, res) => {
  try {
    const { message, model, options } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Сообщение не может быть пустым' });
    }

    console.log('Получен запрос от пользователя:', { message: message.substring(0, 100) + '...' });

    const aiResponse = await aiClient.chat(message, { model, ...options });
    
    res.json({ 
      response: aiResponse,
      model: model || process.env.DEFAULT_MODEL,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Ошибка в /api/chat:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// API для получения списка доступных моделей
app.get('/api/models', async (req, res) => {
  try {
    const models = await aiClient.getModels();
    res.json({ models });
  } catch (error) {
    console.error('Ошибка в /api/models:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// API для проверки статуса
app.get('/api/health', async (req, res) => {
  try {
    const isHealthy = await aiClient.healthCheck();
    res.json({ 
      status: isHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      model: process.env.DEFAULT_MODEL
    });
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// API для Таро раскладов

// Получить список доступных раскладов
app.get('/api/tarot/spreads', (req, res) => {
  try {
    const spreads = tarotSystem.getAvailableSpreads();
    res.json({ spreads });
  } catch (error) {
    console.error('Ошибка в /api/tarot/spreads:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Создать расклад
app.post('/api/tarot/spread', async (req, res) => {
  try {
    const { type, question } = req.body;
    
    if (!type) {
      return res.status(400).json({ error: 'Тип расклада не указан' });
    }

    console.log('Создание Таро расклада:', { type, question: question?.substring(0, 50) });

    const spread = tarotSystem.createSpread(type, question);
    
    res.json({ 
      spread,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Ошибка в /api/tarot/spread:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Получить случайный расклад
app.post('/api/tarot/random', async (req, res) => {
  try {
    const { question } = req.body;
    
    console.log('Создание случайного Таро расклада');

    const spread = tarotSystem.createRandomSpread(question);
    
    res.json({ 
      spread,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Ошибка в /api/tarot/random:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// AI интерпретация Таро расклада
app.post('/api/tarot/interpret', async (req, res) => {
  try {
    const { spread, question } = req.body;
    
    if (!spread) {
      return res.status(400).json({ error: 'Расклад не предоставлен' });
    }

    console.log('AI интерпретация Таро расклада:', { spreadName: spread.name });

    const interpretation = await aiClient.interpretTarotSpread(spread, question);
    
    res.json({ 
      interpretation,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Ошибка в /api/tarot/interpret:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Получить рекомендации раскладов по вопросу
app.post('/api/tarot/recommend', (req, res) => {
  try {
    const { question } = req.body;
    
    if (!question) {
      return res.status(400).json({ error: 'Вопрос не указан' });
    }

    const recommendations = tarotSystem.getRecommendedSpreads(question);
    
    res.json({ recommendations });
  } catch (error) {
    console.error('Ошибка в /api/tarot/recommend:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Статистика Таро системы
app.get('/api/tarot/stats', (req, res) => {
  try {
    const stats = tarotSystem.getStatistics();
    res.json({ stats });
  } catch (error) {
    console.error('Ошибка в /api/tarot/stats:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// API для получения информации о проекте
app.get('/api/info', async (req, res) => {
  try {
    const models = await aiClient.getModels();
    const tarotStats = tarotSystem.getStatistics();
    
    res.json({
      name: 'PervoyaPopitka AI',
      version: '2.0.0',
      description: 'AI-powered project using OpenRouter with Tarot reading functionality',
      features: [
        'Chat with multiple AI models',
        'Tarot card readings',
        'AI interpretation of Tarot spreads',
        'Web and Telegram bot interfaces',
        'Real-time responses'
      ],
      ai: {
        models: models.length,
        default: process.env.DEFAULT_MODEL,
        available: models.map(m => m.name)
      },
      tarot: {
        total_cards: tarotStats.total_cards,
        major_arcana: tarotStats.major_arcana,
        minor_arcana: tarotStats.minor_arcana,
        spread_types: tarotStats.spread_types
      }
    });
  } catch (error) {
    console.error('Ошибка в /api/info:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// Обработка ошибок
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Что-то пошло не так!' });
});

// Запуск сервера
app.listen(port, () => {
  console.log(`🚀 Сервер запущен на http://localhost:${port}`);
  console.log(`🤖 Используется модель: ${process.env.DEFAULT_MODEL}`);
  console.log(`🔑 API ключ настроен: ${process.env.OPENROUTER_API_KEY ? 'Да' : 'Нет'}`);
  console.log(`🔮 Таро система: ${tarotSystem.getStatistics().total_cards} карт, ${tarotSystem.getStatistics().spread_types} раскладов`);
  
  // Проверка подключения к API при запуске
  aiClient.healthCheck().then(isHealthy => {
    console.log(`🏥 Статус API: ${isHealthy ? '✅ Здоров' : '❌ Недоступен'}`);
  }).catch(err => {
    console.log(`🏥 Ошибка проверки API: ${err.message}`);
  });
});