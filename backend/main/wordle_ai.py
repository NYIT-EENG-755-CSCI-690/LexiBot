from abc import ABC, abstractmethod
from enum import Enum, auto
import string
import itertools
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

combined_path = os.path.join(BASE_DIR, 'assets', 'combined_wordlist.txt')
real_wordles_path = os.path.join(BASE_DIR, 'assets', 'shuffled_real_wordles.txt')

class LetterInformation(Enum):
    UNKOWN = auto()  # light grey in the game
    PRESENT = auto()  # yellow in the game
    NOT_PRESENT = auto()  # dark grey in the game
    CORRECT = auto()  # green in the game


class WordleAI(ABC):

    def __init__(self, words):
        self.words = words  # list of all legal 5 letter words

    @abstractmethod
    def guess(self, guess_history):
        """
        Returns a 5 letter word trying to guess the wordle.

        Parameters
        ----------
        guess_history : list of tuples (guess, result)
            A list of tuples (word, result) with result consisting of LetterInformation for each letter on their
            position specifically, for example one previous guess with the guess 'steer' for the word 'tiger':
            [('steer',[LetterInformation.NOT_PRESENT, LetterInformation.PRESENT,
            LetterInformation.PRESENT, LetterInformation.CORRECT, LetterInformation.CORRECT])]
        """
        pass

    @abstractmethod
    def get_author(self):
        """
        Returns the name of the author
        """
        pass



class WordList:
    """
    Reads a list of words from a file and filters it for wordle compatible words.
    Used to provide word list copies.
    """

    def __init__(self, filename):
        self.ascii_lowercase = list(string.ascii_lowercase)
        with open(filename, encoding="utf8") as file:
            self.words = file.readlines()
            self.words = [word.rstrip() for word in self.words]
            self.words = [w for w in self.words if len(w) == 5 and self.is_ascii_lowercase(w)]
            self.words = list(dict.fromkeys(self.words))  # remove duplicates


    def get_list_copy(self):
        return self.words.copy()

    def is_ascii_lowercase(self, word):
        for letter in word:
            if letter not in self.ascii_lowercase:
                return False
        return True

class WordleJudge:
    """
    Helper class to take into account how common words are in the English language.
    """

    def __init__(self, words=WordList(combined_path).words,
                 common_words=WordList(real_wordles_path).words):
        self.common_words = common_words
        self.probability = {}
        for word in words:
            self.probability[word] = self.__calculate_probability(word)

    def __calculate_probability(self, word):
        if word not in self.common_words:
            return 368 / (368 + 8890)
        relative_position = self.common_words.index(word) / len(self.common_words)
        return 0.85 * (1 - relative_position) + 0.35 * relative_position

    def is_wordle_probability(self, word):
        """
        :param word: a 5 letter word
        :return: the probability of the word being a wordle based on its popularity in the English language
        """
        return self.probability[word]



# from WordleAI import WordleAI, LetterInformation
# from WordleJudge import WordleJudge

class EntropyAI(WordleAI):
    def __init__(self, words):
        super().__init__(words)
        self.judge = WordleJudge(words)
        self.cache = {}

    def guess(self, guess_history):
        candidates = self.words
        for (guess, outcome) in guess_history:
            for i, x in enumerate(outcome):
                if x == LetterInformation.CORRECT:
                    candidates = [x for x in candidates if x[i] == guess[i]]
                elif x == LetterInformation.PRESENT:
                    candidates = [x for x in candidates if x[i] != guess[i] and guess[i] in x]
                else:
                    candidates = [x for x in candidates if guess[i] not in x]
        return self.cached_get_candidate(candidates, self.words, guess_history)

    def get_author(self):
        return "achen33"

    """
    This function provides three probability values:
    p[ch][i] -> probability of finding character at i out of all words
    q[ch][i] -> probability of finding character at a location other than i out of all words
    r[ch] -> probability of a character not being in any location out of all words
    """
    def get_probability_distributions(self, words):
        p = {}
        q = {}
        r = {}

        for k in range(26):
            k = chr(k + 97)
            p[k] = [0.0] * 5
            q[k] = [0.0] * 5
            r[k] = 0

        for word in words:
            for i, ch in enumerate(word):
                p[ch][i] += 1

        for word in words:
            for i, ch in enumerate(word):
                for j in range(5):
                    if word[j] != ch:
                        q[ch][j] += 1

        for word in words:
            for ch in set(word):
                r[ch] += 1

        for k in range(26):
            k = chr(k + 97)
            p[k] = [x / len(words) for x in p[k]]
            q[k] = [x / len(words) for x in q[k]]
            r[k] = 1 - r[k] / len(words)

        return p, q, r

    def safe_entropy(self, p):
        return p * math.log(p) if p != 0 else 0

    def get_score(self, word, p, q, r):
        entropy = 0
        frequency = {}
        for ch in word:
            frequency[ch] = frequency.get(ch, 0) + 1
        for i, ch in enumerate(word):
            entropy -= self.safe_entropy(p[ch][i])
            entropy -= self.safe_entropy(q[ch][i]) / frequency[ch] # special assumption when a character is repeated more than once
            entropy -= self.safe_entropy(r[ch])
        return entropy

    def cached_get_candidate(self, words, all_words, guess_history):
        key = tuple(itertools.chain(*[[x[0]]+x[1] for x in guess_history]))
        if key in self.cache:
            return self.cache[key]
        value = self.get_candidate(words, all_words)
        if len(guess_history) < 2:
            self.cache[key] = value
        return value

    def get_candidate(self, words, all_words):
        m = 0
        best = words[0]
        p, q, r = self.get_probability_distributions(words)

        # Once the number of words become small enough, restrict search to that.
        if len(words) <= 2:
            all_words = words

        for word in all_words:
            s = self.get_score(word, p, q, r) + self.judge.is_wordle_probability(word)
            if s > m:
                m = s
                best = word
        return best

    def get_feedback(self, guess, target):
        print("getting feedback")
        feedback = []
        for i, ch in enumerate(guess):
            if ch == target[i]:
                feedback.append(LetterInformation.CORRECT)
            elif ch in target:
                feedback.append(LetterInformation.PRESENT)
            else:
                feedback.append(LetterInformation.NOT_PRESENT)
        return feedback
