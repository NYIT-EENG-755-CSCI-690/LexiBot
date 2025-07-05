
import { useEffect } from 'react';
import axios from 'axios';

const useWordOfTheDay = ({ setWord, setLoading }) => {
  useEffect(() => {
    const fetchWord = async () => {
      setLoading(true);
      const response = await axios.get('/api/node/word-of-the-day');
      setWord(response.data.toUpperCase());
      setLoading(false);
    };
    fetchWord();
  }, [setWord, setLoading]);
};

export default useWordOfTheDay;


