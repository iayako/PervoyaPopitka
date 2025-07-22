const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const OpenRouterClient = require('./lib/openrouter');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Инициализация AI клиента
const aiClient = new OpenRouterClient();

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

// API для получения информации о проекте
app.get('/api/info', (req, res) => {
  res.json({
    name: 'PervoyaPopitka AI',
    version: '1.0.0',
    description: 'AI-powered project using OpenRouter',
    models: {
      default: process.env.DEFAULT_MODEL,
      available: ['qwen/qwen3-14b:free', 'qwen/qwen3-30b-a3b:free', 'qwen/qwq-32b:free']
    },
    features: [
      'Chat with AI models',
      'Multiple model support',
      'Real-time responses',
      'Web interface'
    ]
  });
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
  
  // Проверка подключения к API при запуске
  aiClient.healthCheck().then(isHealthy => {
    console.log(`🏥 Статус API: ${isHealthy ? '✅ Здоров' : '❌ Недоступен'}`);
  }).catch(err => {
    console.log(`🏥 Ошибка проверки API: ${err.message}`);
  });
});