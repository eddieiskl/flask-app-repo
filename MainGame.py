from Live import load_game, welcome
from MemoryGame import play_memory_game
from GuessGame import play_guess_game
from CurrencyRouletteGame import play_currency_roulette_game

def main_menu():
    print(welcome("User"))
    game_choice, difficulty = load_game()

    while True:
        if game_choice == 1:
            if play_memory_game(difficulty):
                print("You won the Memory Game!")
            else:
                print("You lost the Memory Game!")
        elif game_choice == 2:
            if play_guess_game(difficulty):
                print("You won the Guess Game!")
            else:
                print("You lost the Guess Game!")
        elif game_choice == 3:
            if play_currency_roulette_game(difficulty):
                print("You won the Currency Roulette Game!")
            else:
                print("You lost the Currency Roulette Game!")

        next_step = input("Enter 'r' to retry, 'm' to go to the main menu, or 'q' to quit: ").lower()
        if next_step == 'r':
            continue
        elif next_step == 'm':
            main_menu()
            break
        elif next_step == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main_menu()