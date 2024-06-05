#!/bin/python

from hangman import Hangman, GameState
import gpt
import tui


MAX_TRIES = 6

word_history = []


def start_game():
    language = input(tui.colored(tui.Colors.BLUE, "Qual o idioma da palavra? ")).capitalize().strip()
    theme = input(tui.colored(tui.Colors.BLUE, "Qual o tema da palavra? ")).capitalize().strip()
    difficulty = input(tui.colored(tui.Colors.BLUE, "Qual a dificuldade da palavra? ")).capitalize().strip()

    print(tui.colored(tui.Colors.MAGENTA, "\nGerando palavra..."))

    word = gpt.generate_word(theme, language, difficulty, word_history)
    word_history.append(word)
    game = Hangman(word, MAX_TRIES)

    # Loop principal do jogo
    while(game.state() == GameState.RUNNING):
        tui.clear_console()
        tui.render(game)

        guess = ""
        while(True):
            guess = input(tui.colored(tui.Colors.BLUE, "\nQual o seu palpite? ")).strip()

            if not guess.isalpha() or len(guess) != 1:
                print("O palpite deve ser uma única letra.")
            elif game.guessed(guess):
                print("Essa letra já foi escolhida.")
            else:
                game.guess(guess)
                break

    tui.clear_console()
    tui.render(game)

    if game.state() == GameState.WON:
        print(tui.colored(tui.Colors.GREEN, "\nVocê venceu!\n"))
    else:
        print(tui.colored(tui.Colors.RED, "\nVocê perdeu!"))
        print(f"A palavra era \"{word}\"\n")


if __name__ == "__main__":
    tui.clear_console()
    input("Bem vindo ao jogo da forca. Aperte enter para continuar...")
    print() # Linha em branco
    start_game()
    
    while(True):
        response = input("Começar um novo jogo? (s/N) ").lower().strip()

        if (response == "s"):
            tui.clear_console()
            start_game()
        elif (response in ["n", ""] or response.isspace()):
            break
        else:
            print("Reposta inválida. Fechando...")
            break
