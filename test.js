const OpenRouterClient = require('./lib/openrouter');

async function testAPI() {
  console.log('🧪 Запуск тестов API...\n');
  
  try {
    // Инициализация клиента
    const client = new OpenRouterClient();
    console.log('✅ Клиент OpenRouter инициализирован');
    
    // Проверка здоровья API
    console.log('\n🏥 Проверка подключения к API...');
    const isHealthy = await client.healthCheck();
    console.log(`Статус API: ${isHealthy ? '✅ Здоров' : '❌ Недоступен'}`);
    
    if (!isHealthy) {
      console.log('❌ API недоступен, завершаем тесты');
      return;
    }
    
    // Тест простого запроса
    console.log('\n💬 Тестируем простой запрос...');
    const testMessage = 'Привет! Скажи что-нибудь короткое на русском языке.';
    console.log(`Отправляем: "${testMessage}"`);
    
    const response = await client.chat(testMessage, { max_tokens: 100 });
    console.log(`Получен ответ: "${response}"`);
    console.log(`Длина ответа: ${response.length} символов`);
    
    // Тест с другой моделью
    console.log('\n🔄 Тестируем другую модель (QwQ-32B)...');
    const mathQuestion = 'Сколько будет 2+2? Ответь кратко.';
    console.log(`Отправляем: "${mathQuestion}"`);
    
    const mathResponse = await client.chat(mathQuestion, { 
      model: 'qwen/qwq-32b:free',
      max_tokens: 50 
    });
    console.log(`Получен ответ: "${mathResponse}"`);
    
    // Получение списка моделей
    console.log('\n📋 Получаем список доступных моделей...');
    try {
      const models = await client.getModels();
      console.log(`Найдено бесплатных моделей: ${models.length}`);
      models.slice(0, 3).forEach(model => {
        console.log(`  - ${model.id}: ${model.name || 'Без названия'}`);
      });
    } catch (error) {
      console.log('⚠️ Не удалось получить список моделей:', error.message);
    }
    
    console.log('\n✅ Все тесты пройдены успешно!');
    
  } catch (error) {
    console.error('\n❌ Ошибка при выполнении тестов:', error.message);
    process.exit(1);
  }
}

// Запуск тестов
if (require.main === module) {
  testAPI();
}

module.exports = testAPI;