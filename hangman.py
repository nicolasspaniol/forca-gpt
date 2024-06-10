""" Módulo que implementa a lógica principal do jogo """

from enum import Enum
import unicodedata
from typing import Optional


ALLOWED_SPECIAL_CHARS = [" ", "-"]


def normalize(text: str) -> str:
    text = text.upper()
    text = unicodedata.normalize("NFD", text)
    return text.encode("ascii", "ignore").decode("utf-8") 


class GameState(Enum):
    WON = 0,
    LOST = 1,
    RUNNING = 2


class Hangman:
    def __init__(self, word: str, max_tries: int):
        assert all([char.isalpha() or char in ALLOWED_SPECIAL_CHARS for char in word]) 

        self.max_tries = max_tries
        self.word = word.upper()
        # https://stackoverflow.com/a/44433664
        self.normalized_word = normalize(word)
        self.guesses = []


    def guess(self, guess: str) -> None:
        assert len(guess) == 1 and guess.isalpha()

        guess = normalize(guess)
        self.guesses.append(guess)


    def state(self) -> GameState:
        # Todas as letras foram adivinhadas, portanto, vitória
        if all([char in self.guesses or char in ALLOWED_SPECIAL_CHARS for char in self.normalized_word]):
            return GameState.WON

        # O número de tentativas erradas chegou ao limite, portanto, derrota
        if len([char for char in self.guesses if char not in self.normalized_word]) == self.max_tries:
            return GameState.LOST

        return GameState.RUNNING


    def guessed_positions(self) -> list[Optional[str]]:
        for (i, char) in enumerate(self.word):
            normalized_char = self.normalized_word[i]

            if normalized_char in self.guesses or char in ALLOWED_SPECIAL_CHARS:
                yield char
            else:
                yield None


    def guessed(self, guess: str) -> bool:
        return normalize(guess) in self.guesses


    def wrong_guesses(self) -> list[str]:
        return [guess for guess in self.guesses if guess not in self.normalized_word]
