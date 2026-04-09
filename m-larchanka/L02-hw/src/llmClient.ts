import axios from 'axios';
import { LLM_API_URL } from './config';
import fs from 'fs';

export async function generateLLMResponse(prompt: string, model: string, params: any) {
  console.log(`-> LLM[${model}] ${prompt}`)
  const response = await axios.post(LLM_API_URL, {
    model,
    prompt,
    stream: false,
    ...params
  });
  //console.log('+++response: ', response);
  // Сохраняем ответ в файл
  try {
    fs.writeFileSync('last-llm-resp.txt', typeof response.data === 'string' ? response.data : JSON.stringify(response.data, null, 2), 'utf-8');
  } catch (err) {
    console.error('Ошибка записи last-llm-resp.txt:', err);
  }
  return response.data.response;
}
