const express = require('express');
const cors = require('cors');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const bufferWordList = fs.readFileSync('./src/assets/word_list.json', 'utf8');
const acceptableWordArr = JSON.parse(bufferWordList);

const bufferWordListAll= fs.readFileSync('./src/assets/all_words.json', 'utf8');
const candidateWordArr = JSON.parse(bufferWordListAll);

const startDate = new Date('1 Mar 2022');
const calculateTime = (event, startDate) => {
  return (event.getTime() - startDate.getTime()) / (1000 * 3600 * 24);
};
const getIndexUsingTime = () => {
  const time = calculateTime(new Date(), startDate);
  return Math.floor(Math.abs(time)) % acceptableWordArr.length;
};

app.get('/word-of-the-day', (req, res) => {
  const todaysWord = acceptableWordArr[getIndexUsingTime()].toUpperCase();
  // console.log('here', todaysWord);
  if (todaysWord) {
    setTimeout(() => res.json(todaysWord), 500);
  } else {
    res.status(404).json({ error: 'word not found' });
  }
});

// TODO add Post for word validation
app.post('/validate-word', (req, res) => {
  const { word } = req.body; // pull out key in object received

  const isValid = candidateWordArr.includes(word.toLowerCase());
  // res.json({ validWord: isValid }); // send back object as json
  setTimeout(() => res.json({ validWord: isValid }), 500);
});

console.log('Starting server on port 3000');
console.log('Fetched word of the day');
app.listen(3000);
