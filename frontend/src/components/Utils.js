export const isLetter = (letter) => /^[a-zA-Z]$/.test(letter);

export const makeMap = (array) => {
  const obj = {};
  for (let i = 0; i < array.length; i++) {
    const letter = array[i];
    if (obj[letter]) {
      obj[letter]++;
    } else {
      obj[letter] = 1;
    }
  }
  return obj;
};

export const getCSRFToken = () => {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.startsWith(name + '=')) {
      return decodeURIComponent(trimmed.split('=')[1]);
    }
  }
  return null;
};
