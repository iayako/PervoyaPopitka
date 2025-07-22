#!/usr/bin/env node

/**
 * Скрипт для запуска веб-приложения и Telegram бота одновременно
 */

const { spawn } = require('child_process');
const path = require('path');
require('dotenv').config();

console.log('🚀 Запуск PervoyaPopitka AI...\n');

// Запуск веб-сервера
console.log('📡 Запуск веб-сервера...');
const webServer = spawn('node', ['index.js'], {
  stdio: 'inherit',
  cwd: __dirname
});

// Запуск Telegram бота (если токен настроен)
let telegramBot = null;
if (process.env.TELEGRAM_BOT_TOKEN) {
  console.log('🤖 Запуск Telegram бота...');
  telegramBot = spawn('node', ['bot/telegram-bot.js'], {
    stdio: 'inherit',
    cwd: __dirname
  });
} else {
  console.log('⚠️  TELEGRAM_BOT_TOKEN не настроен, Telegram бот не запущен');
}

console.log('\n✨ Все сервисы запущены!');
console.log('🌐 Веб-интерфейс: http://localhost:' + (process.env.PORT || 3000));
if (telegramBot) {
  console.log('📱 Telegram бот активен');
}
console.log('\n💡 Для остановки нажмите Ctrl+C\n');

// Обработка сигналов завершения
process.on('SIGINT', () => {
  console.log('\n🛑 Остановка сервисов...');
  
  if (webServer) {
    webServer.kill('SIGINT');
  }
  
  if (telegramBot) {
    telegramBot.kill('SIGINT');
  }
  
  setTimeout(() => {
    console.log('✅ Все сервисы остановлены');
    process.exit(0);
  }, 2000);
});

// Обработка ошибок
webServer.on('error', (error) => {
  console.error('❌ Ошибка веб-сервера:', error);
});

if (telegramBot) {
  telegramBot.on('error', (error) => {
    console.error('❌ Ошибка Telegram бота:', error);
  });
}

webServer.on('exit', (code) => {
  if (code !== 0) {
    console.error(`❌ Веб-сервер завершился с кодом ${code}`);
  }
});

if (telegramBot) {
  telegramBot.on('exit', (code) => {
    if (code !== 0) {
      console.error(`❌ Telegram бот завершился с кодом ${code}`);
    }
  });
}