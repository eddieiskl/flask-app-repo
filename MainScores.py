from flask import Flask, render_template_string
from Score import get_scores

app = Flask(__name__)

@app.route('/score')
def score_server():
    scores = get_scores()
    if scores == -1:
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

    # Format the scores in a user-friendly table
    return render_template_string("""
        <html>
        <head>
            <title>Scores Game</title>
        </head>
        <body>
            <h1>The scores are:</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {% for score in scores %}
                    <tr>
                        <td>{{ score[0] }}</td>
                        <td>{{ score[1] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
    """, scores=scores)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8777)