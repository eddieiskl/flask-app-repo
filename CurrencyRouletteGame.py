import random
import requests

class CurrencyRouletteGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.random_amount = random.randint(1, 100)
        self.current_rate = self.get_currency_rate()

    def get_currency_rate(self):
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates']['ILS']

    def get_money_interval(self):
        t = self.random_amount * self.current_rate
        return (t - (5 - self.difficulty), t + (5 - self.difficulty))

def play_currency_roulette_game(difficulty):
    game = CurrencyRouletteGame(difficulty)
    money_interval = game.get_money_interval()
    random_amount = game.random_amount
    return money_interval, random_amount