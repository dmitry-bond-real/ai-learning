import dotenv from 'dotenv';
dotenv.config();

export const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN!;
export const LLM_API_URL = process.env.LLM_API_URL!;
export const DEFAULT_MODEL = process.env.DEFAULT_MODEL || 'qwen3.5:latest';
export const AVAILABLE_MODELS = (process.env.AVAILABLE_MODELS || '').split(',').map(m => m.trim()).filter(Boolean);

//console.log(`tlgr.TK: ${TELEGRAM_TOKEN}`);
//console.log(`llm.API: ${LLM_API_URL}`)