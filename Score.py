import os
import logging

SCORES_FILE_NAME = "Scores.txt"
BAD_RETURN_CODE = -1

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

def add_score(player_name, difficulty):
    """Add a score for a player based on difficulty."""
    try:
        points_of_winning = (difficulty * 3) + 5
        with open(SCORES_FILE_NAME, 'a' if os.path.exists(SCORES_FILE_NAME) else 'w') as file:
            file.write(f"{player_name}:{points_of_winning}\n")
        logging.info(f"Added score for {player_name}: {points_of_winning}")
        return points_of_winning
    except Exception as e:
        logging.error(f"Error adding score for player {player_name}: {e}")
        return BAD_RETURN_CODE

def get_scores():
    """Retrieve all player scores from the file."""
    try:
        if os.path.exists(SCORES_FILE_NAME):
            logging.info(f"File {SCORES_FILE_NAME} found.")
            with open(SCORES_FILE_NAME, 'r') as file:
                scores = file.readlines()
            logging.info(f"Scores read from file: {scores}")
            return [score.strip().split(':') for score in scores]
        else:
            logging.warning(f"File {SCORES_FILE_NAME} not found.")
            return []
    except Exception as e:
        logging.error(f"Error reading scores: {e}")
        return BAD_RETURN_CODE