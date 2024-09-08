from flask import Flask, render_template_string
from Score import get_scores

app = Flask(__name__)


@app.route('/score')
def score_server():
    score_data = get_scores()  # Fetch scores

    # Check for errors or empty score data
    if score_data == -1 or not score_data:
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

    # Safely process the scores list
    formatted_scores = []
    try:
        for score_entry in score_data:
            # Ensure each entry has the correct structure, e.g., ['player', 'score']
            if len(score_entry) >= 2:
                formatted_scores.append(f"{score_entry[0]}: {score_entry[1]}")
            else:
                formatted_scores.append("Invalid score entry")
    except IndexError as e:
        # Log the error or handle it appropriately
        print(f"Error processing score data: {e}")
        error_message = "There was an error processing the scores."
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

    # Render the scores safely
    return render_template_string("""
        <html>
        <head>
            <title>Scores Game</title>
        </head>
        <body>
            <h1>The scores are:</h1>
            <ul>
                {% for score in scores %}
                <li>{{ score }}</li>
                {% endfor %}
            </ul>
        </body>
        </html>
    """, scores=formatted_scores)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8777)