""" Módulo contendo as funções responsáveis pelos visuais do jogo """

from enum import Enum
from hangman import Hangman
import os


# Carrega as artes ascii em uma variável global
with open("ascii_art.txt", "r") as f:
    global ASCII_ART
    ASCII_ART = f.read().split(",")


# https://stackoverflow.com/a/287944
class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Usado na função `box`
    LIST = [RESET, BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]


def box(text: str):
    lines = text.split("\n")
    longest_line_length = max(
        [len(line) for line in lines]
    )

    text = "╭" + "─" * longest_line_length + "╮"

    for line in lines:
        # Foi o jeito mais fácil que eu achei pra evitar que caracteres de "tamanho zero",
        # como as cores em `Colors`, interfiram na justificação da string.
        # Ver: https://stackoverflow.com/questions/46154561/remove-zero-width-space-unicode-character-from-python-string
        zero_width_chars_len = sum([len(char) * line.count(char) for char in Colors.LIST])
        text += "\n│" + line.ljust(longest_line_length + zero_width_chars_len) + "│"

    text += "\n╰" + "─" * longest_line_length + "╯"

    return text


def render(game: Hangman):
    art = ASCII_ART[len(game.wrong_guesses())]
    wrong_guesses = ", ".join(game.wrong_guesses())
    word = " ".join([char if char != None else "_" for char in game.guessed_positions()])

    art = art.replace("{GUESSES}", colored(Colors.RED, wrong_guesses))
    art = art.replace("{WORD}", colored(Colors.MAGENTA, word))
    print(box(art))


def colored(color: Colors, text: str):
    return color + text + Colors.RESET


# https://stackoverflow.com/a/684344
# Chama os comandos "cls" e "clear" para limpar o terminal no Windows e Linux, respectivamente
def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')
