
import axios from 'axios';

const checkValidWordSubmission = async ({ setLoading, currentGuess }) => {
  setLoading(true);
  const response = await axios.post('/api/node/validate-word', {
    word: currentGuess, // send to api as object
  });
  const { validWord } = response.data;

  setLoading(false);
  return validWord;
};

export default checkValidWordSubmission;
