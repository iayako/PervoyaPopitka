# Инструкции по развертыванию PervoyaPopitka AI

## 🚀 Быстрый старт

### 1. Предварительные требования
- Node.js 16+ установлен
- npm или yarn
- Интернет-соединение для API запросов

### 2. Установка
```bash
# Клонирование репозитория (если нужно)
git clone <your-repo-url>
cd pervoyapopitka-ai

# Установка зависимостей
npm install
```

### 3. Настройка переменных окружения
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование .env файла
nano .env  # или любой другой редактор
```

Обязательные переменные:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Получите бесплатный API ключ на [OpenRouter](https://openrouter.ai/):
1. Зарегистрируйтесь на сайте
2. Перейдите в раздел Keys
3. Создайте новый ключ
4. Скопируйте и вставьте в .env файл

### 4. Запуск приложения

#### Только веб-интерфейс:
```bash
npm start
```
Приложение будет доступно на http://localhost:3000

#### Только Telegram бот:
```bash
npm run bot
```
Требует настройки TELEGRAM_BOT_TOKEN в .env

#### Все сервисы одновременно:
```bash
npm run start-all
```
Запустит и веб-интерфейс, и Telegram бота

## 🤖 Настройка Telegram бота

### 1. Создание бота
1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. Получите токен бота

### 2. Настройка
Добавьте токен в .env файл:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Запуск
```bash
npm run bot
# или
npm run start-all
```

## 🌐 Развертывание в продакшене

### На VPS/сервере

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Проверка установки
node --version
npm --version
```

#### 2. Развертывание приложения
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd pervoyapopitka-ai

# Установка зависимостей
npm install --production

# Настройка окружения
cp .env.example .env
nano .env
```

#### 3. Настройка PM2 (рекомендуется)
```bash
# Установка PM2
sudo npm install -g pm2

# Создание конфигурации PM2
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [
    {
      name: 'pervoyapopitka-web',
      script: 'index.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    },
    {
      name: 'pervoyapopitka-bot',
      script: 'bot/telegram-bot.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};
EOF

# Запуск с PM2
pm2 start ecosystem.config.js

# Автозапуск при перезагрузке сервера
pm2 startup
pm2 save
```

#### 4. Настройка Nginx (опционально)
```bash
# Установка Nginx
sudo apt install nginx -y

# Создание конфигурации
sudo cat > /etc/nginx/sites-available/pervoyapopitka << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/pervoyapopitka /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### На Heroku

#### 1. Подготовка
```bash
# Установка Heroku CLI
# Следуйте инструкциям на https://devcenter.heroku.com/articles/heroku-cli

# Вход в Heroku
heroku login
```

#### 2. Создание приложения
```bash
# Создание приложения
heroku create your-app-name

# Установка переменных окружения
heroku config:set OPENROUTER_API_KEY=your_api_key
heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
heroku config:set NODE_ENV=production
```

#### 3. Развертывание
```bash
# Деплой
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Просмотр логов
heroku logs --tail
```

### На Railway

#### 1. Подготовка
1. Зарегистрируйтесь на [Railway](https://railway.app/)
2. Подключите GitHub репозиторий

#### 2. Настройка
1. Добавьте переменные окружения в Railway dashboard:
   - `OPENROUTER_API_KEY`
   - `TELEGRAM_BOT_TOKEN` (опционально)
   - `PORT` (автоматически)

#### 3. Деплой
Railway автоматически развернет приложение при push в репозиторий.

## 🔧 Мониторинг и обслуживание

### Логи
```bash
# PM2 логи
pm2 logs

# Логи конкретного приложения
pm2 logs pervoyapopitka-web
pm2 logs pervoyapopitka-bot

# Системные логи
sudo journalctl -u nginx -f
```

### Обновления
```bash
# Обновление кода
git pull origin main
npm install --production

# Перезапуск с PM2
pm2 restart ecosystem.config.js

# Или без PM2
npm run start-all
```

### Бэкап конфигурации
```bash
# Создание бэкапа .env
cp .env .env.backup

# Бэкап PM2 конфигурации
pm2 save
```

## 🔒 Безопасность

### 1. Переменные окружения
- Никогда не коммитьте .env файл
- Используйте сильные API ключи
- Регулярно меняйте токены

### 2. Сервер
```bash
# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable

# Обновления безопасности
sudo apt update && sudo apt upgrade -y
```

### 3. Nginx
```bash
# Базовая защита
sudo nano /etc/nginx/nginx.conf
# Добавьте:
# server_tokens off;
# client_max_body_size 1M;
```

## 📊 Мониторинг использования

### OpenRouter
1. Войдите в [OpenRouter Dashboard](https://openrouter.ai/)
2. Проверьте использование API
3. Мониторьте лимиты и расходы

### Telegram Bot
1. Используйте @BotFather для статистики
2. Мониторьте логи бота
3. Отслеживайте ошибки в PM2

## 🚨 Устранение неполадок

### Частые проблемы

#### 1. API ключ не работает
```bash
# Проверка переменных окружения
echo $OPENROUTER_API_KEY

# Тест API
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/models
```

#### 2. Порт уже используется
```bash
# Найти процесс на порту
sudo lsof -i :3000

# Убить процесс
sudo kill -9 <PID>
```

#### 3. Telegram бот не отвечает
```bash
# Проверка токена
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe

# Проверка логов
pm2 logs pervoyapopitka-bot
```

#### 4. Недостаточно памяти
```bash
# Проверка использования памяти
free -h
pm2 monit

# Увеличение лимита PM2
pm2 restart pervoyapopitka-web --max-memory-restart 2G
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь в правильности конфигурации .env
3. Проверьте статус API сервисов
4. Создайте issue в GitHub репозитории

---

**Удачного развертывания! 🚀**