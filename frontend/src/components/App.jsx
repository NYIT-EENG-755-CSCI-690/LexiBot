import React, { useState, useEffect } from 'react';
import Grid from './Grid';
import Spinner from './Spinner';
import Keyboard from './Keyboard';
import QueryButton from './QueryButton';
import axios from 'axios';
import unique_words from '../assets/word_list';
import { isLetter, makeMap, getCSRFToken } from './Utils';
import useWordOfTheDay from './useWordOfTheDay';
import checkValidWordSubmission from './checkValidWordSubmission';
import handleWordCorrection from './handleWordCorrection';

import logo from '../assets/logo.png';

const ANSWER_LENGTH = 5;
const ROUNDS = 6;

const createEmptyGrid = () =>
  Array(ROUNDS)
    .fill()
    .map(() => ({
      letters: Array(ANSWER_LENGTH).fill(''),
      statuses: Array(ANSWER_LENGTH).fill(''),
    }));

const App = () => {
  const [invalid, setInvalid] = useState(false);
  const [grid, setGrid] = useState(createEmptyGrid());
  const [currentRow, setCurrentRow] = useState(0);
  const [currentGuess, setCurrentGuess] = useState('');
  const [word, setWord] = useState('');
  const [loading, setLoading] = useState(true);
  const [done, setDone] = useState(false);
  const [wordReveal, setWordreveal] = useState(false);
  const [botSteps, setBotSteps] = useState([]);

  useEffect(() => {
    const fetchCSRF = async () => {
      const response = await fetch('/api/django/csrf/', {
        method: 'GET',
        credentials: 'include', // <-- this is key
      });
      const data = await response.json();
    };
    fetchCSRF();
  }, []);

  useWordOfTheDay({ setWord, setLoading }); // word

  const getWordleSteps = async () => {
    const csrftoken = getCSRFToken();
    const response = await fetch('/api/django/wordle-solver/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ answer: word.toLowerCase() }),
    });

    const data = await response.json();
    setBotSteps(data.history);
  };

  const handleAddLetter = (letter) => {
    let updatedGuess;
    if (currentGuess.length < ANSWER_LENGTH) {
      updatedGuess = currentGuess + letter;
    } else {
      updatedGuess = currentGuess.slice(0, -1) + letter;
    }
    updateGrid(updatedGuess);
  };

  const handleBackSpace = () => {
    const updatedGuess = currentGuess.slice(0, -1);
    updateGrid(updatedGuess);
  };

  const updateGrid = (guess) => {
    const updatedGrid = [...grid];
    updatedGrid[currentRow].letters = Array.from(guess.padEnd(ANSWER_LENGTH));
    setGrid(updatedGrid);
    setCurrentGuess(guess);
  };

  const handleRowSubmit = async () => {
    if (currentGuess.length !== ANSWER_LENGTH) return;

    const isValidWord = await checkValidWordSubmission({
      setLoading,
      currentGuess,
    });


    if (!isValidWord) {
      setInvalid(true);
      // remove the class after 500ms
      setTimeout(() => setInvalid(false), 500);
    
      const data = await handleWordCorrection(currentGuess);

      if (data.corrected_word !== currentGuess) {
        setCurrentGuess(data.corrected_word);
        updateGrid(data.corrected_word);
      }

      return;
    }

    const result = Array(ANSWER_LENGTH).fill('');
    const map = makeMap(word);

    // First pass
 

    for (let i = 0; i < ANSWER_LENGTH; i++) {
      if (currentGuess[i] === word[i]) {
        result[i] = 'correct';
        map[currentGuess[i]]--;
      }
    }

    for (let i = 0; i < ANSWER_LENGTH; i++) {
      if (result[i]) continue;
      // value exists in word of the day as a dup
      if (map[currentGuess[i]] > 0) {
        result[i] = 'incorrectly-placed';
        map[currentGuess[i]]--;
      } else {
        result[i] = 'incorrect';
   
      }
    }

    const updatedGrid = [...grid];
    updatedGrid[currentRow].statuses = result;
    setGrid(updatedGrid); // update grid with a copy

    if (currentGuess === word) {
      setDone(true);
    } else if (currentRow === ROUNDS - 1) {
      // ran out of tries
      setDone(true);
      setWordreveal(true);
    } else {
      setCurrentRow(currentRow + 1);
      setCurrentGuess('');
    }
  };

  const handleAppKeyPress = (key) => {
    if (done || loading) return;

    if (key === 'ENTER') {
      handleRowSubmit();
      // submit candidate words here
    } else if (key === 'DEL') {
      handleBackSpace();
    } else if (/^[a-zA-Z]$/.test(key)) {
      handleAddLetter(key.toUpperCase());
    }
  };

  useEffect(() => {
    const listener = (e) => {
      if (done || loading) return;

      if (e.key === 'Enter') {
        handleRowSubmit();
      } else if (e.key === 'Backspace') {
        handleBackSpace();
      } else if (isLetter(e.key)) {
        handleAddLetter(e.key.toUpperCase());
      }
    };

    window.addEventListener('keydown', listener);
    return () => window.removeEventListener('keydown', listener);
  }, [done, loading, handleRowSubmit, handleBackSpace, handleAddLetter]);

  return (
    <div className="container">
      <header className="navbar">
        <div className="header-brand">
          <div className="header-description">AI-powered Wordle Assistant</div>
          <div className="header-logo">
            <h1
              className={`brand ${
                done && currentGuess === word ? 'winner' : ''
              }`}
            >
              LexiBot
            </h1>
            <img src={logo} alt="LexiBot logo" className="logo-img" />
          </div>
        </div>
      </header>
      <Spinner
        loading={loading}
        wordReveal={wordReveal}
        word={word}
        botSteps={botSteps}
        done={done}
      />
      <Grid grid={grid} invalid={invalid} currentRow={currentRow} />
      <Keyboard handleKeyPress={handleAppKeyPress} />
      <QueryButton
        onQueryHandler={getWordleSteps}
        disabled={loading || !done}
      />
    </div>
  );
};

export default App;
