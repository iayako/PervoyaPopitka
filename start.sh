#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Запуск PervoyaPopitka AI...${NC}"

# Проверка наличия Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js не установлен. Установите Node.js 16+ для продолжения.${NC}"
    exit 1
fi

# Проверка наличия npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm не установлен. Установите npm для продолжения.${NC}"
    exit 1
fi

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Файл .env не найден. Создайте файл .env с вашим API ключом.${NC}"
    exit 1
fi

# Проверка API ключа
if ! grep -q "OPENROUTER_API_KEY=sk-" .env; then
    echo -e "${YELLOW}⚠️  Убедитесь, что в файле .env указан корректный OPENROUTER_API_KEY${NC}"
fi

# Установка зависимостей если нужно
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Устанавливаю зависимости...${NC}"
    npm install
fi

# Быстрый тест API
echo -e "${BLUE}🧪 Быстрая проверка API...${NC}"
timeout 10s node -e "
require('dotenv').config();
const OpenRouterClient = require('./lib/openrouter');
const client = new OpenRouterClient();
client.healthCheck().then(healthy => {
    console.log(healthy ? '✅ API доступен' : '❌ API недоступен');
    process.exit(healthy ? 0 : 1);
}).catch(err => {
    console.log('❌ Ошибка проверки API:', err.message);
    process.exit(1);
});
" || {
    echo -e "${RED}❌ Проблема с подключением к API. Проверьте ваш ключ и интернет.${NC}"
    exit 1
}

echo -e "${GREEN}✅ Все проверки пройдены!${NC}"
echo -e "${BLUE}🌐 Запускаю веб-сервер...${NC}"
echo -e "${YELLOW}Откройте браузер и перейдите на: http://localhost:3000${NC}"
echo -e "${YELLOW}Для остановки сервера нажмите Ctrl+C${NC}"
echo ""

# Запуск сервера
npm start