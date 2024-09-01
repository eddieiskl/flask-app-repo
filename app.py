from flask import Flask, render_template, request, redirect, url_for, session
import random
import requests

def get_usd_to_ils_rate():
    api_key = 'fca_live_msqOko8jJ0WgGu84WGdZzdOjVxOueCvDGsxx1qqS'
    url = f'https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&currencies=ILS'
    response = requests.get(url)
    data = response.json()
    return data['data']['ILS']

from Score import add_score, get_scores, BAD_RETURN_CODE

app = Flask(__name__)
app.secret_key = 'your_secret_key'
GIPHY_API_KEY = 'tb2FOxW74MH5X43Yn3gSpDGjLN4xiYd2'

def get_gif_url(query):
    try:
        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=1"
        response = requests.get(url)
        if response.status_code == 200:
            gif_data = response.json()
            gif_url = gif_data['data'][0]['images']['original']['url']
            return gif_url
        else:
            return None
    except Exception as e:
        print(f"Error fetching GIF: {e}")
        return None

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    player_name = session.get('player_name', 'Player')
    return render_template('index.html', player_name=player_name)

@app.route('/memory_game', methods=['GET', 'POST'])
def memory_game():
    if request.method == 'POST':
        if 'difficulty' in request.form:
            difficulty = int(request.form.get('difficulty'))
            sequence = [random.randint(1, 101) for _ in range(difficulty)]
            session['difficulty'] = difficulty
            session['sequence'] = sequence
            return render_template('memory_game.html', sequence=sequence, show_sequence=True)
        else:
            user_sequence = request.form.get('sequence').split()
            user_sequence = [int(num) for num in user_sequence]
            sequence = session.get('sequence', [])
            player_name = session.get('player_name', 'Player')
            difficulty = session.get('difficulty', 1)

            if user_sequence == sequence:
                add_score(player_name, difficulty)
                gif_url = get_gif_url("win")
                return redirect(url_for('result', result_message="Congratulations! You won the Memory Game!",
                                        retry_url=url_for('memory_game'), gif_url=gif_url))
            else:
                gif_url = get_gif_url("lose")
                return redirect(url_for('result',
                                        result_message="Sorry, you lost the Memory Game. The correct sequence was {}.".format(
                                            sequence), retry_url=url_for('memory_game'), gif_url=gif_url))

    return render_template('memory_game.html', show_sequence=False)

@app.route('/memory_game_check', methods=['POST'])
def memory_game_check():
    user_sequence = request.form.get('sequence')
    try:
        user_sequence = [int(num) for num in user_sequence.split()]
        actual_sequence = session.get('sequence')
        difficulty = session.get('difficulty')
        player_name = session.get('player_name', 'Player')
        if user_sequence == actual_sequence:
            add_score(player_name, difficulty)
            gif_url = get_gif_url("win")
            return redirect(url_for('result', result_message="Congratulations! You won the Memory Game!",
                                    retry_url=url_for('memory_game'), gif_url=gif_url))
        else:
            gif_url = get_gif_url("lose")
            return redirect(
                url_for('result', result_message="Sorry, you lost the Memory Game.", retry_url=url_for('memory_game'),
                        gif_url=gif_url))
    except ValueError:
        gif_url = get_gif_url("error")
        return redirect(url_for('result', result_message="Invalid input! Please enter numbers only.",
                                retry_url=url_for('memory_game'), gif_url=gif_url))

@app.route('/guess_game', methods=['GET', 'POST'])
def guess_game():
    if request.method == 'POST':
        if 'difficulty' in request.form:
            session['difficulty'] = int(request.form.get('difficulty'))
            session['secret_number'] = random.randint(1, session['difficulty'])
            return render_template('guess_game.html', ask_for_guess=True)

        guess = int(request.form.get('guess'))
        difficulty = session.get('difficulty')
        secret_number = session.get('secret_number')
        player_name = session.get('player_name', 'Player')

        if guess == secret_number:
            add_score(player_name, difficulty)
            gif_url = get_gif_url("win")
            session.pop('difficulty', None)
            session.pop('secret_number', None)
            return redirect(url_for('result', result_message="Congratulations! You guessed correctly!",
                                    retry_url=url_for('guess_game'), gif_url=gif_url))
        else:
            gif_url = get_gif_url("lose")
            session.pop('difficulty', None)
            session.pop('secret_number', None)
            return redirect(url_for('result',
                                    result_message="Sorry, you guessed wrong. The correct number was {}.".format(
                                        secret_number), retry_url=url_for('guess_game'), gif_url=gif_url))

    return render_template('guess_game.html', ask_for_guess=False)

@app.route('/currency_roulette_game', methods=['GET', 'POST'])
def currency_roulette_game():
    if request.method == 'POST':
        if 'difficulty' in request.form:
            difficulty = int(request.form.get('difficulty'))
            session['difficulty'] = difficulty
            amount = random.randint(1, 100)
            session['amount'] = amount
            return render_template('currency_roulette_game.html', amount=amount, show_guess=True)
        else:
            guess = float(request.form.get('guess'))
            difficulty = session.get('difficulty', 1)
            amount = session.get('amount', 0)
            player_name = session.get('player_name', 'Player')
            rate = get_usd_to_ils_rate()
            total_value = amount * rate
            margin = 5 - difficulty
            min_value = total_value - margin
            max_value = total_value + margin

            if min_value <= guess <= max_value:
                add_score(player_name, difficulty)
                gif_url = get_gif_url("win")
                return redirect(url_for('result', result_message="Congratulations! You won the Currency Roulette Game!",
                                        retry_url=url_for('currency_roulette_game'), gif_url=gif_url))
            else:
                gif_url = get_gif_url("lose")
                return redirect(url_for('result',
                                        result_message="Sorry, you lost the Currency Roulette Game. The correct value was {:.2f} ILS.".format(total_value),
                                        retry_url=url_for('currency_roulette_game'), gif_url=gif_url))

    return render_template('currency_roulette_game.html', show_guess=False)

@app.route('/result')
def result():
    result_message = request.args.get('result_message')
    retry_url = request.args.get('retry_url')
    gif_url = request.args.get('gif_url')
    return render_template('result.html', result_message=result_message, retry_url=retry_url, gif_url=gif_url)

@app.route('/score')
def score():
    try:
        scores = get_scores()
        print(f"Scores: {scores}")
        if scores == BAD_RETURN_CODE:
            return render_template('score.html', current_score="Could not read the score.", top_scores=[])
        current_score = scores[-1][1] if scores else "0"
        top_scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]
        return render_template('score.html', current_score=current_score, top_scores=top_scores)
    except Exception as e:
        print(f"Error in /score route: {e}")
        return render_template('score.html', current_score="Could not read the score.", top_scores=[])

@app.route('/set_name', methods=['POST'])
def set_name():
    player_name = request.form.get('player_name')
    if player_name:
        session['player_name'] = player_name
    return redirect(url_for('index'))

@app.route('/quit')
def quit():
    gif_url = get_gif_url("goodbye")
    return render_template('quit.html', gif_url=gif_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)