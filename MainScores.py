from flask import Flask, render_template_string
from Score import get_scores

app = Flask(__name__)

@app.route('/score')
def score_server():
    score = get_scores()  # Assuming this is the correct function for fetching scores
    if score == -1:
        error_message = "Could not read the score."
        return render_template_string("""
            <html>
            <head>
                <title>Scores Game</title>
            </head>
            <body>
                <h1><div id="score" style="color:red">{{ error_message }}</div></h1>
            </body>
            </html>
        """, error_message=error_message)

    return render_template_string("""
        <html>
        <head>
            <title>Scores Game</title>
        </head>
        <body>
            <h1>The score is <div id="score">{{ score }}</div></h1>
        </body>
        </html>
    """, score=score)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8777)