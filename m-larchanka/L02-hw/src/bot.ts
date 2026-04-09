import TelegramBot from 'node-telegram-bot-api';
import { TELEGRAM_TOKEN, DEFAULT_MODEL, AVAILABLE_MODELS } from './config';
import { generateLLMResponse } from './llmClient';
import { logMessage, logBotCall } from './logger';
import fs from 'fs';

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });
console.log('Ready');

let helloText = 'Добро пожаловать!';
try {
  helloText = fs.readFileSync('hello.txt', 'utf-8');
} catch {}

let currentModel = DEFAULT_MODEL;
let generationParams: any = {};

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, helloText);
});

bot.onText(/\/model (.+)/, (msg, match) => {
  const input = match![1].trim();
  let selectedModel = '';
  // Если пользователь ввёл число, выбираем по индексу
  if (/^\d+$/.test(input)) {
    const idx = parseInt(input, 10) - 1;
    if (AVAILABLE_MODELS[idx]) {
      selectedModel = AVAILABLE_MODELS[idx];
    } else {
      bot.sendMessage(msg.chat.id, `Модель с номером ${input} не найдена.`);
      return;
    }
  } else {
    // Поиск по имени
    if (AVAILABLE_MODELS.includes(input)) {
      selectedModel = input;
    } else {
      bot.sendMessage(msg.chat.id, `Модель с именем ${input} не найдена.`);
      return;
    }
  }
  currentModel = selectedModel;
  bot.sendMessage(msg.chat.id, `Модель установлена: ${currentModel}`);
});

bot.onText(/\/param (\w+) (.+)/, (msg, match) => {
  const key = match![1];
  const value = match![2];
  generationParams[key] = value;
  bot.sendMessage(msg.chat.id, `Параметр ${key} установлен в ${value}`);
});

bot.onText(/\/models/, (msg) => {
  if (AVAILABLE_MODELS.length === 0) {
    bot.sendMessage(msg.chat.id, 'Список моделей не задан.');
  } else {
    const list = AVAILABLE_MODELS.map((m, i) => `${i + 1}. ${m}`).join('\n');
    bot.sendMessage(msg.chat.id, 'Доступные модели:\n' + list);
  }
});

bot.on('message', async (msg) => {
  logBotCall(msg.from?.id, msg.from?.username, msg.text);
  if (msg.text && !msg.text.startsWith('/')) {
    logMessage(`User ${msg.from?.id} (${msg.from?.username || ''}): ${msg.text}`);
    try {
      const reply = await generateLLMResponse(msg.text, currentModel, generationParams);
      logMessage(`Bot reply to ${msg.from?.id}: ${reply}`);
      bot.sendMessage(msg.chat.id, reply);
    } catch (e: any) {
      const errorText = e?.message || e?.toString() || 'Неизвестная ошибка';
      logMessage(`Bot error for ${msg.from?.id}: ${errorText}`);
      bot.sendMessage(msg.chat.id, `Ошибка генерации: ${errorText}`);
    }
  }
});
