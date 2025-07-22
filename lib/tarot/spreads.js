/**
 * Система раскладов Таро
 */

const { TarotCardSystem } = require('./cards');

const SPREAD_TYPES = {
  "one_card": {
    name: "Карта дня",
    description: "Одна карта, которая даст общий совет или покажет энергию дня",
    positions: ["Общий совет"],
    emoji: "🃏",
    card_count: 1
  },
  "three_cards": {
    name: "Прошлое-Настоящее-Будущее",
    description: "Три карты, показывающие влияние прошлого, настоящую ситуацию и возможное будущее",
    positions: ["Прошлое", "Настоящее", "Будущее"],
    emoji: "🔮",
    card_count: 3
  },
  "love_triangle": {
    name: "Любовный треугольник",
    description: "Расклад для вопросов о любви и отношениях",
    positions: ["Ваши чувства", "Чувства партнера", "Потенциал отношений"],
    emoji: "💕",
    card_count: 3
  },
  "decision": {
    name: "Принятие решения",
    description: "Поможет принять важное решение",
    positions: ["Текущая ситуация", "Вариант А", "Вариант Б", "Совет"],
    emoji: "⚖️",
    card_count: 4
  },
  "celtic_cross": {
    name: "Кельтский крест",
    description: "Полный расклад из 10 карт для глубокого анализа ситуации",
    positions: [
      "Текущая ситуация",
      "Препятствие/вызов", 
      "Далекое прошлое",
      "Недавнее прошлое",
      "Возможное будущее",
      "Ближайшее будущее",
      "Ваш подход",
      "Внешние влияния",
      "Надежды и страхи",
      "Итоговый результат"
    ],
    emoji: "✨",
    card_count: 10
  },
  "chakra": {
    name: "Расклад на чакры",
    description: "Анализ энергетического состояния семи основных чакр",
    positions: [
      "Муладхара (корневая)",
      "Свадхистхана (сакральная)", 
      "Манипура (солнечное сплетение)",
      "Анахата (сердечная)",
      "Вишудха (горловая)",
      "Аджна (третий глаз)",
      "Сахасрара (коронная)"
    ],
    emoji: "🌈",
    card_count: 7
  },
  "year_ahead": {
    name: "Год вперед",
    description: "Прогноз на каждый месяц следующего года",
    positions: [
      "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
      "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ],
    emoji: "📅",
    card_count: 12
  }
};

class TarotSpreadSystem {
  constructor() {
    this.cardSystem = new TarotCardSystem();
    this.spreadTypes = SPREAD_TYPES;
  }

  /**
   * Создает расклад выбранного типа
   * @param {string} spreadType - Тип расклада
   * @param {string} question - Вопрос пользователя (опционально)
   * @returns {Object} Объект расклада
   */
  createSpread(spreadType, question = '') {
    if (!this.spreadTypes[spreadType]) {
      throw new Error(`Неизвестный тип расклада: ${spreadType}`);
    }

    const spread = this.spreadTypes[spreadType];
    const cards = this.cardSystem.getRandomCards(spread.card_count);

    const spreadResult = {
      type: spreadType,
      name: spread.name,
      description: spread.description,
      emoji: spread.emoji,
      question: question,
      timestamp: new Date().toISOString(),
      cards: cards.map((card, index) => ({
        position: spread.positions[index],
        card_data: card,
        is_reversed: card.isReversed,
        interpretation: this.cardSystem.formatCardDescription(card, card.isReversed)
      }))
    };

    return spreadResult;
  }

  /**
   * Получает список доступных типов раскладов
   * @returns {Array} Массив типов раскладов
   */
  getAvailableSpreads() {
    return Object.keys(this.spreadTypes).map(key => ({
      id: key,
      ...this.spreadTypes[key]
    }));
  }

  /**
   * Получает информацию о конкретном раскладе
   * @param {string} spreadType - Тип расклада
   * @returns {Object|null} Информация о раскладе
   */
  getSpreadInfo(spreadType) {
    return this.spreadTypes[spreadType] || null;
  }

  /**
   * Форматирует расклад в текстовое сообщение
   * @param {Object} spread - Объект расклада
   * @returns {string} Отформатированное сообщение
   */
  formatSpreadMessage(spread) {
    let message = `${spread.emoji} **${spread.name}**\n\n`;
    message += `_${spread.description}_\n\n`;
    
    if (spread.question) {
      message += `**Ваш вопрос:** ${spread.question}\n\n`;
    }

    spread.cards.forEach((cardInfo, index) => {
      message += `**${index + 1}. ${cardInfo.position}**\n`;
      message += `${cardInfo.interpretation}\n\n`;
    });

    message += `_Время расклада: ${new Date(spread.timestamp).toLocaleString('ru-RU')}_`;
    
    return message;
  }

  /**
   * Получает статистику системы
   * @returns {Object} Статистика
   */
  getStatistics() {
    const cardStats = this.cardSystem.getStatistics();
    
    return {
      ...cardStats,
      spread_types: Object.keys(this.spreadTypes).length,
      available_spreads: this.getAvailableSpreads()
    };
  }

  /**
   * Создает случайный расклад
   * @param {string} question - Вопрос пользователя
   * @returns {Object} Случайный расклад
   */
  createRandomSpread(question = '') {
    const spreadTypes = Object.keys(this.spreadTypes);
    const randomType = spreadTypes[Math.floor(Math.random() * spreadTypes.length)];
    return this.createSpread(randomType, question);
  }

  /**
   * Получает рекомендации по раскладу на основе вопроса
   * @param {string} question - Вопрос пользователя
   * @returns {Array} Рекомендуемые типы раскладов
   */
  getRecommendedSpreads(question) {
    const lowerQuestion = question.toLowerCase();
    const recommendations = [];

    if (lowerQuestion.includes('любовь') || lowerQuestion.includes('отношения') || lowerQuestion.includes('партнер')) {
      recommendations.push('love_triangle');
    }
    
    if (lowerQuestion.includes('решение') || lowerQuestion.includes('выбор') || lowerQuestion.includes('что делать')) {
      recommendations.push('decision');
    }
    
    if (lowerQuestion.includes('будущее') || lowerQuestion.includes('что ждет')) {
      recommendations.push('three_cards');
    }
    
    if (lowerQuestion.includes('год') || lowerQuestion.includes('месяц')) {
      recommendations.push('year_ahead');
    }
    
    if (lowerQuestion.includes('энергия') || lowerQuestion.includes('чакра')) {
      recommendations.push('chakra');
    }

    // Если нет специфических ключевых слов, рекомендуем базовые расклады
    if (recommendations.length === 0) {
      recommendations.push('one_card', 'three_cards');
    }

    return recommendations.map(type => ({
      id: type,
      ...this.spreadTypes[type]
    }));
  }
}

module.exports = { TarotSpreadSystem, SPREAD_TYPES };