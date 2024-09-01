import os

SCORES_FILE_NAME = "Scores.txt"
BAD_RETURN_CODE = -1

def add_score(player_name, difficulty):
    try:
        points_of_winning = (difficulty * 3) + 5
        if os.path.exists(SCORES_FILE_NAME):
            with open(SCORES_FILE_NAME, 'a') as file:
                file.write(f"{player_name}:{points_of_winning}\n")
        else:
            with open(SCORES_FILE_NAME, 'w') as file:
                file.write(f"{player_name}:{points_of_winning}\n")
    except Exception as e:
        print(f"Error adding score: {e}")
        return BAD_RETURN_CODE

def get_scores():
    try:
        if os.path.exists(SCORES_FILE_NAME):
            with open(SCORES_FILE_NAME, 'r') as file:
                scores = file.readlines()
            return [score.strip().split(':') for score in scores]
        else:
            return []
    except Exception as e:
        print(f"Error reading scores: {e}")
        return BAD_RETURN_CODE