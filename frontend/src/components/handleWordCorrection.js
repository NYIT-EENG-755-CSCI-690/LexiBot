import { getCSRFToken } from './Utils';

const handleWordCorrection = async (currentGuess) => {
  const csrftoken = getCSRFToken();
  const response = await fetch('/api/django/word-correction/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFTOKEN': csrftoken,
    },
    body: JSON.stringify({ currentGuess: currentGuess.toLowerCase() }),
  });

  if (!response.ok) {
    const errorText = await response.text(); // Read raw HTML error
    console.error(`Request failed: ${response.status}`, errorText);
    throw new Error(`Word correction failed: ${response.status}`);
  }

  const data = await response.json();
  return data;
};

export default handleWordCorrection;
