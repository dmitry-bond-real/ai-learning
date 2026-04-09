import fs from 'fs';
import path from 'path';

const logsDir = path.join(__dirname, '..', 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

const logStream = fs.createWriteStream(path.join(logsDir, 'bot.log'), { flags: 'a' });
const botCallsStream = fs.createWriteStream(path.join(logsDir, 'bot-calls.log'), { flags: 'a' });

export function logMessage(message: string) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  console.log(logLine.trim());
  logStream.write(logLine);
}

export function logBotCall(userId: number | undefined, username: string | undefined, text: string | undefined) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] User ${userId || '-'} (${username || '-'}) -> ${text || ''}\n`;
  botCallsStream.write(logLine);
}
