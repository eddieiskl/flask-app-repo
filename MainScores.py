from flask import Flask, render_template_string
from Score import get_scores
import logging

# Initialize the Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/score')
def score_server():
    try:
        score_data = get_scores()
        if score_data == -1:
            raise Exception("Could not read the score file.")
        if not score_data:
            raise Exception("Score file is empty or not found.")
        # Continue with score display logic
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"Error: {e}"

        # Safely process the scores list and skip invalid entries
        formatted_scores = []
        for score_entry in score_data:
            try:
                if len(score_entry) >= 2:
                    formatted_scores.append(f"{score_entry[0]}: {score_entry[1]}")
                else:
                    logging.warning(f"Invalid score entry: {score_entry}")
            except Exception as e:
                logging.error(f"Error processing score entry {score_entry}: {e}")

        logging.info(f"Processed formatted scores: {formatted_scores}")

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

    except Exception as e:
        error_message = f"Error processing score data: {e}"
        logging.error(error_message)
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

# Run the application on port 8777
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8777)