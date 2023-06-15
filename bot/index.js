const qrcode = require('qrcode-terminal');
const onMessageCallback = require('./onMessage');
const logger = require('./logger/loggerWinston');
const { Client, LocalAuth } = require('whatsapp-web.js');

const client = new Client({
  puppeteer: {
    args: ['--no-sandbox'],
  },
  authStrategy: new LocalAuth(),
});

client.initialize();

client.on('authenticated', () => {
  logger.info('Authenticated');
});

client.on('qr', (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  logger.info('Client is ready!');
});

client.on(
  'message',
  async (message) => await onMessageCallback(client, message)
);
