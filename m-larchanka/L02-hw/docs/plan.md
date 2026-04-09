# План разработки Telegram-бота для взаимодействия с локальной LLM

## 1. Выбор инструментов и технологий

- **Язык:** TypeScript
- **Telegram Bot API:** [node-telegram-bot-api](https://github.com/yagop/node-telegram-bot-api)
- **HTTP-клиент:** [axios](https://github.com/axios/axios) для запросов к LLM API
- **Менеджер пакетов:** npm или yarn
- **Конфигурация:** dotenv для хранения токена бота и настроек

## 2. Структура проекта

```
/src
  bot.ts
  llmClient.ts
  config.ts
.env
package.json
tsconfig.json
```

## 3. Основные шаги реализации

### 3.1. Инициализация проекта

```sh
npm init -y
npm install typescript node-telegram-bot-api axios dotenv
npx tsc --init
```

### 3.2. Создание файла конфигурации

**.env**
```
TELEGRAM_TOKEN=telegram_bot_token
LLM_API_URL=http://127.0.0.1:11434/api/generate
```

**src/config.ts**

```typescript
import dotenv from 'dotenv';
dotenv.config();

export const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN!;
export const LLM_API_URL = process.env.LLM_API_URL!;
```

### 3.3. Клиент для LLM

**src/llmClient.ts**
```typescript
import axios from 'axios';
import { LLM_API_URL } from './config';

export async function generateLLMResponse(prompt: string, model: string, params: any) {
  const response = await axios.post(LLM_API_URL, {
    prompt,
    model,
    ...params
  });
  return response.data.response;
}
```

### 3.4. Реализация Telegram-бота

**src/bot.ts**
```typescript
import TelegramBot from 'node-telegram-bot-api';
import { TELEGRAM_TOKEN } from './config';
import { generateLLMResponse } from './llmClient';

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

let currentModel = 'default';
let generationParams: any = {};

bot.onText(/\/model (.+)/, (msg, match) => {
  currentModel = match![1];
  bot.sendMessage(msg.chat.id, `Модель установлена: ${currentModel}`);
});

bot.onText(/\/param (\w+) (.+)/, (msg, match) => {
  const key = match![1];
  const value = match![2];
  generationParams[key] = value;
  bot.sendMessage(msg.chat.id, `Параметр ${key} установлен в ${value}`);
});

bot.on('message', async (msg) => {
  if (msg.text && !msg.text.startsWith('/')) {
    const reply = await generateLLMResponse(msg.text, currentModel, generationParams);
    bot.sendMessage(msg.chat.id, reply);
  }
});
```

### 3.5. Запуск бота

Добавить в `package.json`:
```json
"scripts": {
  "start": "ts-node src/bot.ts"
}
```
Запуск:

```sh
npm run start
```

## 4. Особенности

- Каждое сообщение обрабатывается независимо, история не хранится.
- Поддерживаются команды:
  - `/model <имя_модели>` — выбор модели
  - `/param <параметр> <значение>` — установка параметра генерации

---

Этот план можно использовать для автоматической или ручной генерации кода Telegram-бота, соответствующего требованиям.
