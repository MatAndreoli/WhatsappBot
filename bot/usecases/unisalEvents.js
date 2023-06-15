const logger = require('../logger/loggerWinston');
const axios = require('axios');
const { readFile } = require('fs/promises');
const path = require('path');

const formatDate = (date) => {
  return /^(\d+\/\d+\/\d+)$/.test(date)
    ? date.split('/').reverse().join('/')
    : date;
};

const sortByDate = (data) => {
  data.sort((a, b) => {
    let first = new Date(a.date);
    let second = new Date(b.date);
    return first < second ? 1 : -1;
  });
  return data;
};

const buildEventsMsg = async () => {
  let msg = '';
  const data = JSON.parse(
    await readFile(path.resolve(__dirname, '../../WebScraper/events.json'), {
      encoding: 'utf8',
    })
  );

  sortByDate(data)
    .slice(0, 10)
    .forEach((value) => {
      msg += `Evento: *${value.title}*\nData: ${formatDate(value.date)}\t${
        value.hour
      }\nLink: ${value.link}\n\n`;
    });

  return msg;
};

const getUnisalEvents = async (client, from) => {
  try {
    logger.info('Retrieving Events');

    client.sendMessage(
      from,
      'Scraping https://unisal.br/eventos to get the data, it will take a while...'
    );

    await axios.get('http://localhost:3000/events');

    const msg = await buildEventsMsg();
    client.sendMessage(from, msg);
  } catch (e) {
    logger.error(`Some error occurred: ${e}`);
    client.sendMessage(from, `Some error occurred: ${e}`);
  }
};

module.exports = getUnisalEvents;
