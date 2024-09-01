import random

class GuessGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.secret_number = 0

    def generate_number(self):
        self.secret_number = random.randint(1, self.difficulty)
        return self.secret_number

    def compare_results(self, user_guess):
        return self.secret_number == user_guess

def play_guess_game(difficulty):
    game = GuessGame(difficulty)
    secret_number = game.generate_number()
    return secret_number