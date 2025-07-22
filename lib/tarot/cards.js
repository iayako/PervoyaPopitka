/**
 * Система карт Таро с основными картами и их интерпретациями
 */

const MAJOR_ARCANA = [
  {
    id: 0,
    name: "Дурак",
    keywords: ["новые начинания", "невинность", "спонтанность"],
    description: "Символизирует новые начинания, чистый лист, готовность к приключениям",
    reversed_description: "Безрассудство, неосторожность, отсутствие направления"
  },
  {
    id: 1,
    name: "Маг",
    keywords: ["воля", "мастерство", "концентрация"],
    description: "Способность проявлять желания в реальность, сила воли",
    reversed_description: "Манипуляции, неиспользованный потенциал, слабая воля"
  },
  {
    id: 2,
    name: "Верховная Жрица",
    keywords: ["интуиция", "тайны", "подсознание"],
    description: "Внутренняя мудрость, интуиция, скрытые знания",
    reversed_description: "Игнорирование интуиции, поверхностность, секреты"
  },
  {
    id: 3,
    name: "Императрица",
    keywords: ["плодородие", "женственность", "изобилие"],
    description: "Материнская энергия, творчество, природная красота",
    reversed_description: "Зависимость, творческий блок, недостаток самоуважения"
  },
  {
    id: 4,
    name: "Император",
    keywords: ["власть", "структура", "контроль"],
    description: "Лидерство, стабильность, отцовская фигура",
    reversed_description: "Тирания, жесткость, потеря контроля"
  },
  {
    id: 5,
    name: "Иерофант",
    keywords: ["традиции", "духовность", "наставничество"],
    description: "Духовное руководство, традиции, обучение",
    reversed_description: "Догматизм, ограниченность, восстание против традиций"
  },
  {
    id: 6,
    name: "Влюбленные",
    keywords: ["любовь", "выбор", "гармония"],
    description: "Любовь, партнерство, важные решения",
    reversed_description: "Разлука, неправильный выбор, дисгармония"
  },
  {
    id: 7,
    name: "Колесница",
    keywords: ["победа", "контроль", "решимость"],
    description: "Триумф воли, контроль над ситуацией, движение вперед",
    reversed_description: "Отсутствие контроля, поражение, застой"
  },
  {
    id: 8,
    name: "Сила",
    keywords: ["мужество", "терпение", "сострадание"],
    description: "Внутренняя сила, мужество, терпение",
    reversed_description: "Слабость, отсутствие самоконтроля, жестокость"
  },
  {
    id: 9,
    name: "Отшельник",
    keywords: ["мудрость", "поиск", "внутренний свет"],
    description: "Поиск истины, внутренняя мудрость, духовное руководство",
    reversed_description: "Изоляция, отказ от помощи, заблуждения"
  },
  {
    id: 10,
    name: "Колесо Фортуны",
    keywords: ["судьба", "циклы", "удача"],
    description: "Перемены, циклы жизни, судьба",
    reversed_description: "Неудача, отсутствие контроля, негативные циклы"
  },
  {
    id: 11,
    name: "Справедливость",
    keywords: ["баланс", "истина", "карма"],
    description: "Справедливость, баланс, причина и следствие",
    reversed_description: "Несправедливость, дисбаланс, избежание ответственности"
  },
  {
    id: 12,
    name: "Повешенный",
    keywords: ["жертва", "новая перспектива", "ожидание"],
    description: "Новый взгляд на вещи, жертва ради высшей цели",
    reversed_description: "Мученичество, сопротивление переменам, эгоизм"
  },
  {
    id: 13,
    name: "Смерть",
    keywords: ["трансформация", "окончание", "возрождение"],
    description: "Трансформация, окончание старого, новые начинания",
    reversed_description: "Сопротивление переменам, застой, страх смерти"
  },
  {
    id: 14,
    name: "Умеренность",
    keywords: ["баланс", "терпение", "модерация"],
    description: "Баланс, умеренность, терпение",
    reversed_description: "Дисбаланс, излишества, нетерпение"
  },
  {
    id: 15,
    name: "Дьявол",
    keywords: ["искушение", "материализм", "зависимость"],
    description: "Искушение, материальные привязанности, зависимости",
    reversed_description: "Освобождение, разрыв цепей, духовное пробуждение"
  },
  {
    id: 16,
    name: "Башня",
    keywords: ["разрушение", "откровение", "освобождение"],
    description: "Внезапные перемены, разрушение иллюзий, освобождение",
    reversed_description: "Избежание катастрофы, внутренние перемены, сопротивление"
  },
  {
    id: 17,
    name: "Звезда",
    keywords: ["надежда", "вдохновение", "духовность"],
    description: "Надежда, вдохновение, духовное руководство",
    reversed_description: "Отчаяние, отсутствие веры, разочарование"
  },
  {
    id: 18,
    name: "Луна",
    keywords: ["иллюзии", "интуиция", "подсознание"],
    description: "Иллюзии, страхи, интуитивные знания",
    reversed_description: "Освобождение от иллюзий, ясность, преодоление страхов"
  },
  {
    id: 19,
    name: "Солнце",
    keywords: ["радость", "успех", "витальность"],
    description: "Радость, успех, позитивная энергия",
    reversed_description: "Временные неудачи, недостаток энтузиазма, задержки"
  },
  {
    id: 20,
    name: "Суд",
    keywords: ["возрождение", "призвание", "прощение"],
    description: "Духовное пробуждение, второй шанс, прощение",
    reversed_description: "Самосуд, отказ от прощения, упущенные возможности"
  },
  {
    id: 21,
    name: "Мир",
    keywords: ["завершение", "успех", "исполнение"],
    description: "Завершение цикла, достижение целей, гармония",
    reversed_description: "Незавершенность, отсутствие закрытия, задержки"
  }
];

const MINOR_ARCANA_SUITS = {
  "Жезлы": {
    element: "Огонь",
    keywords: ["страсть", "творчество", "энергия", "действие"],
    description: "Творческая энергия, страсть, карьера, духовный рост"
  },
  "Кубки": {
    element: "Вода", 
    keywords: ["эмоции", "любовь", "интуиция", "отношения"],
    description: "Эмоции, отношения, любовь, духовность"
  },
  "Мечи": {
    element: "Воздух",
    keywords: ["мысли", "конфликт", "общение", "интеллект"],
    description: "Мысли, общение, конфликты, интеллектуальные вызовы"
  },
  "Пентакли": {
    element: "Земля",
    keywords: ["материальность", "деньги", "работа", "здоровье"],
    description: "Материальный мир, деньги, работа, здоровье, практичность"
  }
};

class TarotCardSystem {
  constructor() {
    this.majorArcana = MAJOR_ARCANA;
    this.minorArcanaSuits = MINOR_ARCANA_SUITS;
    this.allCards = this.generateAllCards();
  }

  generateAllCards() {
    const cards = [...this.majorArcana];
    
    // Добавляем упрощенные Младшие Арканы
    Object.keys(this.minorArcanaSuits).forEach(suit => {
      const suitInfo = this.minorArcanaSuits[suit];
      
      // Добавляем числовые карты (Туз - 10)
      for (let i = 1; i <= 10; i++) {
        cards.push({
          id: `${suit.toLowerCase()}_${i}`,
          name: `${i} ${suit}`,
          suit: suit,
          number: i,
          keywords: suitInfo.keywords,
          description: `${i} ${suit} - ${suitInfo.description}`,
          reversed_description: `${i} ${suit} (перевернута) - блокированная энергия масти`
        });
      }

      // Добавляем придворные карты
      const courtCards = ["Паж", "Рыцарь", "Королева", "Король"];
      courtCards.forEach(court => {
        cards.push({
          id: `${suit.toLowerCase()}_${court.toLowerCase()}`,
          name: `${court} ${suit}`,
          suit: suit,
          court: court,
          keywords: suitInfo.keywords,
          description: `${court} ${suit} - ${suitInfo.description}`,
          reversed_description: `${court} ${suit} (перевернут) - негативные аспекты личности`
        });
      });
    });

    return cards;
  }

  getAllCards() {
    return this.allCards;
  }

  getRandomCards(count) {
    const shuffled = [...this.allCards].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count).map(card => ({
      ...card,
      isReversed: Math.random() < 0.3 // 30% шанс перевернутой карты
    }));
  }

  getCardById(id) {
    return this.allCards.find(card => card.id === id);
  }

  formatCardDescription(card, isReversed = false) {
    const description = isReversed ? card.reversed_description : card.description;
    const orientation = isReversed ? " (перевернута)" : "";
    
    return `🎴 **${card.name}${orientation}**\n\n${description}\n\n_Ключевые слова: ${card.keywords.join(', ')}_`;
  }

  getStatistics() {
    return {
      total_cards: this.allCards.length,
      major_arcana: this.majorArcana.length,
      minor_arcana: this.allCards.length - this.majorArcana.length,
      suits: Object.keys(this.minorArcanaSuits).length
    };
  }
}

module.exports = { TarotCardSystem, MAJOR_ARCANA, MINOR_ARCANA_SUITS };